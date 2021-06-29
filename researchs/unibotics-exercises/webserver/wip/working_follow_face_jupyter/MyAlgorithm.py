# -*- coding: utf-8 -*-

import threading
import time
import cv2
import numpy as np
from datetime import datetime

time_cycle = 80

class MyAlgorithm(threading.Thread):


    def __init__(self, camera=None, motors=None):
        self.camera = camera
        self.motors = motors
        self.started = False

        self.pan = 0.0
        self.tilt = 0.0
        self.first_time = True
        self.time = 0.0
        self.topright = False
        # MOVE CAMERA TO A KNOWN POSITION
        if (self.motors):
            self.move_camera(0,0)
        self.width = 640
        self.height = 360
        self.threshold_image = np.zeros((640,360,3), np.uint8)
        self.color_image = np.zeros((640,360,3), np.uint8)

        self.stop_event = threading.Event()
        self.stop_event.set()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
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

    def pause (self):
        self.stop_event.clear()
        
    def play (self):
        self.stop_event.set()
        if not self.started:
          self.start()
          self.started = True

    def stop (self):
        self.kill_event.set()
   
    def getImage(self):
        self.lock.acquire()
        img = self.camera.getImage().data
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

    def move_camera(self, pan, tilt):
        if self.camera:
            limits = self.motors.getLimits()
            self.motors.setPTMotorsData(pan, tilt, limits.maxPanSpeed, limits.maxTiltSpeed)

    def algorithm(self):
        # Add your code here

        pass
