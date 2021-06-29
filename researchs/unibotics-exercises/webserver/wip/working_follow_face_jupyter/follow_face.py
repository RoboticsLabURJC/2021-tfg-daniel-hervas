#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#  Copyright (C) 1997-2016 JdeRobot Developers Team
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
#       Carlos Awadallah Estévez<carlosawadallah@gmail.com>
#

import sys
sys.path.append('/usr/lib/python2.7/')
import types
import rospy
from std_srvs.srv import Empty
import time

from MyAlgorithm import MyAlgorithm
import comm, config
import subprocess

class FollowFace ():

    def __init__(self):

        rosdriver = subprocess.Popen(("roslaunch", "usb_cam-test.launch"))
        evidriver = subprocess.Popen(("evicam_driver", "evicam_driver.cfg"))

        cfg = config.load("follow_face_conf.yml")

        #starting comm
        jdrc= comm.init(cfg, 'Follow_face')

        self.camera = jdrc.getCameraClient("Follow_face.Camera")
        self.motors = jdrc.getPTMotorsClient("Follow_face.PTMotors")
        self.algorithm=MyAlgorithm(self.camera, self.motors)

        print "Follow Face Component initialized OK"

    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        print "Follow Face is running"
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Follow Face has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Follow Face stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm)
        print "Code updated"       
        
    def get_threshold_image(self):
        return self.algorithm.get_threshold_image()
    
    def get_color_image(self):
        return self.algorithm.get_color_image()

    def move_camera(self, pan, tilt):
        self.algorithm.move_camera(pan, tilt)
