#!/usr/bin/python
#-*- coding: utf-8 -*-

import rospy
import types
import subprocess
import time
import threading
from std_srvs.srv import Empty
import math
import config
import comm
import sys
import yaml
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

class Drone:
    def __init__(self, config_file, name, camera_name, extra_name, cmdvel_name, pose_name): 
        cfg = config.load(config_file)
        self._jdrc= comm.init(cfg, name)

        self.__camera = self._jdrc.getCameraClient(camera_name)
        self.__extra =  self._jdrc.getArDroneExtraClient(extra_name)
        self.__cmdvel = self._jdrc.getCMDVelClient(cmdvel_name)
        self.__pose3d = self._jdrc.getPose3dClient(pose_name)


    def getImage(self):
        return self.__camera.getImage()

    
    def takeoff(self):
        self.__extra.takeoff()
       
    def land(self):
        self.__extra.land()
    
    def toggleCam(self):
        self.__extra.toggleCam()
              
    def reset(self):
        self.__extra.reset()
        
    def record(self, record):
        self.__extra.record(record)

    def sendCMDVel (self, vx,vy,vz,ax,ay,az):
        self.__cmdvel.sendCMDVel(vx,vy,vz,ax,ay,az)

    def getPose3d(self):
        return self.__pose3d.getPose3d()

    def stop(self):
        self.__pose3d.stop()
        self.__camera.stop()
        self._jdrc.remove()
    
    def pause (self):
        #self.__cmdvel.pause()
        pass
        
    def resume (self):
        #self.__cmdvel.resume()
        pass

import cv2
import numpy as np
import matplotlib.pyplot as plt
import base64

def img2String(img):
    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    return "data:image/jpeg;base64, "+jpg_as_text

from datetime import datetime
time_cycle = 80

class MyAlgorithm(threading.Thread):

    def __init__(self, drone, wsserver):
        self.drone = drone
        self.wsserver = wsserver
        self.threshold_image= np.zeros((640,360,3), np.uint8)
        self.color_image= np.zeros((640,360,3), np.uint8)
        self.using_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.kill_event)
	self.using_event.set()
    
    def getImage(self):
        self.lock.acquire()
        img = self.drone.getImage().data
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
        #print(imgStr)
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
            self.using_event.wait()
            start_time = datetime.now()
            self.algorithm()
            finish_Time = datetime.now()
            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.kill_event.set()

    def play (self):
        if not self.is_alive():
            self.start()
            
    def pause (self):
        #self.using_event.clear()
        pass
        
        
    def resume(self):
        #self.using_event.set()
        pass

    def kill (self):
        self.kill_event.set()

    def algorithm(self):
        #GETTING THE IMAGES
        image = self.getImage()

        # Add your code here
        #print "Runing"

        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        #self.motors.setV(10)
        #self.motors.setW(5)

        #SHOW THE FILTERED IMAGE ON THE GUI
        self.set_color_image(image)

class Cat():
    
    def __init__(self,q=1):
        self.__mouses = [("/opt/jderobot/share/jderobot/mouses/trainning_mouse","/opt/jderobot/share/jderobot/mouses/trainning.cfg"),
                        ("/opt/jderobot/share/jderobot/mouses/q1_mouse", "/opt/jderobot/share/jderobot/mouses/q1.cfg"),
                        ("/opt/jderobot/share/jderobot/mouses/q2_mouse","/opt/jderobot/share/jderobot/mouses/q2.cfg")]


        yml_file = "local_cat.yml"
        cfg = config.load(yml_file)
        self.__q = q
        self.drone = Drone(yml_file,"Cat", "Cat.Camera","Cat.Extra", "Cat.CMDVel", "Cat.Pose3D")

        ssl = cfg.getProperty("Websockets.SSL")
        host = cfg.getProperty("Websockets.Host")
        port = int(cfg.getProperty("Websockets.Port"))
        cert = cfg.getPropertyWithDefault("Websockets.Cert", None)
        key = cfg.getPropertyWithDefault("Websockets.Key", None)

        self.wsserver = getWebSocketServer(host, port, ssl, cert, key)
        self.wsserver.start()
        self.algorithm=MyAlgorithm(self.drone, self.wsserver)
        self.pause_physics_client=rospy.ServiceProxy('/gazebo/pause_physics',Empty)
        self.unpause_physics_client = rospy.ServiceProxy('/gazebo/unpause_physics',Empty)
        self.referee_start = rospy.ServiceProxy("refereeStart", Empty)
        self.referee_stop = rospy.ServiceProxy("refereeStop", Empty)
        self.reset_world = rospy.ServiceProxy("/gazebo/reset_world", Empty)
        
        print "Cat Components initialized OK"

    def play(self):
        #self.drone.takeoff()
        if not self.algorithm.is_alive():
             self.mouse = subprocess.Popen(self.__mouses[self.__q])
        else:
            self.unpause_physics_client()
        self.referee_start()
        self.algorithm.play()
        print "Cat is running"

    def reset(self):
        self.mouse.kill()
        self.mouse = subprocess.Popen(("/opt/jderobot/share/jderobot/mouses/q1_mouse", "/opt/jderobot/share/jderobot/mouses/q1.cfg"))
        self.algorithm.pause()
        self.drone.land()
        self.reset_world() 
        #self.drone.takeoff()
        self.referee_start()
        time.sleep(3)
        self.algorithm.resume()


        
    def pause (self):
        self.pause_physics_client()
        self.drone.pause()
        self.algorithm.pause()
	#self.referee_control("pause")
        
        print "Cat has been paused"
        
    def resume (self):
        self.unpause_physics_client()
        self.algorithm.resume()
        self.drone.resume()
	#self.referee_control("resume")
        print "Cat has been resumed"
         
    def stop(self):
        self.algorithm.stop()
        self.wssever.stop()
        self.referee_stop()
        print "Cat stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm )
        print "Code updated"       

    def move(self):
        self.algorithm.move()
    
    def get_threshold_image(self):
        return self.algorithm.get_threshold_image()
    
    
    def get_color_image(self):
        return self.algorithm.get_color_image()

