def execute(self):

    if not self.initialized:

        self.StopTaxi = False
        self.goForward = False
        self.turn1 = False
        
        self.startTime = 0
        self.startTimePark = 2
        
        self.DIST_REAR_SPOT = 6.3
        self.DIST_REAR_CARY = 4.2
        self.DIST_REAR_CARX = 2.2
        self.DIST_RIGHT = 3.5
        self.MARGIN1 = 0.2
        self.MARGIN2 = 0.15
        self.YAW_MAX = 1.05
        self.YAW_MARGIN = 0.02
        self.DIST_MAX = 20

        self.initialized = True

    # Get the position of the robot
    xCar = self.pose3d.getPose3d().x
    yCar = self.pose3d.getPose3d().y
    
    # We get the orientation of the robot with respect to the map
    yawCar = self.pose3d.getPose3d().yaw

    # Get the data of the laser sensor, which consists of 180 pairs of values
    laser_data_Front = self.laser1.getLaserData()
    laserFront = []
    for i in range(laser_data_Front.numLaser):
        dist = laser_data_Front.distanceData[i]/1000.0
        angle = math.radians(i)
        laserFront += [(dist, angle)]
    
    laser_data_Rear = self.laser2.getLaserData()
    laserRear = []
    for i in range(laser_data_Rear.numLaser):
        dist = laser_data_Rear.distanceData[i]/1000.0
        angle = math.radians(i)
        laserRear += [(dist, angle)]
    
    laser_data_Right = self.laser3.getLaserData()
    laserRight = []
    for i in range(laser_data_Right.numLaser):
        dist = laser_data_Right.distanceData[i]/1000.0
        angle = math.radians(i)
        laserRight += [(dist, angle)]
        
    lasers = [laserFront, laserRear, laserRight]
    lasers_vectorized = []
    for l in lasers: 
        laser_vectorized = []
        for d,a in l:
            x = d * math.cos(a) * -1
            y = d * math.sin(a) * -1
            v = (x,y)
            laser_vectorized += [v]
        lasers_vectorized += [laser_vectorized]

    laserFront_vectorized = lasers_vectorized[0]
    laserRear_vectorized = lasers_vectorized[1]
    laserRight_vectorized = lasers_vectorized[2]
    
    # Average of the 180 values of the laser
    laserFront_mean = np.mean(laserFront_vectorized, axis=0)
    laserRear_mean = np.mean(laserRear_vectorized, axis=0)
    laserRight_mean = np.mean(laserRight_vectorized, axis=0)
    
    if self.StopTaxi == False:
        if(self.DIST_RIGHT-self.MARGIN1)<=abs(laserRight_mean[1])<=(self.DIST_RIGHT+self.MARGIN1) and (self.DIST_REAR_SPOT-self.MARGIN1)<=abs(laserRear_mean[1])<=(self.DIST_REAR_SPOT+self.MARGIN1):
            # If the taxi is alligned with the car in front of the parking spot the taxi stops
            self.motors.sendV(0)
            self.StopTaxi = True
            if self.startTime == 0:
                self.startTime = time.time()
        else:
            # If the taxi did not get to the car ahead, the taxi drives forward
            self.motors.sendV(20)
    else:
        if (time.time() - self.startTime) <= self.startTimePark:
            # The taxi stopped for a while
            self.motors.sendV(0)
        else:
            if self.goForward == False:
                # The taxi goes backward
                if yawCar <= self.YAW_MAX and self.turn1 == False:
                    # The car is getting into the parking space
                    self.motors.sendV(-3)
                    self.motors.sendW(math.pi/4)
                else:
                    # The taxi straightens
                    self.turn1 = True
                    self.motors.sendV(-3)
                    self.motors.sendW(-math.pi/7)
                
                if (self.DIST_REAR_CARY-self.MARGIN2) <= abs(laserRear_mean[1]) <= (self.DIST_REAR_CARY+self.MARGIN2):
                    # If the taxi is very close to the car from behind, it stop
                    self.goForward = True
                    self.motors.sendV(0)
                    self.motors.sendW(0)
            else:
                if yawCar <= -self.YAW_MARGIN or yawCar >= self.YAW_MARGIN:
                    # The taxi rectifies
                    self.motors.sendV(1)
                    self.motors.sendW(-math.pi/2)
                else:
                    # When the car is straight, it stops and rectifies until it is centered in the parking spot
                    self.motors.sendW(0)
                    if (laser_data_Front.distanceData[90]/10 - laser_data_Rear.distanceData[90]/10) > self.DIST_MAX:
                        self.motors.sendV(2)
                    elif (laser_data_Rear.distanceData[90]/10 - laser_data_Front.distanceData[90]/10) > self.DIST_MAX:
                        self.motors.sendV(-2)
                    else:
                        # The taxi is parked
                        print('CAR PARKED')
                        self.motors.sendV(0)

