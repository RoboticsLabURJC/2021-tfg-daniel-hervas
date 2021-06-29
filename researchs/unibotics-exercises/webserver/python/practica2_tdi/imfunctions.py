# -*- coding: utf-8 -*-
"""
Función para añadir ruido

parameters:
    img: uint8 black and white img
    noise: The type of noise, the options are 'gauss' for Gaussian noise,
        'sandp' for salt and pepper noise
    par: This are the parameters that define the noise, in the case of
        Gaussian is a Touple of mean and variance and in salt and pepper
        is density
"""
import numpy as np
import cv2
import math

def im2double(im):
    info = np.iinfo(im.dtype) # Get the data type of the input image
    return im.astype(np.float) / info.max # Divide all values by the largest
                                          #possible value in the datatype
                                          
def imdoublefloat2uint8(im):
    im = im*255
    return im.astype(np.uint8)

def imnoise(img, noise = "gauss", par = [0,0.01]):
    
    imgd = im2double(img)
    
    if noise == "gauss":
        h,w = img.shape
        m, v = par
        nmat = np.random.standard_normal(size=(h,w))
        nmat = math.sqrt(v)*nmat + m
        noisy = imgd + nmat
        
        noisy = imdoublefloat2uint8(noisy)
        return noisy
        
    elif noise == "sandp":
        d = par*0.5   #The parameter indicates total density, divide by two
                      # to get salt density and pepper density
        numpix =np.ceil(d* img.size) #The total number of pixels affected
        h, w = img.shape
        numpix = numpix.item()
        out = np.copy(imgd)
        
        #get noise coords
        
        saltx = np.random.randint(0, h-1, int(numpix))
        salty = np.random.randint(0, w-1, int(numpix))
        pepperx = np.random.randint(0, h-1, int(numpix))
        peppery = np.random.randint(0, w-1, int(numpix))
        
        for i in range(0, int(numpix)-1):
            
            out[saltx[i],salty[i]] = 1
        
            out[pepperx[i],peppery[i]] = 0
        
        print('out double')
        print(out)
        out = imdoublefloat2uint8(out)
        print('out uint 8')
        print(out)
        return(out)
    
    elif noise == "speckle":
        
        v = par
        h,w = img.shape
        nmat = np.random.uniform(-0.5, 0.5, (h,w))
        print(nmat.shape)
        noisy = imgd + math.sqrt(12*v)*np.multiply(imgd,nmat);
        noisy = imdoublefloat2uint8(noisy)
        return noisy
        
    else:
        print("Incorrect argument fo noise")
        return(img)
        
img = np.matrix([[127, 32, 24, 36, 80, 95],[127, 32, 46, 36, 80, 95],[127, 32, 100, 36, 80, 95],[64, 255, 8, 12, 25, 67]], dtype = 'uint8')
print(img)
imnoise(img, "speckle", 0.1)