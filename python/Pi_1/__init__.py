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
from PiCam import PiCam

#Setup the pins on the Pi
print('Setting up Pins')
REXUS_LO = 40
REXUS_SOE = 38
REXUS_SODS = 36
OUT_LED = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(REXUS_LO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(REXUS_SOE, GPIO.IN)
GPIO.setup(REXUS_SODS, GPIO.IN)
GPIO.setup(OUT_LED, GPIO.OUT)

def flash_led(channel):    
    #Flash some LED's
    for i in range(0,5):
        print('Flashing LEDs')
        GPIO.output(OUT_LED,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(OUT_LED,GPIO.LOW)
        time.sleep(0.1)

flash_led(None)
GPIO.add_event_detect(REXUS_LO, GPIO.RISING, callback=flash_led, bouncetime=500)


IMU_1.take_measurements(10)
camera = PiCam()
camera.video_cut = 5
camera.video(20,'test')

#TODO create REXUS class for communicating with ground
REXUS_Comm = REXUS()

#TODO Check System Status

#TODO Check for Hardware Test Mode- GPIO??

while 1:
    #TODO Communicate with ground before lift-off
    Message = 'Some data to send'
    Response = REXUS_Comm.communicate(Message)
    #TODO Check for Software Test Mode- REXUS?
    if Response == 'Test Mode':
        break
    #TODO Check for command to start camera  
    if Response == 'T-10':
        #TODO Activate Camera
        break
    #TODO Check for Lift-off GPIO
    
    break


#TODO Check for SOE- GPIO

#TODO Activate IMU and Motor

#TODO Read Encoder to check for Boom deployment- send to ground

#TODO Check for SODS- GPIO

#TODO Backup Data (between pi's)
