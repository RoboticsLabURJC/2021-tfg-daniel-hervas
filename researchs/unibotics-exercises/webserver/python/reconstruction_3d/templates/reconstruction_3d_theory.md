# 3D reconstruction

<img src="{% static 'python/reconstruction_3d/img/reconstruction_1.png' %}" width="60%" height="60%">

## 1. Introduction

Cameras are usual sensors in robot's equipment. Many robots use vision to perceive their environment. For instance mobile robots may use vision to detect obstacles around and to measure the distance to them. Navigation algorithms may then employ such distances to perform obstacle avoidance.

Obtaining such distances, the visual 3D reconstruction from images, can be solved using RGBD sensors (like Kinect, LIDAR cameras...) or even stereo cameras. In **this exercise** you will learn the **classic algoritm to compute the 3D reconstruction from the images of two simple cameras in stereo pair**, to obtain geometric information from the visual data in images.

This classic algorithm uses pin-hole camera model. It also requires calibrated cameras and texture in the scene. It basically consists of **three steps**: 

- Computation of interest points in one image.
- Matching pixels from left and right images.
- Triangulation to estimate depth, 3D points. 

Some real stereo cameras, like BumbleBee, just perform this algorithm in an electronic circuit.



## 2. Infrastructure

This section breaks down the parts of which the year is made up as follows

### 2.1.- Gazebo simulator

The Gazebo simulator will be used to know the position of the robot in the world. This allows to move the robot to position it in another area of the scene and perform the reconstruction from another perspective.



<img src="{% static 'python/reconstruction_3d/img/reconstruction_2.png' %}" width="60%" height="60%">

### 2.2. Viewers

In this exercise there are several viewers.

In the **upper right** part (next to the simulator) there is a viewer where you can **send content**, for example process an image or project text (using OpenCV) to know the state of variables.

In the **middle** a bigger viewer. This is the **main core of the** viewers since the points you are calculating are projected in space. 

Finally, in the **lower part** you have the **visualization of the stereo pair** of the cameras of the robot (left image and right image). Using the libraries provided by the API you can make point **matches** between both images.



<img src="{% static 'python/reconstruction_3d/img/thumbnail_reconstruction_3d.png' %}" width="50%" height="60%">

## 3. API

- To get the images from the cameras:

  ```python
  imageLeft = self.getImageLeft()
  imageRight = self.getImageRight()
  ```

- To send the camera images to viewer:

  ```python
  self.setImageFiltered(imageLeft)
  ```

- To show matches between the left and right image:

    ```python
    self.showMatches(imageLeft,imageRight,matches)
    ```

- To draw points in 3D world:

  ```python
  self.drawPoint(point,color)
  ```

  