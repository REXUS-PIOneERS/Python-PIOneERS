"""
Program for controlling the IMU connected to Pi_1
"""

import datetime
from IMU import IMU

import time

def take_measurements(n):
    '''Takes n measurements of gyro, acc and mag'''
    imu = IMU()
    imu.setup_default()
    for i in range(0,n):
        for j in range(0,3):
            print('Acc', imu.readAccAxis(j))
            print('Gyr', imu.readGyrAxis(j))
            print('Mag', imu.readMagAxis(j))
            time.sleep(0.5)
            
