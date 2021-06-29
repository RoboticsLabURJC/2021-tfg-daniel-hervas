#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import threading
import time
from datetime import datetime

import jderobot
import math
from math import pi as pi
import cv2
import numpy as np


from matplotlib import pyplot as plt
time_cycle = 80


class MyAlgorithm(threading.Thread):

    def __init__(self, pose3d, cameraC, cameraL, cameraR, motors):
        self.cameraL = cameraL
        self.cameraR = cameraR
        self.cameraC = cameraC
        self.pose3d = pose3d
        self.motors = motors

        self.threshold_image = np.zeros((640,360,3), np.uint8)
        self.color_image = np.zeros((640,360,3), np.uint8)

        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)

    def getImageC(self):
        self.lock.acquire()
        img = self.cameraC.getImage().data
        self.lock.release()
        return img
    
    def getImageR(self):
        self.lock.acquire()
        img = self.cameraR.getImage().data
        self.lock.release()
        return img
    
    def getImageL(self):
        self.lock.acquire()
        img = self.cameraL.getImage().data
        self.lock.release()
        return img

    def set_color_image (self, image):
        img  = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self.color_image_lock.acquire()
        self.color_image = img
        self.color_image_lock.release()

    def get_color_image (self):
        self.color_image_lock.acquire()
        img = np.copy(self.color_image)
        self.color_image_lock.release()
        return img

    def set_threshold_image (self, image):
        img = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self.threshold_image_lock.acquire()
        self.threshold_image = img
        self.threshold_image_lock.release()

    def get_threshold_image (self):
        self.threshold_image_lock.acquire()
        img  = np.copy(self.threshold_image)
        self.threshold_image_lock.release()
        return img

    def setImageFiltered(self, image):
        self.lock.acquire()
        self.lock.release()


    def getImageFiltered(self):
        self.lock.acquire()
        tempImage=self.image
        self.lock.release()
        return tempImage


    def run (self):
        while (not self.kill_event.is_set()):

            start_time = datetime.now()

            if not self.stop_event.is_set():
                self.algorithm()

            finish_Time = datetime.now()

            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)


    def stop (self):
        self.stop_event.set()


    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()


    def kill (self):
        self.kill_event.set()
        

    def algorithm(self):
        # Add your code here
        pass
