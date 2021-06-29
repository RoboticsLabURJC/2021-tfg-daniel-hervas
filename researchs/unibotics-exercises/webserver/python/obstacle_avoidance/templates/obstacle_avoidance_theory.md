# Obstacle avoidance


<img src="{% static 'python/obstacle_avoidance/img/obstacle_2.png' %}" width="60%" style="text-align: center"/>



## 1 - Introduction
The objective of this practice is to implement the logic of the [VFF navigation algorithm](http://www-personal.umich.edu/~johannb/vff&vfh.htm) to control a F1 Robot as the one shown in the next image.


<img src="{% static 'python/obstacle_avoidance/img/f1_overview.png' %}" width="60%" style="text-align: center"/>


Navigation using VFF (Virtual Force Field), consists of:
- Each object in the environment generates a repulsive force towards the robot.
- Destiny generates an attractive force in the robot.

This makes it possible for the robot to go towards the target, distancing itself of the obstacles, so that their address is the vector sum of all the forces.

For this practice a world has been designed for the Gazebo simulator (see section 2.1). The main task will consist of making the robot reach its destiny without crashing with any obstacle. Some other extra tasks can be implemented, and are detailed at [1.1](#extra).

To do so, the student needs to have at least the next knowledge:

* Ease with operations with vectors
* Python programming skills
* Basic understanding of [OpenCV library](http://opencv.org/)


###  1.1 Extra tasks

The solution can integrate one or more of the following levels of difficulty, as well as any other one that occurs to you:

* Go as quickly as possible
* Choose the safest way
* Obstacles in movement
* Robustness in situations of indecision (zero vector sum)


##  2 - Exercise components

<img src="{% static 'python/obstacle_avoidance/img/circuitobstacles.png' %}" width="50%" height="50%" style="float:right;padding-right:10px;margin-top:35px;padding-left:10px;padding-bottom:7px;"/>


### 2.1 Gazebo Simulator

Gazebo simulator will be running in the background. The Gazebo world employed for this exercise has a 3D model of a simple F1 circuit, with some obstacles arranged in a predefined way and distributed throughout it. These obstacles are the ones shown in the following image:


<img src="{% static 'python/obstacle_avoidance/img/obstacle.png' %}" width="20%" style="text-align: center"/>


The other component of the simulated world is the f1 car robot that your algorith will have to control. This robot will provide images thorugh its <font color=red>two cameras</font> (Right and Left) that the student will have to process and a laser sensor where the walls and the obstacles will be detected. __Feel free to use the sensor of the robot with which it is easier to approach the practice, or even to combine the information captured by both to improve the result.__
We recommend using the laser sensor data in this case for the basic version of the practice, and using the images of the two cameras for debugging purposes.

### 2.1 Obstacle Avoidance Component

<img src="{% static 'python/obstacle_avoidance/img/obstacle_1.png' %}" width="50%" style="text-align: center"/>


This component has been developed specifically to carry out this exercise. This component connects to Gazebo to communicate with the f1 (send orders to it and receive sensors data). The student has to modify this component and add code to accomplish the exercise. In particular, it is required to modify the execute() method.

### 2.3 Obstacle Avoidance GUI

<img src="{% static 'python/obstacle_avoidance/img/obstacle_avoidance_gui.png' %}" width="30%" style="text-align: center"/>


This component is meant for you to **debug** your algorithm. The GUI let you see in a graphic way the sensing data the f1 is reading. You can see laser scan information (light blue color lines) which **will help you understand what the f1 is "seeing"** through its laser sensor. In addition, you can specify the VFF's algorithm forces here, so you will be able to see if the robot's behaviour is correct or not based on you algorithm. For this, you have 3 different vectors (green, red and magenta) which represents the different VFF's forces (you can see this in the legend at the bottom right corner of the GUI): 
* **Green vector**: represents the attractive force of the VFF.
* **Red vector**: represents the repulsive force of the VFF.
* **Magenta vector**: represents the resultant force of the VFF.

Lastly, you have a several circumferences showing distance data, so you can know how close the obstacles to adjust you algorithm.


## 3. API.

The robot admits the following instruction:

- To get the position of the robot (x coordinate).

  - ```python
    pose3d.getPose3d().x
    ```

- To obtain the position of the robot (y coordinate).

  - ```python
    pose3d.getPose3d().y
    ```

- To get the orientation of the robot with regarding the map.

  - ```python
    pose3d.getPose3d().yaw
    ```

- To obtain laser sensor data It is composed of 180 pairs of values: (0-180º distance in millimeters).

  - ```python
    laser.getLaserData().values
    ```

- To set and send the linear speed.

  - ```python
    motors.sendV()
    ```

- To set and send the angular velocity.

  - ```python
    motors.sendW()
    ```



### 3.1 Own API.

To simplify, the implementation of control points is offered. To use it, only two actions must be carried out:

1. Obtain the following point: 
   - `self.currentTarget = self.getNextTarget()`
2. Mark it as visited when necessary: 
   - `self.currentTarget.setReached(True)`



## 3.2. Conversion of types

### Laser's API:

- To get the laser data (wich consists of 180 pairs of values), use:
```
laser_data = self.laser.getLaserData()
```
We provide the code necessary to parse this data:
```
laser = []
for i in range(laser_data.numLaser):
    dist = laser_data.distanceData[i]/1000.0
    angle = math.radians(i)
    laser += [(dist, angle)]
```
Now, your laser_data variable will be a list with 180 positions that contain bth the angle of the laser beam and the distance to the point where the beam hit.



### Target's API:

We provide a Python class that contains different destinations arranged along the circuit to make it easier to create a route to follow, so that you can concentrate on avoiding obstacles and on how not to lose the course. You should start your code with:

- To get the next target to reach.
    ```python
    self.currentTarget = self.getNextTarget()
    ```
- To get x coordinate of the next target.
    ```python
    self.targetx = self.currentTarget.getPose().x
    ```

-  To get y coordinate of the next target.
    ```python
    self.targety = self.currentTarget.getPose().y
    ```

- Once you think the next target has been reached, just write:
    ```python
    self.currentTarget.setReached(True)
    ```


### Robot's API:

Finally, here is the way to get robot's position information:

- x coordinate:
    ```
    rx = self.pose3d.getPose3d().x/1000
    ```
- y coordinate:
    ```python
    ry = self.pose3d.getPose3d().y/1000
    ```
- Rotation with respect the map.
    ```python
    rt = self.pose3d.getPose3d().yaw
    ```

- And to send orders to it:
    - Send linear speed:
        ```python
        self.motors.sendV(speed).
        ```
    - Send angular speed:
        ```python
        self.motors.sendW(angle)
        ```



- Once you think the next target has been reached, just write:
    ```python
    self.currentTarget.setReached(True)
    ```



### 3.2.1. Coordinate system

```python
def absolute2relative (x_abs, y_abs, robotx, roboty, robott):
    
	# robotx, roboty are the absolute coordinates of the robot
	# robott is its absolute orientation
    # Convert to relatives
    dx = x_abs - robotx
    dy = y_abs - roboty

    # Rotate with current angle
    x_rel = dx * math.cos (-robott) - dy * math.sin (-robott)
    y_rel = dx * math.sin (-robott) + dy * math.cos (-robott)

return x_rel, and y_rel
```