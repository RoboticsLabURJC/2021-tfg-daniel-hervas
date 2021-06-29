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
#       Alberto Martin Florido <almartinflorido@gmail.com>
#       Aitor Martinez Fernandez <aitor.martinez.fernandez@gmail.com>
#

import sys
import config
sys.path.append('/usr/lib/python2.7/')
import types
import comm
from MyAlgorithm import MyAlgorithm

class VacuumSLAM():
    
    def __init__(self):
        cfg = config.load("vacuum_conf.yml")

        #starting comm
        jdrc= comm.init(cfg, 'VacuumSLAM')

        self.motors = jdrc.getMotorsClient ("VacuumSLAM.Motors")
        self.pose3d = jdrc.getPose3dClient("VacuumSLAM.Pose3D")
        self.laser = jdrc.getLaserClient("VacuumSLAM.Laser").hasproxy()
        self.bumper = jdrc.getBumperClient("VacuumSLAM.Bumper")

        #algorithm=MyAlgorithm(pose3d, motors,laser,bumper)
        self.algorithm=MyAlgorithm(self.pose3d, self.motors,self.laser,self.bumper)

        print "Vacuum SLAM Component initialized OK"

    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        print "Vacuum SLAM is running"
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Vacuum SLAM has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Vacuum SLAM stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm)
        print "Code updated"       
        