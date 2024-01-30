#!/usr/bin/env python3
import socket
# import matplotlib.pyplot as plt
import multiprocessing
from multiprocessing import Queue, Event
import tkinter as tk
from ast import literal_eval
import time
# import pickle
# import pyqtgraph as pg
# from pyqtgraph.Qt import QtCore, QtGui

import sys
# HOST = '192.168.1.150'  # The server's hostname or IP address
PORT = 9000  # The port used by the server
import argparse
def client_thread(queue, tkqueue, killevent, host_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(0.5)
        # s.connect((HOST, PORT))
        s.connect((host_ip, PORT))
        # s.connect((192.168.1.150, PORT))
        while not killevent.is_set():
            data = 0
            try:
                data = s.recv(4096)
            except:
                pass
            finally:
                pass
            if data:
                data = data.decode('utf-8')
                if data.count("[") > 1:
                    data_array = data.split("[")[1:-1]
                    for data_point in data_array:
                        data_list = literal_eval("[" + data_point)
                        if type(data) == type([1, 2]):
                            queue.put(data_list)
                else:
                    data = literal_eval(data)
                if type(data) == type([1, 2]):
                    queue.put(data)
            if not tkqueue.empty():
                y = str(tkqueue.get())

                print(y)
                # Encode String
                y = y.encode()
                print("sending")
                s.sendall(y)
    finally:
        s.sendall(str([-1, 0]).encode())
        time.sleep(1)
        s.close()
# class MainWindow(QtGui.QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.central_widget = QtGui.QStackedWidget()
#         self.setCentralWidget(self.central_widget)
#         self.login_widget = LoginWidget(self)
#         self.login_widget.button.clicked.connect(self.plotter)
#         self.central_widget.addWidget(self.login_widget)
#         self.time_data=[]
#         self.pos_data=[]
#
#     def plotter(self):
#         self.data =[0]
#         self.curve = self.login_widget.plot.getPlotItem().plot()
#
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.updater)
#         self.timer.start(0)
#
#     def updater(self, queue):
#         if not queue.empty():
#             # plt.gca().cla()  # optionally clear axes
#             data = queue.get()
#             while queue.qsize() > 5:
#                 data = queue.get()
#             self.pos_data.append(data[1])
#             self.time_data.append(data[0])
#             self.data.append(data[0],data[1])
#             self.curve.setData(self.data)
#
# class LoginWidget(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(LoginWidget, self).__init__(parent)
#         layout = QtGui.QHBoxLayout()
#         self.button = QtGui.QPushButton('Start Plotting')
#         layout.addWidget(self.button)
#         self.plot = pg.PlotWidget()
#         layout.addWidget(self.plot)
#         self.setLayout(layout)

# def plot_thread(queue, killevent):
#     plotWidget = pg.plot(title="RPS").plot
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()
#
#     try:
#         time_data = []
#         pos_data = []
#         title = "Frequency: tbd"
#         title2 = " Speed: tbd"
#         while not killevent.is_set():
#             if not queue.empty():
#                 # plt.gca().cla()  # optionally clear axes
#                 data = queue.get()
#                 while queue.qsize()>5:
#                     data = queue.get()
#                 pos_data.append(data[1])
#                 time_data.append(data[0])
#
#
#             if len(time_data) == 200:
#                 title = "Frequency: " + str(20 / (time_data[-1] - time_data[-20]))
#                 title2 = " Speed: " + str((pos_data[-1] - pos_data[-5]) / (time_data[-1] - time_data[-5]))
#                 # print(time_data[-1])
#             # plt.plot(time_data[-200:], pos_data[-200:], color="red")
#             # plt.title(title + title2)
#             # plt.draw()
#             plotWidget.setData(time_data, pos_data)
#             print(time_data[-1])
#             print("a")
#
#     finally:
#         with open(str(time.time()) + ".pickle", "wb") as fp:  # Pickling
#             pickle.dump([pos_data, time_data], fp)
#         plt.close()


def tk_thread(tkqueue, killevent,simple=False):
    master = tk.Tk()

    w1 = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=5, length=2000, width=80, sliderlength=80,
                  label="pos gain")
    w1.set(20)
    if not simple:
        w1.pack()
    w2 = tk.Scale(master, from_=0, to=0.5, orient=tk.HORIZONTAL, tickinterval=0.1, length=2000, width=80,
                  sliderlength=80,
                  resolution=0.01, label="vel gain")
    w2.set(0.3)
    if not simple:
        w2.pack()
    w3 = tk.Scale(master, from_=0, to=0.5, orient=tk.HORIZONTAL, tickinterval=0.1, length=2000, width=80,
                  sliderlength=80,
                  resolution=0.01, label="vel int gain")
    w3.set(0.15)
    if not simple:
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

    #send the default params first 
    put_to_queue(2)
    while not killevent.is_set():
        master.update_idletasks()
        master.update()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("python3 odrv_client.py")
    parser.add_argument("--simple", help="hide tuning controls", action="store_true",dest="simple")
    parser.add_argument("--ip", help="IP address of odrive server", type=str,default="192.168.1.150")
    parser.set_defaults(simple=False)
    args = parser.parse_args()
    queue = Queue()
    tkqueue = Queue()
    killsig = Queue(5)
    killevent = Event()
    # creating processes
    p1 = multiprocessing.Process(target=client_thread, args=(queue, tkqueue, killevent,args.ip,))
    # p2 = multiprocessing.Process(target=plot_thread, args=(queue, killevent,))
    p3 = multiprocessing.Process(target=tk_thread, args=(tkqueue, killevent,args.simple))

    # starting process 1
    p1.start()
    # starting process 2
    #p2.start()
    # starting process 3
    p3.start()
    # while killsig.empty():
    #     time.sleep(0.1)
    # p1.terminate()
    # p2.terminate()
    # p3.terminate()
    # app = QtGui.QApplication([])
    # window = MainWindow(queue)
    # window.show()
    # app.exec_()