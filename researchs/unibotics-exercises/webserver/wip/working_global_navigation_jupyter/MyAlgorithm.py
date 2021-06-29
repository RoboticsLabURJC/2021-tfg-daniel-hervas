#! usr/bin/env python
# -*- coding: utf-8 -*-

from sensors import sensor
import numpy as np
import cv2
import math

import threading
import time
from datetime import datetime

time_cycle = 80

class MyAlgorithm(threading.Thread):

    def __init__(self, grid, sensor, vel, parent):
        self.sensor = sensor
        self.grid = grid
        self.vel = vel
        self.parent = parent
        self.started = False
        self.initiallized = False

        self.stop_event = threading.Event()
        self.stop_event.set()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)


    def run (self):

        while (not self.kill_event.is_set()):

            self.stop_event.wait()
            
            start_time = datetime.now()

            self.algorithm()
            self.parent.paintRobot()
                        
            finish_Time = datetime.now()

            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.stop_event.set()

    def play (self):
        self.stop_event.set()
        if not self.started:
          self.start()
          self.started = True

    def kill (self):
        self.kill_event.set()

    def absolutas2relativas(self, x, y, rx, ry, rt):
        # Convert to relatives
        dx = x - rx
        dy = y - ry

        # Rotate with current angle
        x = dx*math.cos(-rt) - dy*math.sin(-rt)
        y = dx*math.sin(-rt) + dy*math.cos(-rt)

        return x,y

    def algorithm(self):
        # Add your code here
        pass
    
    def genPath(self):
        print("Not yet coded!")
        path = None
        return path

