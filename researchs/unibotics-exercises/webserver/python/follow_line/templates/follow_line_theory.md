# Follow Line Practice
<img src="{% static 'python/follow_line/img/follow_line_f1.png' %}" width="100%" height="100%" style="float:left;padding-right:15px"/>



## 1- Introduction

In this exercise we are going to implement a "Formula 1" intelligence to **follow a red line** across the circuit. To do it, the student needs to have at least the next knowledge:

- Python programming skills.
- [Color spaces](https://en.wikipedia.org/wiki/Color_space) (RGB, HSV, etc).
- Basic understanding of [OpenCV library](https://docs.opencv.org/2.4/modules/refman.html).



## 2- Exercise components

### 2.1- Gazebo simulator

The gazebo simulator will be running on the right side of the window.. The Gazebo world employed for this exercise has one element: **a simulated Formula 1 car robot**. The Formula 1 robot will provide camera where the images will be provided to the student.

<img src="{% static 'python/follow_line/img/f1_overview.png' %}" width="100%" height="100%" style="float:left;padding-right:15px"/>



### 2.2 Follow Line Component

This component has been developed specifically to carry out this exercise. This component connects to Gazebo to teleoperate the Formula 1 (or send orders to it) and receives images from its camera. The student has to modify this component and add code to accomplish the exercise. In particular, it is required to modify the `execute()` method.

<img src="{% static 'python/follow_line/img/f1_first_person.png' %}" width="100%" height="100%" style="float:left;padding-right:15px"/>



##  3 - API

The orders that the formula 1 admits are the following:

- To get the images from the camera:

```python
input_image = self.getImage()
```

- To move the robot:

```python
self.motors.sendV(10)
self.motors.sendW(5)
```

- To change the image inRGB to HSV:

```python
image_HSV = cv2.cvtColor()
```

- To filter the red values :

```python
value_min_HSV = np.array([0, 235, 60])
value_max_HSV = np.array([180, 255, 255])
```

- To filter the images:

```python 
image_HSV_filtered = cv2.inRange()
```

- To create a mask with the red values:

```python
image_HSV_filtered_Mask = np.dstack(())
```

- To get the numbers of the image rows and columns:

```python
size = input_image.shape
```

- To get the pixels that change of tone:

```python
position_pixel_left = []
position_pixel_right  = []
```

After that you must calculate the middle position of the road and then, calculate the desviation of the car:

```python
desviation = position_middle - (columns/2)
```

Then, depending on the desviation, you should correct the position of the car. 

- To save the camera image:

```python
self.set_color_image(input_image)
```

- To save the filtered image:

```python
self.set_threshold_image(image_HSV_filtered_Mask)
```

- To obtain an image of the cameras, the data is first saved and then displayed. You can use these instructions to display the contents of the cameras.

```python
 def execute(self):
    img = self.getImage()
    self.set_color_image(img)
    
fl.setExecute(execute)
```

You can use the following instructions to show the filtered images. **Note: The image must be on RGB or Gray Scale color model. Other formats is not allowed.**

```python
 def execute(self):
    img = self.getImage()
    self.set_threshold_image(img)
    
fl.setExecute(execute)
```

Are you able to complete a lap of the circuit? **Go for it**.

<img src="{% static 'python/follow_line/img/circuit.png' %}" width="100%" height="100%" style="float:left;padding-right:15px"/>