import RPi_SPI as SPI
import RPi.GPIO as GPIO

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

spi = SPI.SPI_Slave(18, 15, 16, 13)

GPIO.wait_for_edge(12, GPIO.RISING)

GPIO.cleanup()
