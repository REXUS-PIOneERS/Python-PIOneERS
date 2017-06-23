import RPi_SPI as SPI
import RPi.GPIO as GPIO

GPIO.cleanup()

spi = SPI.SPI_Master(38, 37, 36, 35, freq=2)

print("Sending 10 to channel 1")
spi.send_data(1, 10, 8)

x = spi.request_data(1, 8)

print("Recieved {} from channel 1".format(x))

GPIO.cleanup()
