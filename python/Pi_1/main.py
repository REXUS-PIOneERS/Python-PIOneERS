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
from RPi_SPI import SPI_Master

# Setup the pins on the Pi
print('Setting up Pins')

GPIO.setmode(GPIO.BOARD)
# Main GPIO's for REXUS Signals
REXUS_LO = 40
REXUS_SOE = 38
REXUS_SODS = 36
GPIO.setup(REXUS_LO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(REXUS_SOE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(REXUS_SODS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Pins for SPI Communication
CLK = 29  # clock
MISO = 31  # Master in Slave out, used to transmit FROM the Slave device
MOSI = 33  # Master out Slave in, used to transmit FROM the Master device
CS = 35  # Chip select
SPI = SPI_Master(CLK, MISO, MOSI, CS)

# Output pins
OUT_LED = 37
MOTOR = None  # TODO Set up PWM for motor
GPIO.setup(OUT_LED, GPIO.OUT)

# TODO Pins for UART Communication with the IMP


# Setup classes for REXUS, IMU and PiCam
REXUS_Comm = REXUS()
PiCam_1 = PiCam()
PiCam_1.video_cut = 5
IMU_1 = IMU()
IMU_1.setup_default()


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
    # End the background video
    PiCam_1.end_background_process()
    flash_led()


def start_of_experiment():
    '''Runs at start of experiment i.e. Nose Cone Ejection'''
    print('start of experiment')
    flash_led()
    # Activate the IMU
    conn = IMU_1.take_measurements_process(5, 'IMU_Test', 5)
    # TODO Motor Deplyment
    n = 0
    while not GPIO.input(REXUS_SODS):
        n += 1
        # TODO Send measurements back to ground
        if n == 10:
            n = 0
            # Get data from IMU_1
            print(conn.recv())
            # TODO Get IMP and IMU_2 data via SPI
        time.sleep(0.1)
    start_of_data_storage()


def lift_off():
    '''Program that runs after the rocket lifts off'''
    print('LIFT OFF!!!')
    flash_led()
    if not PiCam_1.active:
        PiCam_1.background_record_process('cam', cut_length=5)
    while not GPIO.input(REXUS_SOE):
        # TODO Send occasional messages to ground reporting status
        time.sleep(0.1)
    start_of_experiment()


def main():
    '''Main entry point for the probram'''
    flash_led()
    # Channel 0 will be equal to 1 when slave is active
    slave_active = SPI.request_data(0, 8)
    if not slave_active:
        print("SPI communication with slave failed")
    else:
        print("SPI communication with slave succeeded")
    # TODO Check for Hardware Test Mode- GPIO??
    # TODO Check System Status
    while 1:
        # TODO REXUS Communications
        Message = 'Some data to send'
        Response = REXUS_Comm.communicate(Message)
        if Response == 'Test Mode':
            break
        if Response == 'T-10':
            PiCam_1.background_record_process('cam', cut_length=5)
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
