import threading
import time
import cv2
import numpy as np
from datetime import datetime

time_cycle = 80

class MyAlgorithm(threading.Thread):


    def __init__(self, camera=None, pose=None, cmdvel=None, extra=None):
        self.camera = camera
        self.pose = pose
        self.cmdvel = cmdvel
        self.extra = extra
        self.started = False
        
        self.filtered_image = np.zeros((480,640,3), np.uint8)
        self.color_image = np.zeros((480,640,3), np.uint8)

        self.stop_event = threading.Event()
        self.stop_event.set()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.filtered_image_lock = threading.Lock()
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
        
    def set_filtered_image (self, image):
        img = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self.filtered_image_lock.acquire()
        self.filtered_image = img
        self.filtered_image_lock.release()
        
    def get_filtered_image (self):
        self.filtered_image_lock.acquire()
        img  = np.copy(self.filtered_image)
        self.filtered_image_lock.release()
        return img

    def move(self):
        self.cmdvel.sendCMDVel(0.0,0,0,0,0.0,0.5)

    def algorithm(self):
        # Add your code here

        pass
