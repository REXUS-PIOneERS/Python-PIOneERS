"""
Program for controlling the IMU connected to Pi_1
"""

import smbus
from LSM9DS0 import *
import multiprocessing


class IMU():
    '''
    Class for controlling the BerryIMU gyroscope, accelerometer and
    magnetometer.

    Before reading data each sensor must be setup either with default values
    by calling self.setup_default or with any other values desired by calling
    the self.writeReg command. For more details on the various options
    available see the documentation at:
        http://ozzmaker.com/wp-content/uploads/2014/12/LSM9DS0.pdf
    The registers of importance are:
        CTRL_REG1_XM and CTRL_REG2_XM for the accelerometer
        CTRL_REG5_XM, CTRL_REG6_XM and CTRL_REG7_XM for the magnetometer
        CTRL_REG1_G and CTRL_REG2_G for the gyro

    Values can be read from each axis individually via the readAccAxis/
    readGryAxis/readMagAxis respectively with the values 0,1 and 2
    representing the x, y and z axis respectively.
    Values can also be read from all three axes simultaneously using the
    corresponding readAcc, readGry and ReadMag commands
    '''
    def __enter__(self):
        self.__init__()

    def __init__(self):
        '''Setup the bus for the IMU'''
        self.bus = smbus.SMBus(1)
        self._processes = []

    def __exit__(self):
        '''Reset all registers and close the bus'''
        self.reset_registers()
        self.bus.close()


    def reset_registers(self):
        '''
        Reset all registers for the accelerometer, gyro and magnetometer to
        zero
        '''
        self.writeReg(ACC_ADDRESS, CTRL_REG1_XM, 0)
        self.writeReg(ACC_ADDRESS, CTRL_REG2_XM, 0)
        self.writeReg(MAG_ADDRESS, CTRL_REG5_XM, 0)
        self.writeReg(MAG_ADDRESS, CTRL_REG6_XM, 0)
        self.writeReg(MAG_ADDRESS, CTRL_REG7_XM, 0)
        self.writeReg(GYR_ADDRESS, CTRL_REG1_G, 0)
        self.writeReg(GYR_ADDRESS, CTRL_REG4_G, 0)

    def setup_default(self):
        '''
        Setup the default values to activate the gyro, magnetometer and
        accelerometer
        '''
        # Initialise accelerometer
        self.writeReg(ACC_ADDRESS, CTRL_REG1_XM, 0b01100111)
        self.writeReg(ACC_ADDRESS, CTRL_REG2_XM, 0b00100000)
        # Initialise the magnetometer
        self.writeReg(MAG_ADDRESS, CTRL_REG5_XM, 0b11110000)
        self.writeReg(MAG_ADDRESS, CTRL_REG6_XM, 0b01100000)
        self.writeReg(MAG_ADDRESS, CTRL_REG7_XM, 0b00000000)
        # Initialise the gyroscope
        self.writeReg(GYR_ADDRESS, CTRL_REG1_G, 0b00001111)
        self.writeReg(GYR_ADDRESS, CTRL_REG4_G, 0b00110000)

    def writeReg(self, address, register,value):
        '''Used to write values to various addresses for setting up the IMU'''
        self.bus.write_byte_data(address, register, value)
        return -1

    def readAccAxis(self, axis):
        '''Axis should be 0,1 or 2 (0=>x,1=>y,2=>z)'''
        # Check which axis we are using to make measurements
        if axis == 0:
            register_l = OUT_X_L_A
            register_h = OUT_X_H_A
        elif axis == 1:
            register_l = OUT_Y_L_A
            register_h = OUT_Y_H_A
        elif axis == 2:
            register_l = OUT_Z_L_A
            register_h = OUT_Z_H_A
        else:
            raise ValueError(
                    'Expected axis to be 0,1 or 2 corresponding to x,y,z')
        # Get the values from the register
        acc_l = self.bus.read_byte_data(ACC_ADDRESS, register_l)
        acc_h = self.bus.read_byte_data(ACC_ADDRESS, register_h)
        acc_combined = (acc_l | acc_h << 8)
        # Return the acceleration value (accounting for positive and negative acceleration)
        return acc_combined if acc_combined < 32768 else acc_combined - 65536

    def readMagAxis(self, axis):
        '''Axis should be 0,1 or 2 (0=>x,1=>y,2=>z)'''
        # Check which axis we are using to make measurements
        if axis == 0:
            register_l = OUT_X_L_M
            register_h = OUT_X_H_M
        elif axis == 1:
            register_l = OUT_Y_L_M
            register_h = OUT_Y_H_M
        elif axis == 2:
            register_l = OUT_Z_L_M
            register_h = OUT_Z_H_M
        else:
            raise ValueError(
                    'Expected axis to be 0,1 or 2 corresponding to x,y,z')
        # Get the values from the register
        mag_l = self.bus.read_byte_data(MAG_ADDRESS, register_l)
        mag_h = self.bus.read_byte_data(MAG_ADDRESS, register_h)
        mag_combined = (mag_l | mag_h << 8)
        # Return the acceleration value (accounting for positive and negative acceleration)
        return mag_combined if mag_combined < 32768 else mag_combined - 65536

    def readGyrAxis(self, axis):
        '''Axis should be 0,1 or 2 (0=>x,1=>y,2=>z)'''
        # Check which axis we are using to make measurements
        if axis == 0:
            register_l = OUT_X_L_G
            register_h = OUT_X_H_G
        elif axis == 1:
            register_l = OUT_Y_L_G
            register_h = OUT_Y_H_G
        elif axis == 2:
            register_l = OUT_Z_L_G
            register_h = OUT_Z_H_G
        else:
            raise ValueError(
                    'Expected axis to be 0,1 or 2 corresponding to x,y,z')
        # Get the values from the register
        gyr_l = self.bus.read_byte_data(GYR_ADDRESS, register_l)
        gyr_h = self.bus.read_byte_data(GYR_ADDRESS, register_h)
        gyr_combined = (gyr_l | gyr_h << 8)
        # Return the acceleration value
        return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536

    def readAcc(self):
        '''
        Reads all data from the accelerometer and returns the results as a
        dictionary with the keys x, y and z
        '''
        return {'x': self.readAccAxis(0),
                'y': self.readAccAxis(1),
                'z': self.readAccAxis(2)}

    def readGyr(self):
        '''
        Reads all data from the gyro and returns the results as a
        dictionary with the keys x, y and z
        '''
        return {'x': self.readGyrAxis(0),
                'y': self.readGyrAxis(1),
                'z': self.readGyrAxis(2)}

    def readMag(self):
        '''
        Reads all data from the accelerometer and returns the results as a
        dictionary with the keys x, y and z
        '''
        return {'x': self.readMagAxis(0),
                'y': self.readMagAxis(1),
                'z': self.readMagAxis(2)}

    def take_measurements_process(self, freq, file):
        '''
        Generates a python process for taking measurements with the IMU.
        '''
        exit_flag = multiprocessing.Value('i', 0)
        p = multiprocessing.Process(target=self.take_measurements,
                                    args=(freq, file, exit_flag))
        self._processes.append(p)
        self._flags.append(exit_flag)
        p.start()
        return True

    def end_measurements_processes(self):
        '''
        End all active processes taking measurements
        '''
        for flag in self._flags:
            with flag.get_lock():
                flag = 1

        for i, process in enumerate(self._processes):
            process.join()
            print('Process {} joined'.format(i))



    def take_measurements(self, freq, file, exit_flag):
        '''
        Reads from all activated sensors at the specified frequency and saves
        to the location in save_file for seconds denoted by time.
        '''
        while not exit_flag:
            print('Taking Measurements')
            time.sleep(0.5)
