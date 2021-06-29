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
#       Eduardo Perdices <eperdices@gsyc.es>
#       Aitor Martinez Fernandez <aitor.martinez.fernandez@gmail.com>
#

import sys
import comm
import config
import types
sys.path.append('/usr/lib/python2.7/')
from MyAlgorithm import MyAlgorithm


class StopPractice():
    def __init__(self):
        cfg = config.load("stop_conf.yml")

        #starting comm
        jdrc= comm.init(cfg, 'Stop')

        self.cameraC = jdrc.getCameraClient("Stop.CameraC")
        self.cameraL = jdrc.getCameraClient("Stop.CameraL")
        self.cameraR = jdrc.getCameraClient("Stop.CameraR")
        self.motors = jdrc.getMotorsClient ("Stop.Motors")
        self.pose3d = jdrc.getPose3dClient("Stop.Pose3D")

        self.algorithm=MyAlgorithm(self.pose3d, self.cameraC, self.cameraL, self.cameraR, self.motors)

        print "Stop_Practice Components initialized OK"

    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        print "Stop_Practice is running"

    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Stop_Practice has been paused"

    def stop(self):
        self.algorithm.stop()
        print "Stop_Practice stopped"

    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm )
        print "Code updated"

    def move(self):
        self.algorithm.move()

    def get_threshold_image(self):
        return self.algorithm.get_threshold_image()

    def get_color_image(self):
        return self.algorithm.get_color_image()
