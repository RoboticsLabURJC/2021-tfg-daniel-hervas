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

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

class Autopark():

    def __init__(self):


        cfg = config.load("autopark_conf.yml")

        #starting comm
        jdrc= comm.init(cfg, 'Autopark')

        self.motors = jdrc.getMotorsClient ("Autopark.Motors")
        self.pose3d = jdrc.getPose3dClient("Autopark.Pose3D")
        self.laser1 = jdrc.getLaserClient("Autopark.Laser1").hasproxy()
        self.laser2 = jdrc.getLaserClient("Autopark.Laser2").hasproxy()
        self.laser3 = jdrc.getLaserClient("Autopark.Laser3").hasproxy()

        self.algorithm = MyAlgorithm(self.pose3d, self.laser1, self.laser2, self.laser3, self.motors)

        print "Autopark Component initialized OK"

    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        print "Autopark is running"
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Autopark has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Autopark stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm)
        print "Code updated"       
        
