import serial  # подключаем библиотеку для последовательной связи
import time  # подключаем библиотеку чтобы задействовать функции задержки в программе
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


# def start_mesuring(pusk):
ArduinoSerial = serial.Serial('com3', 9600)  # создаем объект для работы с портом последовательной связи
# time.sleep(2)  # ждем 2 секунды чтобы установилась последовательная связь
# print (ArduinoSerial.readline()) #считываем данные из последовательного порта и печатаем их в виде строки
# print("Enter 1 to turn ON LED and 0 to turn OFF LED")
camera_stream = VideoStream(src=0).start()
while True:
    is_person_detected = check_person(camera_stream)
    if is_person_detected == '1':
        print('Human detected')
    else:
        print('Human not detected')
    ArduinoSerial.write(is_person_detected.encode())  # передаем 1
    # print ("LED turned ON")
    # print (ArduinoSerial.readline())
    time.sleep(1)
    # time.sleep(15)
    # print (ArduinoSerial.readline())
