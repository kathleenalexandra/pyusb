#!/usr/bin/python

import datetime as dt

import matplotlib; matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

import matplotlib.animation as animation

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

fig = plt.figure()

ax1 = fig.add_subplot(211)

plt.title('SensorTile Project')

ax2 = fig.add_subplot(212)

ax1.set(ylabel='Displacement (mm)')

ax2.set(ylabel='Acceleration (mg)')



# plot parameters

x_len = 200

dis_range = [-100, 100]

accel_range = [-450, 450]

xs = list(range(0, 200))

ys1 = [0] * x_len

ys2 = [0] * x_len



ax1.set_ylim(dis_range)

line1, = ax1.plot(xs, ys1, animated=True)

ax2.set_ylim(accel_range)

line2, = ax2.plot(xs, ys2, animated=True)



# serial initialization

sensortile = SensorTile_Serial.serial_SensorTile(address, baud_rate, timeout, python3)

sensortile.init_connection()



# This function is called periodically from FuncAnimation

# def animate(i, xs, ys):

def animate(i, ys1, ys2):



    # get displacement, acceleration

    dis_list, accel_list = sensortile.collect_data()



    # Add dis and accel to lists

    ys1.extend(dis_list)

    ys2.extend(accel_list)



    # Limit x and y lists to 200 samples - 2s 

    ys1 = ys1[-x_len:]

    ys2 = ys2[-x_len:]



    # Draw dis and accel lists

    line1.set_ydata(ys1)

    line2.set_ydata(ys2)



    return line1, line2,





# Set up plot to call animate() function periodically

# interval = 10ms

ani = animation.FuncAnimation(fig, animate, fargs=(ys1, ys2,), interval=3, blit=True)

plt.show()



# shutdown the system after closing the plot

sensortile.close_connection()