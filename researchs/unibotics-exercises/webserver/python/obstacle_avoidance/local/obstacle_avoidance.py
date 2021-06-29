#!/usr/bin/python
#-*- coding: utf-8 -*-
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
#       Aitor Martinez Fernandez <aitor.martinez.fernandez@gmail.com>
#       Francisco Miguel Rivas Montero <franciscomiguel.rivas@urjc.es>
#

import threading
import time
from datetime import datetime
import math
import numpy as np
from numpy import inf
import matplotlib.pyplot as plt
from web_sockets_server.utils import img2String
from std_srvs.srv import Empty

import json

import jderobot
import sys

class Target:
    def __init__(self,id,pose,active=False,reached=False):
        self.id=id
        self.pose=pose
        self.active=active
        self.reached=reached

    def getPose(self):
        return self.pose

    def getId(self):
        return self.id

    def getPose(self):
        return self.pose

    def isReached(self):
        return self.reached

    def setReached(self,value):
        self.reached=value

    def isActive(self):
        return self.active

    def setActive(self,value):
        self.active=True

class Parser:
    def __init__(self):
        data_string = '{ "targets": [{"name": "target 01", "x": 1,    "y": -30}, {"name": "target 02", "x": -5,   "y": -41}, {"name": "target 03", "x": -12,  "y": -33}, {"name": "target 04", "x": -15,  "y": -14}, {"name": "target 05", "x": -54,  "y": -13}, {"name": "target 06", "x": -63,  "y": -30}, {"name": "target 07", "x": -96,  "y": -25}, {"name": "target 08", "x": -96,  "y": 24}, {"name": "target 09", "x": -47,  "y": 48}, {"name": "target 10", "x": -40,  "y": 62}, {"name": "target 11", "x": -31,  "y": 45}, {"name": "target 12", "x": -22,  "y": 44}, {"name": "target 13", "x": -17,  "y": 59}, {"name": "target 14", "x": -1,   "y": 57}, {"name": "target 15", "x": 0,    "y": 0}] }'
        self.data = json.loads(data_string)

    def getTargets(self):
        targets = []
        for t in self.data["targets"]:
            targets.append(Target(t["name"],jderobot.Pose3DData(t["x"],t["y"],0,0,0,0,0,0),False,False))
        return targets

time_cycle = 80

class MyAlgorithm(threading.Thread):

    def __init__(self, laser, motors, pose3d, wsserver, rfstop):
        self.laser = laser
        self.motors = motors
        self.pose3d = pose3d
        self.wsserver = wsserver
        self.referee_stop = rfstop
        # Car direction
        self.carx = 0.0
        self.cary = 0.0
        # Obstacles direction
        self.obsx = 0.0
        self.obsy = 0.0
        # Average direction
        self.avgx = 0.0
        self.avgy = 0.0
        # Current target
        self.targetx = 0.0
        self.targety = 0.0
        self.targetid = "NaN"

        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)

        # Init targets
        parser = Parser()
        self.targets = parser.getTargets()
    
    def sendTargetWS(self, target):
        caryaw = self.pose3d.getPose3d().yaw
        targetx = target.getPose().x
        targety = target.getPose().y
        targetid = target.getId()
        dx = targetx - self.pose3d.getPose3d().x
        dy = targety - self.pose3d.getPose3d().y
        
        message = json.dumps({"func": "setTarget", "x":dx,"y":dy,"yaw":caryaw,"id":targetid})
        self.wsserver.sendMessage(message)


    def getNextTarget(self):
        for target in self.targets:
            if target.isReached() == False:
                self.sendTargetWS(target)
                
                return target

        self.referee_stop()
        self.stop()
        return None

    def getCarDirection(self):
        return (self.carx, self.cary)

    def getObstaclesDirection(self):
        return (self.obsx, self.obsy)

    def getAverageDirection(self):
        return (self.avgx, self.avgy)

    def setCarDirection(self,x,y):
        self.carx = x
        self.cary = y
        message = json.dumps({"func": "setCarDirection", "x":x,"y":y})
        self.wsserver.sendMessage(message)

    def setObstacleDirection(self,x,y):
        self.obsx = x
        self.obsy = y
        message = json.dumps({"func": "setObstacleDirection", "x":x,"y":y})
        self.wsserver.sendMessage(message)

    def setResultantDirection(self,x,y):
        self.avgx = x
        self.avgy = y
        message = json.dumps({"func": "setResultantDirection", "x":x,"y":y})
        self.wsserver.sendMessage(message)

    def getCurrentTarget(self):
        return (self.targetx, self.targety, self.targetid)
    
    def absolutas2relativas(self, x, y, rx, ry, rt):
        # Convert to relatives
        dx = x - rx
        dy = y - ry

        # Rotate with current angle
        x = dx*math.cos(-rt) - dy*math.sin(-rt)
        y = dx*math.sin(-rt) + dy*math.cos(-rt)

        return x,y

    def run (self):

        while (not self.kill_event.is_set()):
            lsr = np.asarray(self.laser.getLaserData().values)
            lsr[lsr == inf] = 10
            message = json.dumps({"func": "setLaser", "data": tuple(lsr) })
            self.wsserver.sendMessage(message)
            start_time = datetime.now()
            if not self.stop_event.is_set():
                self.algorithm()
            finish_Time = datetime.now()
            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()

    def kill (self):
        self.kill_event.set()

    def algorithm(self):
        #print "running"
        self.currentTarget=self.getNextTarget()
        self.targetx = self.currentTarget.getPose().x
        self.targety = self.currentTarget.getPose().y
        self.targetid = self.currentTarget.getId()
        #print(self.targetx,self.targety)

        # TODO

        # Car direction
        self.setCarDirection(2,0)
        # Obstacles direction
        self.setObstacleDirection(0,2)
        # Average direction
        self.setResultantDirection(2,2)

import types
import rospy
from geometry_msgs.msg import Twist
from math import pi as PI


class ThreadPublisher(threading.Thread):

    def __init__(self, pub, kill_event):
        self.pub = pub
        self.kill_event = kill_event
        threading.Thread.__init__(self, args=kill_event)

    def run(self):
        while (not self.kill_event.is_set()):
            start_time = datetime.now()

            self.pub.publish()

            finish_Time = datetime.now()

            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)



def cmdvel2Twist(vel):

    tw = Twist()
    tw.linear.x = vel.vx
    tw.linear.y = vel.vy
    tw.linear.z = vel.vz
    tw.angular.x = vel.ax
    tw.angular.y = vel.ay
    tw.angular.z = vel.az

    return tw


class CMDVel ():

    def __init__(self):

        self.vx = 0 # vel in x[m/s] (use this for V in wheeled robots)
        self.vy = 0 # vel in y[m/s]
        self.vz = 0 # vel in z[m/s]
        self.ax = 0 # angular vel in X axis [rad/s]
        self.ay = 0 # angular vel in X axis [rad/s]
        self.az = 0 # angular vel in Z axis [rad/s] (use this for W in wheeled robots)
        self.timeStamp = 0 # Time stamp [s]


    def __str__(self):
        s = "CMDVel: {\n   vx: " + str(self.vx) + "\n   vy: " + str(self.vy)
        s = s + "\n   vz: " + str(self.vz) + "\n   ax: " + str(self.ax) 
        s = s + "\n   ay: " + str(self.ay) + "\n   az: " + str(self.az)
        s = s + "\n   timeStamp: " + str(self.timeStamp)  + "\n}"
        return s 

class PublisherMotors:
 
    def __init__(self, topic, maxV, maxW):

        self.maxW = maxW
        self.maxV = maxV

        self.topic = topic
        self.data = CMDVel()
        self.pub = self.pub = rospy.Publisher(self.topic, Twist, queue_size=1)
        rospy.init_node("FollowLineF1")
        self.lock = threading.Lock()

        self.kill_event = threading.Event()
        self.thread = ThreadPublisher(self, self.kill_event)

        self.thread.daemon = True
        self.start()
 
    def publish (self):

        self.lock.acquire()
        tw = cmdvel2Twist(self.data)
        self.lock.release()
        self.pub.publish(tw)
        
    def stop(self):
   
        self.kill_event.set()
        self.pub.unregister()

    def start (self):

        self.kill_event.clear()
        self.thread.start()
        


    def getMaxW(self):
        return self.maxW

    def getMaxV(self):
        return self.maxV
        

    def sendVelocities(self, vel):

        self.lock.acquire()
        self.data = vel
        self.lock.release()

    def sendV(self, v):

        self.sendVX(v)

    def sendL(self, l):

        self.sendVY(l)

    def sendW(self, w):

        self.sendAZ(w)

    def sendVX(self, vx):

        self.lock.acquire()
        self.data.vx = vx
        self.lock.release()

    def sendVY(self, vy):

        self.lock.acquire()
        self.data.vy = vy
        self.lock.release()

    def sendAZ(self, az):

        self.lock.acquire()
        self.data.az = az
        self.lock.release()


from sensor_msgs.msg import LaserScan

def laserScan2LaserData(scan):
    '''
    Translates from ROS LaserScan to JderobotTypes LaserData. 
    @param scan: ROS LaserScan to translate
    @type scan: LaserScan
    @return a LaserData translated from scan
    '''
    laser = LaserData()
    laser.values = scan.ranges
    ''' 
          ROS Angle Map      JdeRobot Angle Map
                0                  PI/2
                |                   |
                |                   |
       PI/2 --------- -PI/2  PI --------- 0
                |                   |
                |                   |
    '''
    laser.minAngle = scan.angle_min  + PI/2
    laser.maxAngle = scan.angle_max  + PI/2
    laser.maxRange = scan.range_max
    laser.minRange = scan.range_min
    laser.timeStamp = scan.header.stamp.secs + (scan.header.stamp.nsecs *1e-9)
    return laser

class LaserData ():

	def __init__(self):

		self.values = [] # meters
		self.minAngle = 0 # Angle of first value (rads)
		self.maxAngle = 0 # Angle of last value (rads)
		self.minRange = 0 # Max Range posible (meters)
		self.maxRange = 0 #Min Range posible (meters)
		self.timeStamp = 0 # seconds


	def __str__(self):
		s = "LaserData: {\n   minAngle: " + str(self.minAngle) + "\n   maxAngle: " + str(self.maxAngle)
		s = s + "\n   minRange: " + str(self.minRange) + "\n   maxRange: " + str(self.maxRange) 
		s = s + "\n   timeStamp: " + str(self.timeStamp) + "\n   values: " + str(self.values) + "\n}"
		return s 


class ListenerLaser:
    '''
        ROS Laser Subscriber. Laser Client to Receive Laser Scans from ROS nodes.
    '''
    def __init__(self, topic):
        '''
        ListenerLaser Constructor.
        @param topic: ROS topic to subscribe
        
        @type topic: String
        '''
        self.topic = topic
        self.data = LaserData()
        self.sub = None
        self.lock = threading.Lock()
        self.start()
 
    def __callback (self, scan):
        '''
        Callback function to receive and save Laser Scans. 
        @param scan: ROS LaserScan received
        
        @type scan: LaserScan
        '''
        laser = laserScan2LaserData(scan)

        self.lock.acquire()
        self.data = laser
        self.lock.release()
        
    def stop(self):
        '''
        Stops (Unregisters) the client.
        '''
        self.sub.unregister()

    def start (self):
        '''
        Starts (Subscribes) the client.
        '''
        self.sub = rospy.Subscriber(self.topic, LaserScan, self.__callback)
        
    def getLaserData(self):
        '''
        Returns last LaserData. 
        @return last JdeRobotTypes LaserData saved
        '''
        self.lock.acquire()
        laser = self.data
        self.lock.release()
        
        return laser


from nav_msgs.msg import Odometry
from math import asin, atan2, pi

def quat2Yaw(qw, qx, qy, qz):
    '''
    Translates from Quaternion to Yaw. 

    @param qw,qx,qy,qz: Quaternion values

    @type qw,qx,qy,qz: float

    @return Yaw value translated from Quaternion

    '''
    rotateZa0=2.0*(qx*qy + qw*qz)
    rotateZa1=qw*qw + qx*qx - qy*qy - qz*qz
    rotateZ=0.0
    if(rotateZa0 != 0.0 and rotateZa1 != 0.0):
        rotateZ=atan2(rotateZa0,rotateZa1)
    return rotateZ

def quat2Pitch(qw, qx, qy, qz):
    '''
    Translates from Quaternion to Pitch. 

    @param qw,qx,qy,qz: Quaternion values

    @type qw,qx,qy,qz: float

    @return Pitch value translated from Quaternion

    '''

    rotateYa0=-2.0*(qx*qz - qw*qy)
    rotateY=0.0
    if(rotateYa0 >= 1.0):
        rotateY = pi/2.0
    elif(rotateYa0 <= -1.0):
        rotateY = -pi/2.0
    else:
        rotateY = asin(rotateYa0)

    return rotateY

def quat2Roll (qw, qx, qy, qz):
    '''
    Translates from Quaternion to Roll. 

    @param qw,qx,qy,qz: Quaternion values

    @type qw,qx,qy,qz: float

    @return Roll value translated from Quaternion

    '''
    rotateXa0=2.0*(qy*qz + qw*qx)
    rotateXa1=qw*qw - qx*qx - qy*qy + qz*qz
    rotateX=0.0

    if(rotateXa0 != 0.0 and rotateXa1 != 0.0):
        rotateX=atan2(rotateXa0, rotateXa1)
    return rotateX


def odometry2Pose3D(odom):
    '''
    Translates from ROS Odometry to JderobotTypes Pose3d. 

    @param odom: ROS Odometry to translate

    @type odom: Odometry

    @return a Pose3d translated from odom

    '''
    pose = Pose3d()
    ori = odom.pose.pose.orientation

    pose.x = odom.pose.pose.position.x
    pose.y = odom.pose.pose.position.y
    pose.z = odom.pose.pose.position.z
    #pose.h = odom.pose.pose.position.h
    pose.yaw = quat2Yaw(ori.w, ori.x, ori.y, ori.z)
    pose.pitch = quat2Pitch(ori.w, ori.x, ori.y, ori.z)
    pose.roll = quat2Roll(ori.w, ori.x, ori.y, ori.z)
    pose.q = [ori.w, ori.x, ori.y, ori.z]
    pose.timeStamp = odom.header.stamp.secs + (odom.header.stamp.nsecs *1e-9)

    return pose

class Pose3d ():

	def __init__(self):

		self.x = 0 # X coord [meters]
		self.y = 0 # Y coord [meters]
		self.z = 0 # Z coord [meters]
		self.h = 1 # H param
		self.yaw = 0 #Yaw angle[rads]
		self.pitch = 0 # Pitch angle[rads]
		self.roll = 0 # Roll angle[rads]
		self.q = [0,0,0,0] # Quaternion
		self.timeStamp = 0 # Time stamp [s]


	def __str__(self):
		s = "Pose3D: {\n   x: " + str(self.x) + "\n   Y: " + str(self.y)
		s = s + "\n   Z: " + str(self.z) + "\n   H: " + str(self.h) 
		s = s + "\n   Yaw: " + str(self.yaw) + "\n   Pitch: " + str(self.pitch) + "\n   Roll: " + str(self.roll)
		s = s + "\n   quaternion: " + str(self.q) + "\n   timeStamp: " + str(self.timeStamp)  + "\n}"
		return s 


class ListenerPose3d:
    '''
        ROS Pose3D Subscriber. Pose3D Client to Receive pose3d from ROS nodes.
    '''
    def __init__(self, topic):
        '''
        ListenerPose3d Constructor.

        @param topic: ROS topic to subscribe
        
        @type topic: String

        '''
        self.topic = topic
        self.data = Pose3d()
        self.sub = None
        self.lock = threading.Lock()
        self.start()
 
    def __callback (self, odom):
        '''
        Callback function to receive and save Pose3d. 

        @param odom: ROS Odometry received
        
        @type odom: Odometry

        '''
        pose = odometry2Pose3D(odom)

        self.lock.acquire()
        self.data = pose
        self.lock.release()
        
    def stop(self):
        '''
        Stops (Unregisters) the client.

        '''
        self.sub.unregister()

    def start (self):
        '''
        Starts (Subscribes) the client.

        '''
        self.sub = rospy.Subscriber(self.topic, Odometry, self.__callback)
        
    def getPose3d(self):
        '''
        Returns last Pose3d. 

        @return last JdeRobotTypes Pose3d saved

        '''
        self.lock.acquire()
        pose = self.data
        self.lock.release()
        
        return pose

import config
from web_sockets_server import getWebSocketServer

class ObstacleAvoidance():

    def __init__(self):
        cfg = config.load("obstacle_avoidance.yml")

        laserTopic = cfg.getProperty("Laser.Topic")
        poseTopic = cfg.getProperty("Pose3D.Topic")
        motorsTopic = cfg.getProperty("Motors.Topic")
        self.motors = PublisherMotors(motorsTopic, 4, 0.3)
        self.laser = ListenerLaser(laserTopic)
        self.pose3d = ListenerPose3d(poseTopic)

        ssl = cfg.getProperty("Websockets.SSL")
        host = cfg.getProperty("Websockets.Host")
        port = int(cfg.getProperty("Websockets.Port"))
        cert = cfg.getPropertyWithDefault("Websockets.Cert", None)
        key = cfg.getPropertyWithDefault("Websockets.Key", None)
        #print(cert, key)

        self.wsserver = getWebSocketServer(host, port, ssl, cert, key)
        self.wsserver.start()
        self.referee_start = rospy.ServiceProxy("refereeStart", Empty)
        self.referee_stop = rospy.ServiceProxy("refereeStop", Empty)
        self.algorithm=MyAlgorithm(self.laser, self.motors, self.pose3d, self.wsserver, self.referee_stop)
        print "Obstacle_Avoidance Components initialized OK"

    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        self.referee_start()
        print "Obstacle_Avoidance is running"

    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Obstacle_Avoidance has been paused"

    def stop(self):
        self.algorithm.stop()
        self.referee_stop()
        self.wssever.stop()
        print "Obstacle_Avoidance stopped"

    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm )
        print "Code updated"

    def move(self):
        self.algorithm.move()

    def setCarDirection(self,x,y):
        self.algorithm.setCarDirection(x,y)

    def setObstacleDirection(self,x,y):
        self.algorithm.setObstacleDirection(x,y)

    def setResultantDirection(self,x,y):
        self.algorithm.setResultantDirection(x,y)

    def getNextTarget(self):
        self.algorithm.getNextTarget(self)


def printImage(image):
    plt.axis('off')
    a = plt.imshow(image)
    plt.show()
