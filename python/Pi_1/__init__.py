"""
The main thread for Pi_1 of the REXUS PIOneERS project, controlling most of
the logic operations for the entire experiment.
"""
# Imports for the raspbeery pi
import RPi.GPIO as GPIO
# Imports for the program
import time
# Imports of local files and classes
from REXUS import REXUS
from IMU import IMU
from PiCam import PiCam

# Setup the pins on the Pi
print('Setting up Pins')
REXUS_LO = 40
REXUS_SOE = 38
REXUS_SODS = 36
OUT_LED = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(REXUS_LO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(REXUS_SOE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(REXUS_SODS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OUT_LED, GPIO.OUT)

# Setup classes for REXUS, IMU and PiCam
REXUS_Comm = REXUS()
PiCam_1 = PiCam()
PiCam_1.video_cut = 5
IMU_1 = IMU()


# Random Test Function for flashing an LED
def flash_led():
    print('Flashing LEDs')
    for i in range(0, 5):
        GPIO.output(OUT_LED, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(OUT_LED, GPIO.LOW)
        time.sleep(0.1)


def start_of_data_storage():
    '''Backs up data between both Pi's'''
    print('Start of data storage')
    # End the IMU measurements
    IMU_1.end_measurements_processes()
    flash_led()


def start_of_experiment():
    '''Runs at start of experiment i.e. Nose Cone Ejection'''
    print('start of experiment')
    flash_led()
    # Activate the IMU
    IMU_1.take_measurements_process(1, 'placeholder')
    # TODO Motor Deplyment
    while not GPIO.input(REXUS_SODS):
        time.sleep(0.1)
    start_of_data_storage()


def lift_off():
    '''Program that runs after the rocket lifts off'''
    print('LIFT OFF!!!')
    flash_led()
    if not PiCam_1.active:
        PiCam_1.video(1, 'test')
    while not GPIO.input(REXUS_SOE):
        # TODO Send occasional messages to ground reporting status
        time.sleep(0.1)
    start_of_experiment()


def main():
    '''Main entry point for the probram'''
    flash_led()
    # TODO Check for Hardware Test Mode- GPIO??
    # TODO Check System Status
    while 1:
        # TODO REXUS Communications
        Message = 'Some data to send'
        Response = REXUS_Comm.communicate(Message)
        if Response == 'Test Mode':
            break
        if Response == 'T-10':
            PiCam_1.video(10, 'test')
        if GPIO.input(REXUS_LO):
            lift_off()
            break

# Start the main program
try:
    main()
except KeyboardInterrupt:
    # Something to handle the exception
    pass
finally:
    GPIO.cleanup()
