#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
from time import sleep
from math import sin
import math
from fibre import Logger, Event
from odrive.utils import OperationAbortedException
from fibre.protocol import ChannelBrokenException
import sys
import tkinter as tk

print("a")
od = odrive.find_any()
axis = od.axis1
mo = axis.motor
enc = axis.encoder

# wait for odrive to finish calibration
while axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
    sleep(1)

axis.controller.config.vel_limit = 6

axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
axis.controller.config.vel_ramp_rate = 2
axis.controller.config.input_mode = INPUT_MODE_VEL_RAMP
# axis.controller.input_vel = 5
# while axis.encoder.vel_estimate <4:
#     sleep(1)
# plot the velocity
# cancellation_token = start_liveplotter(lambda:[axis.encoder.vel_estimate, axis.controller.input_vel])
# print("Showing plot. Press Ctrl+C to exit.")
# for i in range(1,1000):
#     axis.controller.input_vel = 5+sin(i/100)
#     sleep(0.01)
#
axis.controller.input_vel = 0

master = tk.Tk()

w1 = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=5, length=2000, width=80, sliderlength=80,
              label="pos gain")
w1.set(1)
w1.pack()
w2 = tk.Scale(master, from_=0, to=0.5, orient=tk.HORIZONTAL, tickinterval=0.1, length=2000, width=80, sliderlength=80,
              resolution=0.01, label="vel gain")
w2.set(0.1)
w2.pack()
w3 = tk.Scale(master, from_=0, to=0.5, orient=tk.HORIZONTAL, tickinterval=0.1, length=2000, width=80, sliderlength=80,
              resolution=0.01, label="vel int gain")
w3.set(0.1)
w3.pack()
w4 = tk.Scale(master, from_=0, to=5, orient=tk.HORIZONTAL, tickinterval=1, length=2000, width=80, sliderlength=80,
              resolution=0.2, label="velocity")
w4.set(0)
w4.pack()

# create the main sections of the layout,
# and lay them out
bar = tk.Frame(master)
bar.pack(side=tk.TOP)


def velCallBack(value):
    w4.set(value)


B0 = tk.Button(master, text="0", command=lambda: velCallBack(0), width=4, height=2)
B0.pack(in_=bar, side=tk.LEFT)

B1 = tk.Button(master, text="1", command=lambda: velCallBack(0), width=4, height=2)
B1.pack(in_=bar, side=tk.LEFT)

B3 = tk.Button(master, text="3", command=lambda: velCallBack(0), width=4, height=2)
B3.pack(in_=bar, side=tk.LEFT)

B5 = tk.Button(master, text="5", command=lambda: velCallBack(0), width=4, height=2)
B5.pack(in_=bar, side=tk.LEFT)

while True:
    axis.controller.input_vel = w4.get()
    axis.controller.config.pos_gain = w1.get()
    axis.controller.config.vel_gain = w2.get()
    axis.controller.config.vel_integrator_gain = w3.get()
    master.update_idletasks()
    master.update()
    time.sleep(0.1)

# #circular control
# axis.controller.config.pos_gain = 20
# axis.controller.config.vel_gain = 0.6
# axis.controller.config.vel_integrator_gain = 0.32
#
# cancellation_token = start_liveplotter(lambda:[axis.encoder.pos_circular, axis.controller.pos_setpoint])
# axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
#
# #axis.controller.config.input_filter_bandwidth = 2.0
# #axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
# #axis.controller.config.circular_setpoints = True
# axis.controller.input_pos=0.1
#
#
# while not cancellation_token.is_set():
#     axis.controller.config.pos_gain = w1.get()
#     axis.controller.config.vel_gain = w2.get()
#     axis.controller.config.vel_integrator_gain = w3.get()
#     tk.update_idletasks()
#     tk.update()
#     time.sleep(0.1)
