#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/usr/lib/python2.7/')
import types
import rospy
from std_srvs.srv import Empty
import time
import cv2
import numpy as np

from MyAlgorithm import MyAlgorithm
import config
import comm
import yaml
from Camera.threadcamera import ThreadCamera
from cameraFilter import CameraFilter
from IPython.display import clear_output


def selectVideoSource(cfg):
    """
    @param cfg: configuration
    @return cam: selected camera
    @raise SystemExit in case of unsupported video source
    """
    source = cfg['Introrob']['Source']
    if source.lower() == 'local':
        from Camera.local_camera import Camera
        cam_idx = cfg['Introrob']['Local']['DeviceNo']
        print('  Chosen source: local camera (index %d)' % (cam_idx))
        cam = Camera(cam_idx)
    elif source.lower() == 'video':
        from Camera.local_video import Camera
        video_path = cfg['Introrob']['Video']['Path']
        print('  Chosen source: local video (%s)' % (video_path))
        cam = Camera(video_path)
    elif source.lower() == 'stream':
        # comm already prints the source technology (ICE/ROS)
        import comm
        import config
        cfg = config.load('color_filter_conf.yml')
        jdrc = comm.init(cfg, 'Introrob')
        proxy = jdrc.getCameraClient('Introrob.Stream')
        from Camera.stream_camera import Camera
        cam = Camera(proxy)
    else:
        raise SystemExit(('%s not supported! Supported source: Local, Video, Stream') % (source))

    return cam


def readConfig():
    try:
        with open('color_filter_conf.yml', 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        raise SystemExit('Error: Cannot read/parse YML file. Check YAML syntax.')
    except:
        raise SystemExit('\n\tFILE "color_filter_conf.yml" DOES NOT EXIST\n')

class ColorFilter ():
    def __init__(self):

        cfg = readConfig()
        self.camera = selectVideoSource(cfg)
        # Threading the camera...
        t_cam = ThreadCamera(self.camera)
        t_cam.start()

        self.algorithm = MyAlgorithm(self.camera)
        
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
                   
    def setExecute(self, ex):
        self.algorithm.func = ex
        def execute(self):
            self.func(self)
            # print filtered image each 30 interations
            if (self.visualizationIterator % 15) == 0 and self.visualizationEnabled:
                if self.filtered_image.any():
                    clear_output()
                    self.displaybuttons()
                    self.printFilteredImage()
                else:
                    print
                    print "//////////////////////////////////// "
                    print "You haven't set any Filtered Image!!"
                    print "//////////////////////////////////// "
                    print

        self.algorithm.algorithm = types.MethodType(execute, self.algorithm)
        print "Code updated"       
        
    def get_filtered_image (self):
        return self.algorithm.get_filtered_image()
    
    def get_color_image (self):
        return self.algorithm.get_color_image()
        
