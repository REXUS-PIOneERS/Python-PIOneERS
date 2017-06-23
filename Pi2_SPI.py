import RPi_SPI as SPI
import RPi.GPIO as GPIO

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.INPUT, pull_up_down=GPIO.PUD_UP)

spi = SPI.SPI_Slave(16, 13, 14, 11)

GPIO.wait_for_edge(12, GPIO.RISING)

GPIO.cleanup()
