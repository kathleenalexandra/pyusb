#!/usr/bin/python

import datetime as dt

import numpy as np

import SensorTile_Serial

import sys



#  Serial setup according to command line arguments

python_version = sys.version[0]

if len(sys.argv) != 2:

    print ("Wrong Number of Arguments!")

    print ("Please use format: python SensorTile_Animation_args.py SerialAddress")

else:

    address = sys.argv[1]

    if python_version == "2":

        python3 = False

    else:

        python3 = True



baud_rate = 9600

timeout = 2



# Create figure for plotting


sensortile = SensorTile_Serial.serial_SensorTile(address, baud_rate, timeout, python3)

sensortile.init_connection()


while 1:
    dis_list, accel_list = sensortile.collect_data()
    



sensortile.close_connection()