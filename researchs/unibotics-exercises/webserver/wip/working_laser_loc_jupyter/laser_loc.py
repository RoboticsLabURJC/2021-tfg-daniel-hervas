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
import matplotlib.lines as mlines
import numpy as np
import math

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

from sensors.sensors import Sensors
from sensors.threadSensors import ThreadSensors
from mapWidget import MapWidget
from MyAlgorithm import MyAlgorithm

import matplotlib.image as mpimg
import rospy
import threading
from math import asin, atan2, pi
from jderobotTypes import LaserData, CMDVel, Pose3d
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from threadPublisher import ThreadPublisher


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
        laser.minAngle = scan.angle_min  + pi/2
        laser.maxAngle = scan.angle_max  + pi/2
        laser.maxRange = scan.range_max
        laser.minRange = scan.range_min
        laser.timeStamp = scan.header.stamp.secs + (scan.header.stamp.nsecs *1e-9)
        return laser

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

def cmdvel2Twist(vel):
    '''
    Translates from JderobotTypes CMDVel to ROS Twist. 

    @param vel: JderobotTypes CMDVel to translate

    @type img: JdeRobotTypes.CMDVel

    @return a Twist translated from vel

    '''
    tw = Twist()
    tw.linear.x = vel.vx
    tw.linear.y = vel.vy
    tw.linear.z = vel.vz
    tw.angular.x = vel.ax
    tw.angular.y = vel.ay
    tw.angular.z = vel.az

    return tw

class PublisherMotors:
    '''
        ROS Motors Publisher. Motors Client to Send CMDVel to ROS nodes.
    '''
    def __init__(self, topic, maxV, maxW):
        '''
        ListenerMotors Constructor.

        @param topic: ROS topic to publish
        
        @type topic: String

        '''
        self.maxW = maxW
        self.maxV = maxV

        self.topic = topic
        self.data = CMDVel()
        self.pub = self.pub = rospy.Publisher(self.topic, Twist, queue_size=1)
        self.lock = threading.Lock()

        self.kill_event = threading.Event()
        self.thread = ThreadPublisher(self, self.kill_event)

        self.thread.daemon = True
        self.start()
 
    def publish (self):
        '''
        Function to publish cmdvel. 
        '''
        self.lock.acquire()
        tw = cmdvel2Twist(self.data)
        self.lock.release()
        self.pub.publish(tw)
        
    def stop(self):
        '''
        Stops (Unregisters) the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        self.kill_event.set()
        self.pub.unregister()

    def start (self):
        '''
        Starts (Subscribes) the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        self.kill_event.clear()
        self.thread.start()
        


    def getMaxW(self):
        return self.maxW

    def getMaxV(self):
        return self.maxV
        

    def sendVelocities(self, vel):
        '''
        Sends CMDVel.

        @param vel: CMDVel to publish
        
        @type vel: CMDVel

        '''
        self.lock.acquire()
        self.data = vel
        self.lock.release()

    def sendV(self, v):
        '''
        Sends V velocity. uses self.sendVX

        @param v: V velocity
        
        @type v: float

        '''
        self.sendVX(v)

    def sendL(self, l):
        '''
        Sends L velocity. uses self.sendVY

        @param l: L velocity
        
        @type l: float

        '''
        self.sendVY(l)

    def sendW(self, w):
        '''
        Sends W velocity. uses self.sendAZ

        @param w: W velocity
        
        @type w: float

        '''
        self.sendAZ(w)

    def sendVX(self, vx):
        '''
        Sends VX velocity.

        @param vx: VX velocity
        
        @type vx: float

        '''
        self.lock.acquire()
        self.data.vx = vx
        self.lock.release()

    def sendVY(self, vy):
        '''
        Sends VY velocity.

        @param vy: VY velocity
        
        @type vy: float

        '''
        self.lock.acquire()
        self.data.vy = vy
        self.lock.release()

    def sendAZ(self, az):
        '''
        Sends AZ velocity.

        @param az: AZ velocity
        
        @type az: float

        '''
        self.lock.acquire()
        self.data.vz = az
        self.lock.release()

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


class LaserLoc():

    def __init__(self, ax):

        cfg = config.load('laser_loc_conf.yml')

        ymlNode = cfg.getProperty('LaserLoc')
        node = rospy.init_node(ymlNode["NodeName"], anonymous=True)
        # ------------ M O T O R S ----------------------------------
        print("Publishing "+  "LaserLoc.Motors" + " with ROS messages")
        topicM = cfg.getProperty("LaserLoc.Motors"+".Topic")
        maxW = cfg.getPropertyWithDefault("LaserLoc.Motors"+".maxW", 0.5)
        if not maxW:
            maxW = 0.5
            print ("LaserLoc.Motors"+".maxW not provided, the default value is used: "+ repr(maxW))
        maxV = cfg.getPropertyWithDefault("LaserLoc.Motors"+".maxV", 5)
        if not maxV:
            maxV = 5
            print ("LaserLoc.Motors"+".maxV not provided, the default value is used: "+ repr(maxV))
        self.motors = PublisherMotors(topicM, maxV, maxW)
        # ----------------- P O S E     3 D -------------------------------------
        print("Receiving " + "LaserLoc.Pose3D" + " from ROS messages")
        topicP = cfg.getProperty("LaserLoc.Pose3D"+".Topic")
        self.pose3d = ListenerPose3d(topicP)
        # -------- L A S E R --------------------------------------------------
        print("Receiving " + "LaserLoc.Laser" + "  LaserData from ROS messages")
        topicL  = cfg.getProperty("LaserLoc.Laser"+".Topic")
        self.laser = ListenerLaser(topicL)

        self.map_img = cfg.getProperty("LaserLoc.Map.Img")

        self.ax = ax
        self.estimations = []
        self.fig = None
        self.ax1 = None

        #THREAD 3 - ALGORITHM AND COMPUTATION
        #////////////////////////////////////////////////////////
        self.algorithm = MyAlgorithm(self.pose3d, self.motors,self.laser)
        #////////////////////////////////////////////////////////
        self.map = MapWidget(self, self.map_img, self.algorithm)
        
        #THREAD 2 - SENSORS
        #////////////////////////////////////////////////////////
        self.sensor = Sensors(self.motors, self.pose3d, self.laser)

        t2 = ThreadSensors(self.sensor)
        t2.daemon = True
        t2.start()
        #////////////////////////////////////////////////////////

        print "Laser Loc Component initialized OK"

    def play(self):
        # self.unpause_physics_client()
        print "Laser Loc is running"
        self.algorithm.play()
        
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Laser Loc has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Laser Loc stopped" 

    def getLaser(self, particle):
        return self.algorithm.doRayTracing(particle)

    def paintParticles(self, particles):
        self.ax.cla()
        self.ax.imshow(self.map.map)
        self.ax.set_xlim([0, 500])
        self.ax.set_ylim([550, 0])
        for p in particles:
            px,py = self.map.map2pixel([p.x, p.y])
            c = self.map.prob2Color(p.prob)
            circle = plt.Circle((px,py), 3, color=c)
            self.ax.plot([px,px+10*math.cos(p.yaw)],[py,py-10*math.sin(p.yaw)],color=c)
            self.ax.add_artist(circle)
        est_prev = None
        for est in self.estimations:
            px,py = self.map.map2pixel([est[0], est[1]])
            circle = plt.Circle((px,py), 3, color='blue')
            self.ax.add_artist(circle)
            if est_prev is not None:
                self.ax.plot([est_prev[0],px],[est_prev[1],py],color='blue')
            est_prev = [px,py]
        #robot
        px,py = self.map.map2pixel([self.pose3d.getPose3d().x, self.pose3d.getPose3d().y])
        circle = plt.Circle((px,py), 3, color='purple')
        self.ax.plot([px,px-10*math.cos(self.pose3d.getPose3d().yaw)],[py,py+10*math.sin(self.pose3d.getPose3d().yaw)],color='purple')
        self.ax.add_artist(circle)      

    def paintLaser(self, laser):
        c = ""
        if len(laser)>9:
            step = 22
            c = "blue"
        else:
            step = 1
            c = "red"

        if not self.fig:
            self.fig=plt.figure()
            self.ax1=self.fig.add_subplot(111)

        allValues = []
        for d in range(0,len(laser),step):
            dist = laser[d][0]
            angle = laser[d][1]#-3*math.pi/4
            val = dist * math.cos(angle)
            allValues.append([0,val])
        allLevels = []
        for d in range(0,len(laser),step):
            dist = laser[d][0]
            angle = laser[d][1] #- math.pi/2
            if len(laser)>9:
                val = dist * math.sin(angle)
            else:
                val = -dist * math.sin(angle)
            allLevels.append([0,val])
        for levels, values in zip(allLevels, allValues):
            if len(laser)>9:
                self.ax1.plot(values,levels,color=c)
            else:
                self.ax1.plot(levels,values,color=c)
        plt.show()

    def setEstimation(self, estimation):
        self.estimations.append([estimation[0],estimation[1]])
        part = []
        self.paintParticles(part)

    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm)
        print "Code updated"  

    def setCalculateNewGeneration(self, cng):
        self.algorithm.newGen = types.MethodType(cng, self.algorithm)
        print "Function updated"     

    def moveTeleop(self, x, y):
        vel = CMDVel()
        vel.vx = (y-3.0)/2.5*self.motors.getMaxW()
        vel.az = -(x-2.0)/2.5*self.motors.getMaxV()
        self.motors.sendVelocities(vel)
