import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)


class SPI_Master():

    def __init__(self, CLK, MISO, MOSI, CS, freq=1000):
        self.CLK = CLK          # Clock
        self.MISO = MISO        # Master out, slave in
        self. MOSI = MOSI       # Master in, slave out
        self.CS = CS            # Chip Select
        GPIO.setup(self.CLK, GPIO.OUT)
        GPIO.setup(self.MOSI, GPIO.OUT)
        GPIO.setup(self.MISO, GPIO.IN)
        GPIO.setup(self.CS, GPIO.OUT)
        self.freq = freq
        # Activate the SPI line
        self.activate_spi_line()

    def activate_spi_line(self):
        '''Pull all lines high'''
        GPIO.output(self.CLK, GPIO.HIGH)
        GPIO.output(self.MOSI, GPIO.HIGH)
        GPIO.output(self.CS, GPIO.HIGH)

    def send_data(self, channel, data, num_bits):
        '''
        Send data to the slave device

        Structure of command
        Bit 8: 1 = recieve, 0 = send  (MSB)
        Bit 5-7: Channel of send/recieve
        Bit 1-4: Number of bits to read/write (LSB)
        Command, Channel, Bits
        '''
        command = (0b1 << 7 | channel << 4 | num_bits)
        print("sending command:", bin(command))
        # Pull CS Low to prepare for recieving command
        GPIO.output(self.CS, GPIO.HIGH)
        GPIO.output(self.CS, GPIO.LOW)
        # Wait for acknoweldge from Slave
        time.sleep(0.1)
        self._sendBitsFromMaster(command, 8)
        # Sleep for a bit to give the slave time to prepare
        # time.sleep(0.1)
        # Send the data
        self._sendBitsFromMaster(data, num_bits)
        # Pull CS High to signal end of communication
        GPIO.output(self.CS, GPIO.HIGH)

    def request_data(self, channel, num_bits):
        '''
        Request data from the slave device
        Structure of command
        Bit 8: 1 = recieve, 0 = send  (MSB)
        Bit 5-7: Channel of send/recieve
        Bit 1-4: Number of bits to read/write (LSB)
        Command, Channel, Bits
        '''
        command = (0b0 << 7 | channel << 4 | num_bits)
        # Pull CS Low to prepare for recieving command
        GPIO.output(self.CS, GPIO.HIGH)
        GPIO.output(self.CS, GPIO.LOW)
        time.sleep(0.1)
        self._sendBitsFromMaster(command, 8)
        # Sleep to give slave time to respond
        # time.sleep(0.1)
        # Recieve the data
        GPIO.output(self.CS, GPIO.HIGH)
        return self._recvBitsFromSlave(num_bits)

    def _sendBitsFromMaster(self, data, num_bits):
        '''Send bits to the slave device'''
        print("Sending bits...",bin(data))
        for bit in range(num_bits, 0, -1):
            bit -= 1
            dec_value = 2 ** bit
            if (data/dec_value >= 1):
                print("sent bit: 1")
                GPIO.output(self.MOSI, GPIO.HIGH)
                data -= dec_value
            else:
                print("sent bit: 0")
                GPIO.output(self.MOSI, GPIO.LOW)
            # Pulse the clock pin to push data through
            time.sleep(0.5/self.freq)
            GPIO.output(self.CLK, GPIO.LOW)
            GPIO.output(self.CLK, GPIO.HIGH)
            time.sleep(0.5/self.freq)

    def _recvBitsFromSlave(self, num_bits):
        '''Get data from the salve'''
        data = 0

        for bit in range(num_bits):
            # Pulse the clock to start recieving data
            time.sleep(0.5/self.freq)
            GPIO.output(self.CLK, GPIO.LOW)
            GPIO.output(self.CLK, GPIO.HIGH)
            time.sleep(0.5/self.freq)  # Give the slave time to respond
            if GPIO.input(self.MISO):
                data |= 0b1
            data <<= 1
        data >>= 1
        return data


class SPI_Slave():

    def __init__(self, CLK, MISO, MOSI, CS):
        # Setup Pins
        self.CLK = CLK
        self.MISO = MISO
        self.MOSI = MOSI
        self.CS = CS
        GPIO.setup(self.CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.MOSI, GPIO.IN)
        GPIO.setup(self.MISO, GPIO.OUT)
        GPIO.setup(self.CS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Setup data registers
        self.channels = [0 for i in range(7)]
        # Activate spi connection
        self.activate_spi_line()

    def activate_spi_line(self):
        '''Pull output pins high, setup detect for CS'''
        GPIO.output(self.MISO, GPIO.HIGH)
        GPIO.add_event_detect(self.CS,
                              GPIO.FALLING,
                              callback=self.recieve_command)
        print("Event detection added")

    def recieve_command(self, channel):
        '''Reads data from the master to recieve the command (8-bit)'''
        GPIO.output(self.MISO, GPIO.LOW)
        command = self._readBitsFromMaster(8)
        print("Command recieved:", bin(command))
        '''
        Structure of command
        Bit 8: 1 = recieve, 0 = send  (MSB)
        Bit 5-7: Channel of send/recieve
        Bit 1-4: Number of bits to read/write (LSB)
        '''
        recieve = (command & 0b10000000) >> 7
        channel = (command & 0b01110000) >> 4
        num_bits = command & 0b00001111
        print(recieve, channel, num_bits)
        if recieve:
            self._recieve_data(channel, num_bits)
        else:
            self._send_data(channel, num_bits)

    def _readBitsFromMaster(self, num_bits):
        '''Reads bits from the master'''
        print("Waiting for bits")
        data = 0
        for bit in range(num_bits):
            # Wait for the clock to pulse
            GPIO.wait_for_edge(self.CLK, GPIO.FALLING)
            if GPIO.input(self.MOSI):
                print("Recieved bit:", 1)
                data |= 0b1
            else:
                print("Recieved bit:", 0)
            data <<= 1

        data >>= 1
        return data

    def _recieve_data(self, channel, num_bits):
        '''Recieve the data and store in the channel'''
        if 0 > channel or channel > 7:
            print('Recieve: Invalid SPI channel number, must be in range 0-7', channel)
            return
        # Read the data
        self.channels[channel] = self._readBitsFromMaster(num_bits)

    def _send_data(self, channel, num_bits):
        '''Send the data from the channel'''
        if 0 > channel or channel > 7:
            print('Send: Invalid SPI channel number, must be in range 0-7', channel)
        # Send the data
        self._sendBitsFromSlave(self.channels[channel], num_bits)

    def _sendBitsFromSlave(self, data, num_bits):
        '''Sends the data to the Master'''
        # Send data starting with the MSB
        for bit in range(num_bits, 0, -1):
            bit -= 1
            dec_value = 2 ** bit
            # Wait for the clock to pulse
            GPIO.wait_for_edge(self.CLK, GPIO.FALLING)
            if data/dec_value >= 1:
                GPIO.output(self.MISO, GPIO.HIGH)
                data -= dec_value
            else:
                GPIO.output(self.MISO, GPIO.LOW)
