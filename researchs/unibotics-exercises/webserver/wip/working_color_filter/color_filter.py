#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/usr/lib/python2.7/')
import types
import rospy
from std_srvs.srv import Empty
import time

from MyAlgorithm import MyAlgorithm
import easyiceconfig as EasyIce
from parallelIce.cameraClient import CameraClient
from parallelIce.cmdvel import CMDVel
from parallelIce.extra import Extra
from parallelIce.pose3dClient import Pose3DClient

class ColorFilter ():
    def __init__(self):
        ic = EasyIce.initialize(["color_filter", "color_filter.cfg"])
        
        self.camera = CameraClient(ic, "Introrob.Camera", True)
        self.pose = Pose3DClient(ic, "Introrob.Pose3D", True)
        self.cmdvel = CMDVel(ic, "Introrob.CMDVel")
        self.extra = Extra(ic, "Introrob.Extra")
        #self.pause_physics_client = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        #self.unpause_physics_client = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)

        self.algorithm = MyAlgorithm(self.camera, self.pose, self.cmdvel, self.extra)
        
        print "Color filter initialized OK"
        
    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        print "Color filter is running"
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Color filter has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Color filter stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType( execute, self.algorithm )
        print "Code updated"       
        
    def get_filtered_image (self):
        return self.algorithm.get_filtered_image()
    
    def get_color_image (self):
        return self.algorithm.get_color_image()

    def move(self):
        self.algorithm.move()
        
