# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-s", "--server-ip", required=True,
# 	help="ip address of the server to which the client will connect")
# args = vars(ap.parse_args())

# uncomment below if we are using server di ruangan Kak Reza 
host_address = 'tcp://10.30.60.110:5555'

# uncomment below if wa are using localhost
# host_address = 'tcp://localhost:5555'

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to=host_address)

# raspberry name should be the same as camID
# cause it will be use to to POST data from
# the server, and variable rpiName will be use
# as camID for posting the data to the database 
rpiName = 1
print('rpiName : ', rpiName)

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0).start()
print('starting camera..')
time.sleep(2.0)
print('Camera should be done starting')
 
print('Started sending video frames to server...')
while True:
	# read the frame from the camera and send it to the server
	frame = vs.read()
	# print('Read Frame')
	sender.send_image(rpiName, frame)
	# print('Sent Frame')