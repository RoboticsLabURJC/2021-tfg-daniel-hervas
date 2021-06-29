
import matplotlib.pyplot as plt
import numpy as np
import time

def printImage(image):
    plt.axis('off')
    a = plt.imshow(image)
    plt.show()

def printVideo(image):
    #plt.close()
    plt.axis('off')
    v = plt.imshow(image) #, block=False)
    plt.show()
    time.sleep(2)
    plt.close()
