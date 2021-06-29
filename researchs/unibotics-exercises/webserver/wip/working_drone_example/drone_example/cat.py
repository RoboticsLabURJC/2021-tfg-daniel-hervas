import rospy
import types
from .MyAlgorithm import MyAlgorithm
from drone import Drone

import subprocess

from std_srvs.srv import Empty

class Cat():
    
    def __init__(self):
        self.drone = Drone("mavros/cmd/arming", "mavros/cmd/land","mavros/set_mode",  "/mavros/setpoint_velocity/cmd_vel","/mavros/local_position/odom",  "/solo/cam_ventral/image_raw", "/solo/cam_frontal/image_raw")
        self.algorithm=MyAlgorithm(self.drone)
        self.pause_physics_client=rospy.ServiceProxy('/gazebo/pause_physics',Empty)
        self.unpause_physics_client = rospy.ServiceProxy('/gazebo/unpause_physics',Empty)
        print "Drone Components initialized OK"

    def play(self):
        if self.algorithm.is_alive():
            self.unpause_physics_client()
        self.algorithm.play()
        print "Drone is running"
        
    def pause (self):
        self.pause_physics_client()
        self.drone.pause()
        self.algorithm.pause()
        
        print "Drone has been paused"
        
    def resume (self):
        self.unpause_physics_client()
        self.algorithm.resume()
        self.drone.resume()
        print "Drone has been resumed"
         
    def stop(self):
        self.algorithm.stop()
        print "Drone stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm )
        print "Code updated"       

    def move(self):
        self.algorithm.move()
    
    def get_threshold_image_ventral(self):
        return self.algorithm.get_threshold_image_ventral()
    
    def get_threshold_image_frontal(self):
        return self.algorithm.get_threshold_image_frontal()
    
    def get_color_image_ventral(self):
        return self.algorithm.get_color_image_ventral()
    
    def get_color_image_frontal(self):
        return self.algorithm.get_color_image_frontal()
