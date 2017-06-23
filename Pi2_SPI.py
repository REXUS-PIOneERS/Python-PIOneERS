from . import RPi_SPI as SPI
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.INPUT, pull_up_down=GPIO.PUD_UP)

spi = SPI.SPI_Slave(38, 37, 36, 35, freq=10)

GPIO.wait_for_edge(12, GPIO.RISING)

GPIO.cleanup()
