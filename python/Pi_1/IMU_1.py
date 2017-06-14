"""
Program for controlling the IMU connected to Pi_1
"""

from IMU import IMU

import time

def take_measurements(n):
    '''Takes n measurements of gyro, acc and mag'''
    imu = IMU()
    imu.setup_default()
    for i in range(0,n):
        for j in range(0,3):
            print('Acc', j, imu.readAccAxis(j))
            print('Gyr', j, imu.readGyrAxis(j))
            print('Mag', j, imu.readMagAxis(j))
        time.sleep(0.5)
            