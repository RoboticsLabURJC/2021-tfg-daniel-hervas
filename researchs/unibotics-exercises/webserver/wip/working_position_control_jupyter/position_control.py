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
import types
sys.path.append('/usr/lib/python2.7/')
import config
import comm
from MyAlgorithm import MyAlgorithm, PID


class PositionControl():

    def __init__(self):

        cfg = config.load("position_control_conf.yml")
        #starting comm
        jdrc = comm.init(cfg, 'Introrob')

        self.camera = jdrc.getCameraClient("Introrob.Camera")
        self.navdata = jdrc.getNavdataClient("Introrob.Navdata")
        self.pose = jdrc.getPose3dClient("Introrob.Pose3D")
        self.cmdvel = jdrc.getCMDVelClient("Introrob.CMDVel")
        self.extra = jdrc.getArDroneExtraClient("Introrob.Extra")

        self.algorithm=MyAlgorithm(self.camera, self.navdata, self.pose, self.cmdvel, self.extra)

        print "Position Control Component initialized OK"

    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        print "Position Control is running"
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Position Control has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Position Control stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm)
        print "Code updated"

    def setPID(self, pid):
        self.algorithm.xPid.update = types.MethodType(pid, self.algorithm.xPid)
        self.algorithm.yPid.update = types.MethodType(pid, self.algorithm.yPid)
        print "PID updated"       
    
    def get_color_image(self):
        return self.algorithm.get_color_image()


