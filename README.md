## Grid-smart-thermometer
## Grid & Cloud, SPBU

## How it works
1. The program expects some video stream, after which the script analyzes the frame and determines whether a person is on the frame or not.
2. If a person has been detected, the program sends a signal to the Arduino uno platform to go into human standby mode
3. As soon as the person is close enough, the Arduino switches to temperature measurement mode
4. After measuring the temperature, the result is displayed on the screen
5. Then the detection will start again

## Requirements
### Hardware requierements:
* Arduino Uno plarftorm kit
* Two colored light bulbs
* Ultrasonic distance meter HC-SR04
* Infrared temperature meter GY-906
* PC
* A camera that can be connected to a PC

### Program requirements:
* Python 3.8
## How to run it
1. Install requirements.txt  ```pip install -r requirements.txt```
2. Install 'i2cmaster.h' and 'NewPing.h' for programming Arduino Uno
3. Connect Arduino and Camera to PC
4. Start script 'gui.py'
5. Press button 'Start'
6. Observe the result
