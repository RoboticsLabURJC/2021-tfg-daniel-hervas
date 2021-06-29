# -*- coding: utf-8 -*-

import numpy as np
import threading
import time
from datetime import datetime
import jderobot
import math
import cv2
from math import pi as pi
import random
from particles import Particle
#from PyQt5 import QtGui
import copy

time_cycle = 10

class MyAlgorithm(threading.Thread):

    def __init__(self, pose3d, motors, laser):
        # Robot's sensors and actuators
        # ------------------
        self.pose3d = pose3d
        self.motors = motors
        self.laser = laser
        self.map = None
        # ------------------
        self.started = False
        self.initiallized = False
        self.newGeneration = False
        self.particleClicked = None 
        self.calculated = False
        
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

    def parse_laser_data(self,laser_data):
        laser = []
        for i in range(180):
            dist = laser_data.values[i]
            angle = math.radians(i)
            laser += [(dist, angle)]
        return laser

    def setParticles (self, particles):
        self.map.setParticles(particles)

    def setEstimation (self, est):
        if self.isAvailable(est[0],est[1]):
            self.map.parent.setEstimation(est)

    def isAvailable(self, x, y):
        return self.isWhitePixel(x,y)

    def isWhitePixel (self, x, y):
        img = self.map.map
        white = [255, 255, 255]
        px,py = self.map.map2pixel((x,y))
        px = int(px)
        py = int(py)
        if (px < 0) or (py < 0) or (px >= self.map.width) or (py >= self.map.height):
            return False
        else:
            color = img[py,px]
            color = color.tolist()
            if color == white:
                return True
            else:
                return False

    def newGen(self):
        print("new generation")
        particles = []
        self.setParticles(particles)
            
    def algorithm(self):
        
        if self.particleClicked is not None and not self.calculated:
            print("Particle Probability: ", self.particleClicked.prob)
            self.calculated = True

        if self.newGeneration:
            self.newGen()
            self.newGeneration = False

