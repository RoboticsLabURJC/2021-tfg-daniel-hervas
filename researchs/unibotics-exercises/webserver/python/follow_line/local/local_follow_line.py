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
#       Aitor Martinez Fernandez <aitor.martinez.fernandez@gmail.com>
#       Francisco Miguel Rivas Montero <franciscomiguel.rivas@urjc.es>
#       Carlos Awadallah Estevez <carlosawadallah@gmail.com>
#


import rospy
from sensor_msgs.msg import Image as ImageROS
from std_srvs.srv import Empty
from math import pi as PI
import cv2
from cv_bridge import CvBridge, CvBridgeError
import threading


MAXRANGE = 8 #max length received from imageD
MINRANGE = 0

def imageMsg2Image(img, bridge):

    image = Image()

    image.width = img.width
    image.height = img.height
    image.format = "RGB8"
    image.timeStamp = img.header.stamp.secs + (img.header.stamp.nsecs *1e-9)
    cv_image=0
    if (img.encoding[-2:] == "C1"):
        gray_img_buff = bridge.imgmsg_to_cv2(img, img.encoding)
        cv_image  = depthToRGB8(gray_img_buff, img.encoding)
    else:
        cv_image = bridge.imgmsg_to_cv2(img, "rgb8")
    image.data = cv_image
    return image

import numpy as np


class Image:

    def __init__(self):

        self.height = 3  # Image height [pixels]
        self.width = 3  # Image width [pixels]
        self.timeStamp = 0 # Time stamp [s] */
        self.format = "" # Image format string (RGB8, BGR,...)
        self.data = np.zeros((self.height, self.width, 3), np.uint8) # The image data itself
        self.data.shape = self.height, self.width, 3


    def __str__(self):
        s = "Image: {\n   height: " + str(self.height) + "\n   width: " + str(self.width)
        s = s + "\n   format: " + self.format + "\n   timeStamp: " + str(self.timeStamp) 
        s = s + "\n   data: " + str(self.data) + "\n}"
        return s 


class ListenerCamera:
 
    def __init__(self, topic):
        
        self.topic = topic
        self.data = Image()
        self.sub = None
        self.lock = threading.Lock()

        self.bridge = CvBridge()
        self.start()
 
    def __callback (self, img):

        image = imageMsg2Image(img, self.bridge)

        self.lock.acquire()
        self.data = image
        self.lock.release()
        
    def stop(self):

        self.sub.unregister()

    def start (self):
 
        self.sub = rospy.Subscriber(self.topic, ImageROS, self.__callback)
        
    def getImage(self):

        self.lock.acquire()
        image = self.data
        self.lock.release()
        
        return image

    def hasproxy (self):

        return hasattr(self,"sub") and self.sub


from geometry_msgs.msg import Twist


import time
from datetime import datetime

time_cycle = 80


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


import sys
import types
import yaml
#from web_sockets_server import getWebSocketServer ### cambiaaaaaaaaaaaaaaaaaaaaaaaar
import ssl
from SimpleWebSocketServer import WebSocket, SimpleSSLWebSocketServer, SimpleWebSocketServer

class SimpleWS(WebSocket):

    def handleMessage(self):
        pass

    def handleConnected(self):
        
        self.server.appendClient(self)

        print (self.address, 'connected')

    def handleClose(self):

        self.server.removeClient(self)

        print (self.address, 'disconnected')

class SimpleWSServer (SimpleWebSocketServer):
    def __init__(self, host, port, websocketclass, selectInterval = 0.1):

        SimpleWebSocketServer.__init__(self, host, port,
                                        websocketclass, selectInterval)

        self._lock_clients = threading.Lock()
        self._clients = []


    def close(self):
        super(SimpleWSServer, self).close()


    def serveforever(self):
        super(SimpleWSServer, self).serveforever()

    def appendClient(self, client):
        self._lock_clients.acquire()
        self._clients.append(client)
        self._lock_clients.release()

    def removeClient(self, client):
        self._lock_clients.acquire()
        self._clients.remove(client)
        self._lock_clients.release()

    def sendMessage(self, message):
        
        self._lock_clients.acquire()
        my_clients = list(self._clients)
        self._lock_clients.release()
        for client in my_clients:
            client.sendMessage(unicode(message, "utf-8"))


class ThreadingWSServer(threading.Thread):
    def __init__(self, host, port, websocketclass, selectInterval = 0.1):
        super(ThreadingWSServer, self).__init__()
        self._stop_event = threading.Event()
        self._server = SimpleWSServer(host, port, websocketclass, selectInterval)


    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def sendMessage(self, message):
        self._server.sendMessage(message)

    def run(self):
        self._server.serveforever()

class SimpleWSSServer (SimpleSSLWebSocketServer):
    def __init__(self, host, port, websocketclass, cert, key, version = ssl.PROTOCOL_TLSv1, selectInterval = 0.1):

        SimpleSSLWebSocketServer.__init__(self, host, port,
                                        websocketclass, cert, key, version, selectInterval)

        self._lock_clients = threading.Lock()
        self._clients = []


    def close(self):
        super(SimpleWSSServer, self).close()


    def serveforever(self):
        super(SimpleWSSServer, self).serveforever()

    def appendClient(self, client):
        self._lock_clients.acquire()
        self._clients.append(client)
        self._lock_clients.release()

    def removeClient(self, client):
        self._lock_clients.acquire()
        self._clients.remove(client)
        self._lock_clients.release()

    def sendMessage(self, message):
        
        self._lock_clients.acquire()
        my_clients = list(self._clients)
        self._lock_clients.release()
        for client in my_clients:
            client.sendMessage(unicode(message, "utf-8"))

class ThreadingWSSServer(threading.Thread):
    def __init__(self, host, port, websocketclass, cert, key, version = ssl.PROTOCOL_TLSv1, selectInterval = 0.1):
        super(ThreadingWSSServer, self).__init__()
        self._stop_event = threading.Event()
        self._server = SimpleWSSServer(host, port, websocketclass, cert, key, version, selectInterval)


    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def sendMessage(self, message):
        self._server.sendMessage(message)

    def run(self):
        self._server.serveforever()

def getWebSocketServer(host, port, ssl = False, cert=None, key=None, version = ssl.PROTOCOL_TLSv1):
    if ssl:
        return ThreadingWSSServer(host, port, SimpleWS, cert, key, version)
    else:
        return ThreadingWSServer(host, port, SimpleWS)

def readConfig():
    try:
        with open('local_follow_line.yml', 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        raise SystemExit('Error: Cannot read/parse YML file. Check YAML syntax.')
    except:
        raise SystemExit('\n\tFILE "local_follow_line.yml" DOES NOT EXIST\n')

class FollowLine():
    
    def __init__(self):
        cfg = readConfig()

        cameraTopic = cfg["Camera"]["Topic"]
        motorsTopic = cfg["Motors"]["Topic"]
        maxv = cfg["Motors"]["MaxV"]
        maxw = cfg["Motors"]["MaxW"]

        self.camera = ListenerCamera(cameraTopic)
        self.motors = PublisherMotors(motorsTopic, maxv, maxw)

        ssl = cfg["Websockets"]["SSL"]
        host = cfg["Websockets"]["Host"]
        port = int(cfg["Websockets"]["Port"])
        cert = cfg["Websockets"]["Cert"] 
        key = cfg["Websockets"]["Key"]
        #print(cert, key)

        self.wsserver = getWebSocketServer(host, port, ssl, cert, key)
        self.wsserver.start()
        self.algorithm=MyAlgorithm(self.camera, self.motors, self.wsserver)

        self.referee_start = rospy.ServiceProxy("refereeStart", Empty)
        self.referee_stop = rospy.ServiceProxy("refereeStop", Empty)

        print "Follow_Line Components initialized OK"

    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        self.referee_start()
        print "Follow_Line is running"
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Follow_Line has been paused"
         
    def stop(self):
        self.algorithm.stop()
        self.wssever.stop()
        self.referee_stop()
        print "Follow_Line stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm )
        print "Code updated"       

    def move(self):
        self.algorithm.move()
    
    def get_threshold_image(self):
        return self.algorithm.get_threshold_image()
    
    def get_color_image(self):
        return self.algorithm.get_color_image()

import math
import numpy as np
import matplotlib.pyplot as plt
import base64

def img2String(img):
    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    return "data:image/jpeg;base64, "+jpg_as_text

class MyAlgorithm(threading.Thread):

    def __init__(self, camera, motors, wsserver):
        self.camera = camera
        self.motors = motors
        self.wsserver = wsserver
        self.threshold_image = np.zeros((640,360,3), np.uint8)
        self.color_image = np.zeros((640,360,3), np.uint8)
        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)
    
    def getImage(self):
        self.lock.acquire()
        img = self.camera.getImage().data
        self.lock.release()
        return img

    def set_color_image (self, image):
        img  = np.copy(image)
        #if len(img.shape) == 2:
        #  img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.color_image_lock.acquire()
        self.color_image = img
        self.color_image_lock.release()
        imgStr = img2String(img)
        self.wsserver.sendMessage(imgStr)
        #plt.axis('off') # printImage
        #a = plt.imshow(img)
        #time.sleep(0.1)

        
    def get_color_image (self):
        self.color_image_lock.acquire()
        img = np.copy(self.color_image)
        self.color_image_lock.release()
        return img
        
    def set_threshold_image (self, image):
        img = np.copy(image)
        #if len(img.shape) == 2:
        #  img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.threshold_image_lock.acquire()
        self.threshold_image = img
        self.threshold_image_lock.release()
        #plt.axis('off') # printImage
        #a = plt.imshow(img)
        #time.sleep(0.1)
        imgStr = img2String(img)
        self.wsserver.sendMessage(imgStr)
        
    def get_threshold_image (self):
        self.threshold_image_lock.acquire()
        img  = np.copy(self.threshold_image)
        self.threshold_image_lock.release()
        return img

    def run (self):

        while (not self.kill_event.is_set()):
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
        image = self.getImage()
        self.set_color_image(image)


def printImage(image):
    plt.axis('off')
    a = plt.imshow(image)
    plt.show()
