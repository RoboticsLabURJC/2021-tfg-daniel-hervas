#!/usr/bin/python
#-*- coding: utf-8 -*-
import threading
import time
from datetime import datetime

import math
import cv2
import numpy as np

time_cycle = 80

class MyAlgorithm(threading.Thread):

    def __init__(self, drone):
        self.drone = drone
        self.threshold_image_ventral = np.zeros((640,360,3), np.uint8)
        self.color_image_ventral = np.zeros((640,360,3), np.uint8)
        self.threshold_image_frontal = np.zeros((640,360,3), np.uint8)
        self.color_image_frontal = np.zeros((640,360,3), np.uint8)
        self.using_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_image_ventral_lock = threading.Lock()
        self.color_image_ventral_lock = threading.Lock()
        self.threshold_image_frontal_lock = threading.Lock()
        self.color_image_frontal_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.kill_event)
    
    def getImageVentral(self):
        self.lock.acquire()
        img = self.drone.getImageVentral().data
        self.lock.release()
        return img
    
    def getImageFrontal(self):
        self.lock.acquire()
        img = self.drone.getImageFrontal().data
        self.lock.release()
        return img

    def set_color_image_ventral (self, image):
        img  = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.color_image_ventral_lock.acquire()
        self.color_image_ventral = img
        self.color_image_ventral_lock.release()
	plt.axis('off') # printImage
        a = plt.imshow(img)
        time.sleep(0.1)

    
    def set_color_image_frontal (self, image):
        img  = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.color_image_frontal_lock.acquire()
        self.color_image_frontal = img
        self.color_image_frontal_lock.release()
	plt.axis('off') # printImage
        a = plt.imshow(img)
        time.sleep(0.1)
        
    def get_color_image_ventral (self):
        self.color_image_ventral_lock.acquire()
        img = np.copy(self.color_ventral_image)
        self.color_image_ventral_lock.release()
        return img
    
    def get_color_image_frontal (self):
        self.color_image_frontal_lock.acquire()
        img = np.copy(self.color_image_frontal)
        self.color_image_frontal_lock.release()
        return img
        
    def set_threshold_image_ventral (self, image):
        img = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.threshold_image_ventral_lock.acquire()
        self.threshold_image_ventral = img
        self.threshold_image_ventral_lock.release()
	plt.axis('off') # printImage
        a = plt.imshow(img)
        time.sleep(0.1)
        
    def set_threshold_image_frontal (self, image):
        img = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.threshold_image_frontal_lock.acquire()
        self.threshold_image_frontal = img
        self.threshold_image_frontal_lock.release()
	plt.axis('off') # printImage
        a = plt.imshow(img)
        time.sleep(0.1)
        
    def get_threshold_image_ventral (self):
        self.threshold_image_ventral_lock.acquire()
        img  = np.copy(self.threshold_image_ventral)
        self.threshold_image_ventral_lock.release()
        return img
    
    def get_threshold_image_frontal (self):
        self.threshold_image_frontal_lock.acquire()
        img  = np.copy(self.threshold_image_frontal)
        self.threshold_image_frontal_lock.release()
        return img

    def run (self):

        while (not self.kill_event.is_set()):
            self.using_event.wait()
            start_time = datetime.now()
            self.algorithm()
            finish_Time = datetime.now()
            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.kill_event.set()

    def play (self):
        self.start()
            
    def pause (self):
        self.using_event.clear()
        
        
    def resume(self):
        self.using_event.set()

    def kill (self):
        self.kill_event.set()

    def algorithm(self):
        #GETTING THE IMAGES
        image = self.getImageFrontal()

        # Add your code here
        #print "Runing"

        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        #self.motors.setV(10)
        #self.motors.setW(5)

        #SHOW THE FILTERED IMAGE ON THE GUI
        self.set_color_image_frontal(image)
