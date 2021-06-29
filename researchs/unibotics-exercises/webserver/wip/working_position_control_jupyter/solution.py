
''' UPDATE METHOD FOR PID CLASS '''
def pid(self, current_value):
    self.error = self.set_point - current_value
    self.P_value = self.Kp * self.error
    self.D_value = self.Kd * ( self.error - self.Derivator)
    self.Derivator = self.error

    self.Integrator = self.Integrator + self.error

    if self.Integrator > self.Integrator_max:
        self.Integrator = self.Integrator_max
    elif self.Integrator < self.Integrator_min:
        self.Integrator = self.Integrator_min

    self.I_value = self.Integrator * self.Ki

    PID = self.P_value + self.I_value + self.D_value
    return PID
      

''' EXECUTE METHOD FOR ALGORITHM CLASS '''
def execute(self):
    self.actualBeacon=self.getNextBeacon()
    if self.actualBeacon == None:
        self.reset()
        self.actualBeacon=self.getNextBeacon()

    if self.actualBeacon.isActive() == False:
        print ('Actual beacon is: {}'.format(self.actualBeacon.getId()))
        self.xPid.set_point = self.actualBeacon.getPose().x
        self.xPid.Integrator = 0
        self.xPid.Derivator = 0
        self.yPid.set_point = self.actualBeacon.getPose().y
        self.yPid.Integrator = 0
        self.yPid.Derivator = 0
        self.actualBeacon.setActive(True)

    if self.actualBeacon.isReached()==False:
        droneX=self.pose.getPose3d().x
        droneY=self.pose.getPose3d().y
        valueX = self.xPid.update(droneX)
        valueY = self.yPid.update(droneY)
        print(valueX)
        self.cmdvel.sendCMDVel(valueX,valueY,0,0,0,0)
        errorX = self.xPid.error
        errorY = self.yPid.error

        if abs(errorX) < self.minError and abs(errorY) < self.minError:
            print ('{} has been reached'.format(self.actualBeacon.getId()))
            self.actualBeacon.setReached(True)
            

