import serial  # connect the library for serial communication
import time  # connect the library to use the delay functions in the program
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2


def check_person(camera_stream):
    # Classes which can be detected by a model
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    # Loading model
    net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')
    # Getting frame by a camera
    frame = camera_stream.read()
    if frame is None:
        print('Camera connection failed')
        return '0'
    # Frame's processing
    frame = imutils.resize(frame, width=400)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    # Checking frame's result for a person and returning '1' or '0' and stop the stream
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] != 'person':
                continue
            else:
                return '1'
        else:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] == 'person':
                return '0'
    return '0'



ArduinoSerial = serial.Serial('com3', 9600)  # create an object to work with a serial communication port
time.sleep(2)  # wait 2 seconds for serial communication to be established
# print (ArduinoSerial.readline()) # read data from the serial port and print it as a string
# print("Enter 1 to turn ON LED and 0 to turn OFF LED")
camera_stream = VideoStream(src=0).start()
while True:
    is_person_detected = check_person(camera_stream)
    if is_person_detected == '1':
        print('Human detected')
        ArduinoSerial.write(is_person_detected.encode())  # pass 1
        check = str(ArduinoSerial.readline()) 
        a = str(b'1\r\n')
        b = str(b'2\r\n')
        c = str(b'3\r\n')
        d = str(b'4\r\n')
        while (check != a):
            check = str(ArduinoSerial.readline())
            print (check)
            if (check == b):
                print ('Move your hand to the sensor')
            if (check == c):
                print ('Temperature is normal, come through')
            if (check == d):
                print ('No passage, high temperature')
    else:
        print('Human not detected')
        ArduinoSerial.write(is_person_detected.encode())  # pass 0
    # print ("LED turned ON")
    # print (ArduinoSerial.readline())
    time.sleep(1)
    #time.sleep(15)
    # print (ArduinoSerial.readline())
