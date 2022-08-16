# import the necessary packages
from imutils import build_montages
from datetime import datetime
import imagezmq
import argparse
import imutils
import cv2

# For running inference on the TF-Hub module.
import tensorflow as tf
import tensorflow_hub as hub

# For data manipulation.
import numpy as np
import pandas as pd

# For distance calculation.
from scipy.spatial import distance as dist

# For using HTTP to POST the data to the API.
import requests

# URL for API
URL = 'http://10.30.60.110:5050/sl_vision_post'

# Print Tensorflow version and starting to load model
print('Starting To Load Model...')
print('TF version :',tf.__version__)

# Model Folder
module_handle = "mobilenet"
# Loading model
detector = hub.load(module_handle).signatures['default']
print('Load Model Finish...')

# Read the pre define points of interests
points_data = pd.read_csv('data.csv')

# initialize the ImageHub object
print('Starting ImageZMQ Server')

# uncomment below if we are using server di ruangan Kak Reza 
# imageHub = imagezmq.ImageHub(open_port='tcp://192.168.43.118:5555')

# uncomment below if wa are using localhost
imageHub = imagezmq.ImageHub(open_port='tcp://10.30.60.110:5555')

# initialize the dictionary which will contain  information regarding
# when a device was last active, then store the last time the check
# was made was now
# lastActive = {}
# lastActiveCheck = datetime.now()

# start looping over all the frames
while True:
    # this variable hold the key of a point and the value is the number of person counted in that point
    # example, there is a point called "Sofa", Sofa is the key to the python dict and the value is the number
    # of person near the point "Sofa". and this name (Sofa) will be in accordance to the csv data that
    # holds the points pre-define
    jumlah = dict.fromkeys(points_data.values[:,0],0)
    
    # print('waiting for image...')
    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    (rpiName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')

    # if a device is not in the last active dictionary then it means
    # that its a newly connected device
    # if rpiName not in lastActive.keys():
    #     print("[INFO] receiving data from {}...".format(rpiName))

    # record the last active time for the device from which we just
    # received a frame
    # lastActive[rpiName] = datetime.now()

    # ML TO BE HERE
    im_tensor = tf.convert_to_tensor(frame)
    im_tensor = tf.image.convert_image_dtype(frame, tf.float32)[tf.newaxis, ...]
    imH = frame.shape[0]
    imW = frame.shape[1]

    result = detector(im_tensor)

    # filter only person class
    index_person_detected = np.where(result["detection_class_entities"] == b'Person')[0]
    # filter against the with object that has confindent scored over 0.2
    index_person_detected_minscore = np.where(result["detection_scores"].numpy()[index_person_detected] > 0.2)[0]

    # separate the results into variables
    boxes = result["detection_boxes"].numpy()[index_person_detected][index_person_detected_minscore] # Bounding box coordinates of detected objects
    classes = result["detection_class_entities"].numpy()[index_person_detected][index_person_detected_minscore]  # Class index of detected objects
    scores =  result["detection_class_entities"].numpy()[index_person_detected][index_person_detected_minscore] # Confidence of detected objects    
    
    # convert boxes value to pixel unit
    boxes = boxes*[[imH, imW, imH, imW]]

    p_centroids = []
    for i in np.int16(boxes):
        ymin, xmin, ymax, xmax = i
        centerX = (xmin+xmax)/2
        centerY = (ymin+ymax)/2
        p_centroids.append((centerX, centerY))

    for centroid in p_centroids:
        all_dist = []
        for i in range(points_data.shape[0]):
            d = dist.euclidean( (points_data.iloc[int(i),1],points_data.iloc[int(i),2]) , (centroid[0], centroid[1]) )
            t = (points_data.iloc[int(i),0],(points_data.iloc[int(i),1],points_data.iloc[int(i),2]),(centroid[0],centroid[1]),d)
            all_dist.append(t)

        all_dist.sort(key=lambda x: x[3])

        update = jumlah[all_dist[0][0]] + 1 
        jumlah[all_dist[0][0]] = update

    # print(jumlah)
    # END OF ML

    # Post data to API for every point of interests
    for key, value in jumlah.items():
        dictRes = {'id_cam' : rpiName, 'id_dot': key, 'people_count ': value}
        print(dictRes)
        x = requests.post(URL, json = dictRes)

    frame = imutils.resize(frame, width=400)
    cv2.imwrite("Image.png", frame)