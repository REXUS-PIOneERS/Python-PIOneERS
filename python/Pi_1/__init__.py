"""
The main thread for Pi_1 of the REXUS PIOneERS project, controlling most of the logic
operations for the entire experiment.
"""
#Imports for the raspbeery pi
import RPi.GPIO as GPIO
#Imports for the program
import time
#Imports of local files and classes
from REXUS import REXUS
import IMU_1

#Setup all the pins on the Pi
print('Setting up GPIO Pins')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.IN)
GPIO.setup(40, GPIO.OUT)

#Flash some LED's
for i in range(0,5):
    print('Flashing LEDs')
    GPIO.output(40,GPIO.LOW)
    time.sleep(2)
    GPIO.output(40,GPIO.HIGH)
    time.sleep(2)

while 1:
    button = GPIO.input(35)
    print(button)
    if button = 1:
        break

GPIO.output(40,GPIO.LOW)

GPIO.cleanup()
#TODO create REXUS class for communicating with ground
REXUS_Comm = REXUS()

#TODO Check System Status

#TODO Check for Hardware Test Mode- GPIO??

while 1:
    #TODO Communicate with ground before lift-off
    Message = 'Some data to send'
    Response = REXUS_Comm.communicate(Message)
    
    #TODO Check for Software Test Mode- REXUS?
    #TODO Check for command to start camera    
    #TODO Check for Lift-off GPIO
    break


#TODO Check for SOE- GPIO

#TODO Activate IMU and Motor

#TODO Read Encoder to check for Boom deployment- send to ground

#TODO Check for SODS- GPIO

#TODO Backup Data (between pi's)
