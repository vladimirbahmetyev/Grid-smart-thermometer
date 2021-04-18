import serial #подключаем библиотеку для последовательной связи
import time #подключаем библиотеку чтобы задействовать функции задержки в программе
 
#def start_mesuring(pusk):
ArduinoSerial = serial.Serial('com3',9600) #создаем объект для работы с портом последовательной связи
time.sleep(2) #ждем 2 секунды чтобы установилась последовательная связь
#print (ArduinoSerial.readline()) #считываем данные из последовательного порта и печатаем их в виде строки
print ("Enter 1 to turn ON LED and 0 to turn OFF LED")
#pusk = 0

while 1: #бесконечный цикл
    #pusk = str(get_parameter())   #<---------------------------------ТУТ НУЖНО ДОБАВИТЬ ВЫЗОВ ФУНКЦИИ
    var = str(input()) #pusk #считываем данные от пользователя
    print ("Human detected", var) #печатаем подтверждение ввода    
    if (var == '1'): #если значение равно 1
        ArduinoSerial.write('1'.encode()) #передаем 1
        #print ("LED turned ON")
        #print (ArduinoSerial.readline())
        time.sleep(1) 
        #на проде добавить больше тайм слип, чтобы человек вышел из кадра?????

    if (var == '0'): # если значение равно 0
        ArduinoSerial.write('0'.encode()) #передаем 0
        #print ("LED turned OFF")
        time.sleep(1)
    #time.sleep(15)
    #print (ArduinoSerial.readline())