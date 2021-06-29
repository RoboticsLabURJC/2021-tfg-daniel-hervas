import threading
import time
from datetime import datetime

import math
import jderobot
from Beacon import Beacon
import numpy as np

time_cycle = 80

class PID:
    """
	Discrete PID control
	"""

    def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.Derivator = Derivator
        self.Integrator = Integrator
        self.Integrator_max = Integrator_max
        self.Integrator_min = Integrator_min

        self.set_point = 0.0
        self.error = 0.0

    def update(self, current_value):
        pass

class MyAlgorithm(threading.Thread):

    def __init__(self, camera, navdata, pose, cmdvel, extra):
        self.camera = camera
        self.navdata = navdata
        self.pose = pose
        self.cmdvel = cmdvel
        self.extra = extra
        self.started = False

        self.beacons=[]
        self.initBeacons()
        self.minError=0.01

        self.xPid=PID()
        self.yPid=PID()
        self.threshold_image = np.zeros((640,360,3), np.uint8)
        self.color_image = np.zeros((640,360,3), np.uint8)

        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.threshold_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
        self.lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)

    def initBeacons(self):
        self.beacons.append(Beacon('baliza1',jderobot.Pose3DData(0,5,0,0,0,0,0,0),False,False))
        self.beacons.append(Beacon('baliza2',jderobot.Pose3DData(5,0,0,0,0,0,0,0),False,False))
        self.beacons.append(Beacon('baliza3',jderobot.Pose3DData(0,-5,0,0,0,0,0,0),False,False))
        self.beacons.append(Beacon('baliza4',jderobot.Pose3DData(-5,0,0,0,0,0,0,0),False,False))
        self.beacons.append(Beacon('baliza5',jderobot.Pose3DData(10,0,0,0,0,0,0,0),False,False))
        self.beacons.append(Beacon('inicio',jderobot.Pose3DData(0,0,0,0,0,0,0,0),False,False))

    def getNextBeacon(self):
        for beacon in self.beacons:
            if beacon.isReached() == False:
                return beacon

        return None

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
    
    def reset(self):
        self.xPid=PID()
        self.yPid=PID()
        self.beacons=[]
        self.initBeacons()

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

    def algorithm(self):
        # Add your code here
        pass
