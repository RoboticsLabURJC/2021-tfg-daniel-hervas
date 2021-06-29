#!/usr/bin/python3
#
#  Copyright (C) 1997-2016 JDE Developers Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#  Authors :
#       Carlos Awadallah Estevez <carlosawadallah@gmail.com>
#

import sys
sys.path.append('/usr/lib/python2.7/')
import types
import comm
import config
from MyAlgorithm import MyAlgorithm
from matplotlib import pyplot as plt

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

from threadMotors import ThreadMotors
from threadMotors import Velocity

from sensors.sensor import Sensor
from sensors.grid import Grid


class GlobalNavigation():

    def __init__(self):
        self.coordinatesClicked = None
        self.grid = Grid()

        cfg = config.load("teleTaxi_conf.yml")
        #starting comm
        jdrc= comm.init(cfg, 'TeleTaxi')

        self.motors = jdrc.getMotorsClient ("TeleTaxi.Motors")
        self.pose = jdrc.getPose3dClient("TeleTaxi.Pose3D")

        self.vel = Velocity(0, 0, self.motors.getMaxV(), self.motors.getMaxW()) 
        self.sensor = Sensor(self.grid, self.pose, True)
        self.algorithm = MyAlgorithm(self.grid, self.sensor, self.vel, self)

        t1 = ThreadMotors(self.motors, self.vel)
        t1.daemon = True
        t1.start()

        print "Global Navigation Component initialized OK"

    def play(self):
        # self.unpause_physics_client()
        print "Global Navigation is running"
        self.algorithm.play()
        
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Global Navigation has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Global Navigation stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm)
        print "Code updated"  

    def setGeneratePath(self, gepa):
        self.algorithm.genPath = types.MethodType(gepa, self.algorithm)
        print "Function updated"     

    def printCoordinates(self, x, y):
        print "x: {0}, y: {1} ".format(x,y)

    def calcPath(self):
        return self.algorithm.genPath()

    def setAx(self, ax):
        self.ax = ax

    def paintRobot(self):
        robotpos = self.algorithm.grid.worldToGrid(self.sensor.getRobotX(), self.sensor.getRobotY())
        robot = plt.Circle((robotpos[0], robotpos[1]), 3, color='yellow')
        self.ax.add_artist(robot)

        
            
        

