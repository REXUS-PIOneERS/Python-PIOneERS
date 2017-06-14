"""
Program for controlling the IMU connected to Pi_1
"""

import smbus
import timeit
from LSM9DSO import *
import datetime

class IMU():
    
    def __init__(self):
        #Setup the bus for the IMU
        self.bus = smbus.SMBus(1)
        
    def setup_default(self):
        '''Setup the default values to activate the gyro, magnetometer and accelerometer'''
        #Initialise accelerometer
        self.writeReg(ACC_ADDRESS, CTRL_REG1_XM, 0b01100111)
        self.writeReg(ACC_ADDRESS, CTRL_REG2_XM, 0b00100000)
        #Initialise the magnetometer
        self.writeReg(MAG_ADDRESS, CTRL_REG5_XM, 0b11110000)
        self.writeReg(MAG_ADDRESS, CTRL_REG6_XM, 0b01100000)
        self.writeReg(MAG_ADDRESS, CTRL_REG7_XM, 0b00000000)
        #Initialise the gyroscope
        self.writeReg(GYR_ADDRESS, CTRL_REG1_G, 0b00001111)
        self.writeReg(GYR_ADDRESS, CTRL_REG4_G, 0b00110000)
        
    def writeReg(self,address,register,value):
        '''Used to write values to various addresses for setting up the IMU'''
        self.bus.write_byte_data(address, register, value)
        return -1
    
    def readAccAxis(self,axis):
        '''Axis should be 0,1 or 2 (0=>x,1=>y,2=>z)'''
        #Check which axis we are using to make measurements
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
            raise ValueError('Expected axis to be 0,1 or 2 corresponding to x,y,z')
        #Get the values from the register
        acc_l = self.bus.read_byte_data(ACC_ADDRESS, register_l)
        acc_h = self.bus.read_byte_data(ACC_ADDRESS, register_h)
        acc_combined = (acc_l | acc_h << 8)
        #Return the acceleration value (accounting for positive and negative acceleration)
        return acc_combined if acc_combined < 32768 else acc_combined - 65536
    
    def readMagAxis(self,axis):
        '''Axis should be 0,1 or 2 (0=>x,1=>y,2=>z)'''
        #Check which axis we are using to make measurements
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
            raise ValueError('Expected axis to be 0,1 or 2 corresponding to x,y,z')
        #Get the values from the register
        mag_l = self.bus.read_byte_data(MAG_ADDRESS, register_l)
        mag_h = self.bus.read_byte_data(MAG_ADDRESS, register_h)
        mag_combined = (mag_l | mag_h << 8)
        #Return the acceleration value (accounting for positive and negative acceleration)
        return mag_combined if mag_combined < 32768 else mag_combined - 65536

    def readGyrAxis(self,axis):
        '''Axis should be 0,1 or 2 (0=>x,1=>y,2=>z)'''
        #Check which axis we are using to make measurements
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
            raise ValueError('Expected axis to be 0,1 or 2 corresponding to x,y,z')
        #Get the values from the register
        gyr_l = self.bus.read_byte_data(GYR_ADDRESS, register_l)
        gyr_h = self.bus.read_byte_data(GYR_ADDRESS, register_h)
        gyr_combined = (gyr_l | gyr_h << 8)
        #Return the acceleration value (accounting for positive and negative acceleration)
        return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536