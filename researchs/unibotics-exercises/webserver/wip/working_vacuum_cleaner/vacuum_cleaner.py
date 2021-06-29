import sys
sys.path.append('/usr/lib/python2.7/')
import types
import rospy
from std_srvs.srv import Empty
import time


import comm
import config

from MyAlgorithm import MyAlgorithm

class VacuumCleaner ():
    def __init__(self):
        
        cfg = config.load("vacuum_cleaner_conf.yml")

        #starting comm
        jdrc= comm.init(cfg,'VacuumCleaner')

        self.motors = jdrc.getMotorsClient("VacuumCleaner.Motors")
        self.pose3d = jdrc.getPose3dClient("VacuumCleaner.Pose3D")
        self.laser = jdrc.getLaserClient("VacuumCleaner.Laser").hasproxy()
        self.bumper = jdrc.getBumperClient("VacuumCleaner.Bumper")

        self.algorithm = MyAlgorithm(self.motors, self.pose3d, self.laser, self.bumper)

        print "Vacuum_Cleaner initialized OK"
        
    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        print "Vacuum_Cleaner is running"
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Vacuum_Cleaner has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Vacuum_Cleaner stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType( execute, self.algorithm )
        print "Code updated"       

    def move(self):
        self.algorithm.move()
