# prototype for "bitwise" SPI transmission
# for use on raspberry pi
# as part of the rexus project


# imports
import RPi.GPIO as GPIO
import time
import sys

# select pins for SPI
# "Chip select" is probably not needed as this is only for a single device (i think)

CLK = 18  # clock
MISO = 23  # Master in Slave out, used to transmit FROM the Slave device
MOSI = 24  # Master out Slave in, used to transmit FROM the Master device
CS = 25  # Chip select


def setupSpiPinsMaster(clkPin, misoPin, mosiPin, csPin):
    # used on the master device to set up pins
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(misoPin, GPIO.IN)  # note this is an input
    GPIO.setup(mosiPin, GPIO.OUT)
    GPIO.setup(csPin, GPIO.OUT)


def setupSpiPinsSlave(clkPin, misoPin, mosiPin, csPin):
    # used on the slave device to set up pins
    GPIO.setup(clkPin, GPIO.IN)
    GPIO.setup(misoPin, GPIO.OUT)  # note this is now an ouput
    GPIO.setup(mosiPin, GPIO.IN)
    GPIO.setup(csPin, GPIO.IN)


def readFromSlave(channel, clkPin, misoPin, mosiPin, csPin):
    # read an input from the slave device to the master
    if (channel < 0) or (channel > 7):
        # test for channels in valid range assuming 8 channel SPI
        print "Invalid SPI channel number, must be in range [0, 7]"
        return -1

    # pull CS pin high between conversations, apparently this is common for some devices
    GPIO.output(csPin, GPIO.HIGH)

    # start read with clock and CS low
    GPIO.output(csPin, GPIO.LOW)
    GPIO.output(clkPin, GPIO.LOW)

    # read command is:
    # start bit = 1
    # single-ended comparison = 1
    # channel num bit 2
    # channel num bit 1
    # channel num bit 0 (LSB)
    read_command = 0x18
    read_command |= channel

    sendBitsFromMaster(read_command, 5, clkPin, mosiPin)

    # note that the 12 here is the number of bits that are expected and this should be changed accoring to the data being recieved


    slaveValue = recvBitsFromSlave(12, clkPin, misoPin)

    # set CS high to end the read
    GPIO.output(csPin, GPIO.HIGH)


def sendBitsFromMaster(data, numBits, clkPin, mosiPin):
    # read all the bits from the data and push over the line
    for bit in range(numBits, 0, -1):  # count down from MSB to LSB
        bit = bit - 1
        dec_value = 2 ** bit

        if (data / dec_value >= 1):
            GPIO.ouput(mosiPin, GPIO.HIGH)
            data = data - dec_value

        else:
            GPIO.output(mosiPin, GPIO.LOW)

        # pulse the clock pin to push the data through
        GPIO.output(clkPin, GPIO.HIGH)
        #POSSIBLE NEED FOR SHORT DELAY
        GPIO.output(clkPin, GPIO.LOW)

def recvBitsFromSlave(numBits, clkPin, misoPin):
    retVal = 0

    for bit in range(numBits):
        #read in a single bit of data
        if GPIO.input(misoPin):
            retVal |= 0x1

        #pulse clock pin
        GPIO.output(clkPin, GPIO.HIGH)
        #POSSIBLE NEED FOR SHORT DELAY
        GPIO.output(clkPin, GPIO.LOW)

        #advance input to next bit
        retVal <<= 1


    return retVal


def sendBitsFromSlave(data, numBits, clkPin, misoPin):
    # read all the bits from the data and push over the line
    bit = numBits - 1
    while (bit >= 0):
        dec_value = 2 ** bit
        if (data/dec_value >= 1):
            GPIO.output(misoPin, GPIO.HIGH)
            data = data - dec_value
        else:
            GPIO.output(misoPin, GPIO.LOW)

        while (not(GPIO.input(clkPin))):
            pass
            #do nothing, this stalls the processor, maybe theres a better way to do this?
            #once the clock goes high again it can continue

        bit = bit - 1

    return


def recvBitsFromMaster(numBits, clkPin, mosiPin):
    retVal = 0

    for bit in range(numBits):
        while (not(GPIO.input(clkPin))):
            pass
            #do nothing
            #stalls the processor

        if GPIO.input(mosiPin):
            retVal |= 0x1

        #advance to next bit
            retVal <<= 1

    return retVal
