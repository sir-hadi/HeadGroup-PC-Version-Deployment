# Server Side
## Dependecy and packages
to run the program we need to install some dependecy. there is a file
called requirments.txt and packages.txt, first install the requirments using
this command : 
pip3 install -r requirements.txt

be sure to install python3 first. after finishing instaling try to run the code first.
the running time will take some time, if the its running and there is no problem then you
dont need to install the packages.txt. if there is a error regarding some libXX-dev, try to 
install packages.txt with the command below:

``` 
xargs sudo apt-get install packages.txt 
```

## Running the server side code
The server uses 'ServerSideVidStream.py'. to run the
script it needs two argument which are below:
-> --ip : the ip address of where the server
example command : 

```
python3 ServerSideVidStream.py --ip=192.168.88.12
```

NOTE !!! : tha program needs a csv file called 'data.csv' to run, data.csv holds
the point of each light that should be control. data.csv must have a header 
'id','x', and 'y'. here is an example of whats inside the data.csv file:

```
id,x,y
1,101,102
2,600,1000
3,700,1100
```


# Client Side
## Dependecy and packages
to install the dependecy use the command below on your client device
```
pip3 install -r raspi-requirments.txt
```

## Running the client side code
Client/Raspberry Device/Camera Device uses 'ClientVidStream.py'. to run the
script it needs two argument which are below:
-> --host : the ip address of where the server code is running
-> --id   : id of the camere
example command :
```
python3 ClientVidStream.py --host=192.168.88.12 --id=1
```
