#  Authors :
#       Samuel Rey Escudero <samuel.rey.escudero@gmail.com>
#

import sys, math
import threading
#from PyQt5 import QtGui, QtCore
#from PyQt5.QtWidgets import QWidget, QLabel
#from PyQt5.QtCore import QPointF
import cv2
import time
from datetime import datetime

time_cycle = 50;

class Map(threading.Thread):
    
    def __init__(self, grid):
        #super(Map, self).__init__()
        #self.lock = threading.Lock()
        self.readConfFile()
        #self.parent = winParent        
        self.grid = grid
        self.initUI()

        self.lastPos = None
        self.lastDest = None
        self.stop_event = threading.Event()
        self.stop_event.set()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)
        

    def run (self):

        while (not self.kill_event.is_set()):

            self.stop_event.wait()
            
            start_time = datetime.now()

            self.updateMap(self.grid)
                        
            finish_Time = datetime.now()

            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def readConfFile(self):
        lines = open("taxiMap.conf", "r").readlines()

        if not lines:
            raise Exception("Could not read map config file")

        for line in lines:
            lineSplit = line.split("=")
            if (lineSplit[0] == "img"):
                if (lineSplit[1][-1] == "\n"):
                    self.mapPath = lineSplit[1][:-1]
                else:
                    self.mapPath = lineSplit[1]
            elif (lineSplit[0] == "worldWidth"):
                self.worldWidth = int(lineSplit[1])
            elif (lineSplit[0] == "worldHeight"):
                self.worldHeight = lineSplit[1]
            elif (lineSplit[0] == "originX"):
                self.originX = int(lineSplit[1])
            elif (lineSplit[0] == "originY"):
                self.originY = int(lineSplit[1])
            elif (lineSplit[0] == "angle"):
                self.mapAngle = int(lineSplit[1]) % 360

    def initUI(self):
        self.map = cv2.imread(self.mapPath, cv2.IMREAD_GRAYSCALE)
        self.map = cv2.resize(self.map, (400, 400))
        self.height = 400
        self.width = 400

