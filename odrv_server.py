#!/usr/bin/env python3
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

from time import sleep, time
import multiprocessing
from multiprocessing import Queue
import socket
import select
from ast import literal_eval
import argparse

# get IP address of machine
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
s.close()
PORT = 9000  # Port to listen on (non-privileged ports are > 1023)



def server_thread(queue, tkqueue,ip=""):
    if ip=="":
        ip=HOST
    try:
        while True:
            s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((ip, PORT))
            print("hostname is ",ip)
            s.listen()
            conn, addr = s.accept()
            conn.settimeout(0.5)
            print('Connected by', addr)
            while True:
                if not queue.empty():
                    y = str(queue.get())
                    y = y.encode()
                    conn.sendall(y)
                data = 0
                ready = select.select([conn], [], [], 0.001)
                if ready[0]:
                    data = conn.recv(4096)
                if data:
                    data = data.decode('utf-8')
                    print("data obtained", data)
                    print(type(data), type([1, 2]))
                    data = literal_eval(data)
                    if type(data) == type([1, 2]):
                        print("list obtained")
                        if data[0] == -1:
                            print("connection closed!")
                            conn.close()
                            break
                        tkqueue.put(data)
                        print("inserted",data)
            s.close()
            print("Restarting")
            sleep(3)
    except:
        print("error")
    finally:
        s.close()


def ping_thread(queue, tkqueue):
    try:
        od = odrive.find_any()
        axis = od.axis0

        # # wait for odrive to finish calibration
        # while axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
        #     sleep(1)

        axis.controller.config.vel_limit = 6

        axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        axis.controller.config.vel_ramp_rate = 2
        axis.controller.config.input_mode = INPUT_MODE_VEL_RAMP
        axis.controller.input_vel = 0
        ref_time = time()
        ref_time=0
        running = False
        while True:
            # print("a")
            #print(tkqueue.empty())
            if not tkqueue.empty():
                params = tkqueue.get()
                print(params)
                if params[0] == 0:
                    # start spinning
                    axis.requested_state =8
                    print("spinning at ",params[1])
                    axis.controller.input_vel = params[1]
                    running = True
                elif params[0] == 1:
                    # stop program
                    print("stopping")
                    axis.controller.input_vel = 0
                    axis.requested_state =1
                    running = False
                elif params[0] == 2:
                    # set params
                    # axis.controller.input_vel = params[2]
                    print("setting params")
                    axis.controller.config.pos_gain = params[2]
                    axis.controller.config.vel_gain = params[3]
                    axis.controller.config.vel_integrator_gain = params[4]
            if running:
                #print("putting")
                #vel_est=1
                vel_est=axis.encoder.vel_estimate
                print(vel_est)
                queue.put([time()-ref_time,vel_est])
            #print("sleeping")
            sleep(1)
            #print("slept")
    finally:
        pass


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("python3 odrv_client.py")
    parser.add_argument("--ip", help="IP address of odrive server", type=str,default="100.74.220.98")
    parser.set_defaults(simple=False)
    args = parser.parse_args()

    queue = Queue()
    tkqueue = Queue()


    # creating processes
    p1 = multiprocessing.Process(target=server_thread, args=(queue, tkqueue,args.ip))
    p2 = multiprocessing.Process(target=ping_thread, args=(queue, tkqueue,))

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()
