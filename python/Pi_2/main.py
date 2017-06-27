"""
The main thread for Pi_1 of the REXUS PIOneERS project, controlling most of
the logic operations for the entire experiment.
"""
# Imports for the raspbeery pi
import RPi.GPIO as GPIO
# Imports for the program
import time
# Imports of local files and classes
from RPi_SPI import SPI_Slave
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

# Setup classes for ImP, SPI and PiCam
CLK = 12
MISO = 16
MOSI = 18
CS = 22
SPI = SPI_Slave(CLK, MISO, MOSI, CS)
# Set channel 0 to 1 to show slave is active
SPI.channels[0] = 1
PiCam_2 = PiCam()
ImP = None  # TODO Setup UART communication for ImP


def flash_led():
    '''Test function that flashes an LED'''
    print('Flashing LEDs')
    for i in range(0, 5):
        GPIO.output(OUT_LED, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(OUT_LED, GPIO.LOW)
        time.sleep(0.1)


def start_of_data_storage():
    '''Backs up data between both Pi's'''
    print('Start of data storage')
    flash_led()


def start_of_experiment():
    '''Runs at start of experiment i.e. Nose Cone Ejection'''
    print('start of experiment')
    flash_led()
    # TODO UART Communication with ImP
    while not GPIO.input(REXUS_SODS):
        time.sleep(0.1)
    start_of_data_storage()


def lift_off():
    '''Program that runs after the rocket lifts off'''
    print('LIFT OFF!!!')
    flash_led()
    if not PiCam_2.active:
        PiCam_2.background_record_process('video', 5)
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
        # TODO SPI communications with Pi_1
        Response = None
        if Response == 'Test Mode':
            break
        if Response == 'T-10':
            PiCam_2.background_record_process("video", 5)
        if GPIO.input(REXUS_LO):
            lift_off()
            break

# Start the main program
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
