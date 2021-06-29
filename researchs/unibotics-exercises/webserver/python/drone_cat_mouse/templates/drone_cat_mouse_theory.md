# Drone cat mouse



<img src="{% static 'python/drone_cat_mouse/img/drone_cat_mouse.png' %}" width="60%" style="text-align: center">



## 1- Introduction

- In this exercise we are going to implement a "Drone" intelligence to **follow a red drone**. To do it, the student needs to have at least the next knowledge:
  - Python programming skills
  - [Color spaces](https://en.wikipedia.org/wiki/List_of_color_spaces_and_their_uses) (RGB, HSV, etc)
  - Basic understanding of [OpenCV library](https://docs.opencv.org/2.4/modules/refman.html)



## 2- Exercise components

### 2.1- Gazebo simulator

Gazebo simulator will be running in the background. The Gazebo world employed for this exercise has one element: a simulated black drone robot (cat) and red drone (mouse).The cat will provide camera where the images will be provided to the student.

### 2.2 Drone Cat Mouse Component

This component has been developed specifically to carry out this exercise. This component connects to Gazebo to teleoperate the Cat (or send orders to it) and receives images from its camera. The student has to modify this component and add code to accomplish the exercise. In particular, it is required to modify the `execute()` method.

<img src="{% static 'python/drone_cat_mouse/img/intro.png' %}" width="50%" style="text-align: center">



## 3- Exercise initialization

In the left part of the window is the theory and the cells of Jupyter code (you can switch between one and the other by clicking on the icon in the top bar). On the right side of the window is the Gazebo simulator with the world containing drones.

**Part of the code shown below is already available in the Jupyter cells.**

To start executing the exercise code you have to import the necessary files.

```python
from drone_cat_mouse import Cat
```

To start coding, we need to call Cat class once. Run this code and wait a few seconds until cat initialization finishes with an OK message:

```python
%matplotlib inline
cat = Cat()
```

Now we can start coding to give intelligence to the Drone. We can do it modifying the `execute()` method from drone cat mouse component. This method will be called iteratively. Each iteration, we'll print a message.

```python
# Implement execute method
def execute(self):
    print "Running execute iteration"
      
cat.setExecute(execute)
cat.play()
```

Stop printing the updating of the method with an empty instruction:

```python
def execute(self):
    pass

cat.setExecute(execute)
```



##  4 - API

- To get the images from the cameras:

  - `input_image = self.getImage()`

- To switch between front and ventral image:

- - `input_image = self.drone.toggleCam()`

- To takeoff and land the drone:

  - `self.drone.takeoff()`
  - `self.drone.land()`

- To move the robot:

  - `self.drone.sendCMDVel(vx,vy,vz,ax,ay,az)`

- To change the image inRGB to HSV:

  - `image_HSV = cv2.cvtColor()`

- To filter the red values:

  - `value_min_HSV = np.array([0, 235, 60])`
  - `value_max_HSV = np.array([180, 255, 255])`

- To filter the images:

  - `image_HSV_filtered = cv2.inRange()`

- To create a mask with the red values:

  - `image_HSV_filtered_Mask = np.dstack(())`

- To get the numbers of the image rows and columns:

  - `size = input_image.shape`

- To get the pixels that change of tone:

  - `position_pixel_left = []`
  - `position_pixel_right = []`

- After that you must calculate the middle position of the road and then, calculate the deviation of the drone:

  - `desviation = position_middle - (columns/2)`

  Then, depending on the desviation, you should correct the position of the drone.

- To save the camera image:

  - `self.set_color_image_ventral(input_image)`

- To save the filtered image:

  - `self.set_threshold_image_frontal(image_HSV_filtered_Mask)`

- To pause/resume the world:

  - `cat.pause()`
  - `cat.resume()`

- To obtain an image of the cameras, the data is first saved and then displayed. You can use these instructions to display the contents of the cameras.

  - ```
    def execute(self):
        img = self.drone.getImageFrontal()
        self.set_color_image(img)
        
    cat.setExecute(execute)
    ```

- You can use the following instructions to show the filtered images:

  - ```python
    def execute(self):
        img = self.getImageVentral()
        self.set_threshold_image_ventral(img)
        
    cat.setExecute(execute)
    ```

- Or

  - ```python
    def execute(self):
        segmentedImage = cat.get_threshold_image_frontal()
        self.set_threshold_image_frontal(segmentedImage)
        
    cat.setExecute(execute)
    ```

<img src="{% static 'python/drone_cat_mouse/img/drone_cat_mouse_image_processed.gif' %}" width="60%" style="text-align: center">

