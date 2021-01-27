#!/usr/bin/env python3
import odrive
from odrive.enums import *
from fibre import Logger, Event
import tkinter as tk
from time import sleep, time
import multiprocessing
from multiprocessing import Queue
import pickle

def ping_thread(queue, tkqueue, killevent):
    try:
        od = odrive.find_any()
        axis = od.axis1
        data=[]
        # wait for odrive to finish calibration
        while axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            sleep(1)

        axis.controller.config.vel_limit = 6

        axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        axis.controller.config.vel_ramp_rate = 2
        axis.controller.config.input_mode = INPUT_MODE_VEL_RAMP
        axis.controller.input_vel = 0
        ref_time = time()
        ref_time=0
        running = False
        while not killevent.is_set():
            if not tkqueue.empty():
                params = tkqueue.get()
                print(params)
                if params[0] == 0:
                    # start spinning
                    print("spinning at ",params[1])
                    axis.controller.input_vel = params[1]
                    running = True
                elif params[0] == 1:
                    # stop program
                    print("stopping")
                    axis.controller.input_vel = 0
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
                # queue.put([time()-ref_time,vel_est])
                data.append([time()-ref_time,vel_est])
            #print("sleeping")
            sleep(1)
            #print("slept")
    finally:
        with open(str(time()) + ".pickle", "wb") as fp:  # Pickling
            pickle.dump(data, fp)


def tk_thread(tkqueue, killevent):
    master = tk.Tk()

    w1 = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=5, length=2000, width=80, sliderlength=80,
                  label="pos gain")
    w1.set(1)
    w1.pack()
    w2 = tk.Scale(master, from_=0, to=0.5, orient=tk.HORIZONTAL, tickinterval=0.1, length=2000, width=80,
                  sliderlength=80,
                  resolution=0.01, label="vel gain")
    w2.set(0.1)
    w2.pack()
    w3 = tk.Scale(master, from_=0, to=0.5, orient=tk.HORIZONTAL, tickinterval=0.1, length=2000, width=80,
                  sliderlength=80,
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

    B1 = tk.Button(master, text="1", command=lambda: velCallBack(1), width=4, height=2)
    B1.pack(in_=bar, side=tk.LEFT)

    B3 = tk.Button(master, text="3", command=lambda: velCallBack(3), width=4, height=2)
    B3.pack(in_=bar, side=tk.LEFT)

    B5 = tk.Button(master, text="5", command=lambda: velCallBack(5), width=4, height=2)
    B5.pack(in_=bar, side=tk.LEFT)

    bar2 = tk.Frame(master)
    bar2.pack(side=tk.TOP)

    def put_to_queue(value):
        tkqueue.put([value, w4.get(), w1.get(), w2.get(), w3.get()])

    B_start = tk.Button(master, text="Start / Update speed", command=lambda: put_to_queue(0), width=14, height=2)
    B_start.pack(in_=bar2, side=tk.LEFT)

    B_stop = tk.Button(master, text="Stop", command=lambda: put_to_queue(1), width=4, height=2)
    B_stop.pack(in_=bar2, side=tk.LEFT)

    B_param_upload = tk.Button(master, text="Param upload", command=lambda: put_to_queue(2), width=10, height=2)
    B_param_upload.pack(in_=bar2, side=tk.LEFT)

    B_exit = tk.Button(master, text="Exit", command=lambda: killevent.set(), width=4, height=2)
    B_exit.pack(in_=bar2, side=tk.LEFT)

    while not killevent.is_set():
        master.update_idletasks()
        master.update()


if __name__ == "__main__":
    queue = Queue()
    tkqueue = Queue()
    killevent = Event()

    # creating processes
    p1 = multiprocessing.Process(target=tk_thread, args=(tkqueue, killevent,))
    p2 = multiprocessing.Process(target=ping_thread, args=(queue, tkqueue, killevent,))

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()

    p1.join()
    p2.join()