
'''
///////////////////////////////////////////////////////////////////
            CALCULATE NEW GENERATION FUNCTION
///////////////////////////////////////////////////////////////////
'''
def calculateNewGeneration(self):

    print("new generation")
    if (not self.located):
        self.iteration += 1
        maxProb = 0.0;
        self.convergence = True;
        # Looking for the most likely particle
        for i in range(0,len(self.particles)):
            if (maxProb < self.particles[i].prob):
                maxProb = self.particles[i].prob
                center = self.particles[i] # greater prob
        # Checking if the generation converges
        for i in range(0,len(self.particles)):
            d = math.sqrt(math.pow(center.x-self.particles[i].x,2)+math.pow(center.y-self.particles[i].y,2))
            if (d > 2.0): # convergence translates into having all the particles inside a circle of radius 2
                self.convergence = False;

        if self.convergence or self.iteration >= 30:
            # Prediction in case of convergence or confused generation
            if center.prob >= 0.9:
                # Great Probability -> Prediction
                self.setEstimation((center.x,center.y))
                self.located = True;
            else:
                # Low Probbility -> Resample
                self.particles = []
                for i in range(self.numParticles):
                    randomX = None
                    randomY = None
                    randomYaw = None
                    prob = None
                    while True:
                        randomX = random.uniform(-5, -5+self.map.worldWidth)
                        randomY = random.uniform(-5, -5+self.map.worldHeight)
                        if self.isAvailable(randomX,randomY):
                            break
                    randomYaw =  random.uniform(-math.pi, math.pi)
                    p = Particle(randomX,randomY,randomYaw,0.0,self.map.robotAngle)
                    laserP = []
                    # Ray Tracing
                    for k in range (-90,90,22): # 8 laser beams
                        angle = p.yaw+math.radians(k)
                        stepx = 0.1*math.cos(angle)
                        stepy = 0.1*math.sin(angle)
                        x = p.x-0.15*math.cos(p.yaw)
                        y = p.y-0.15*math.sin(p.yaw)

                        while self.isWhitePixel(x,y):
                            x = x-stepx
                            y = y-stepy

                        dist = math.sqrt(math.pow((x-p.x),2)+math.pow(y-p.y,2))
                        laserP.append((dist, math.radians(k)))
                    # health function
                    error = 0.0
                    realLaser = self.parse_laser_data(self.laser.getLaserData())

                    for j in range(0,len(realLaser),22):
                        realDist = realLaser[j][0]
                        teoricalDist = laserP[j/22][0]
                        error += math.sqrt(math.pow(realDist-teoricalDist,2))

                    if error <= 4.5:
                        prob = 1.0-(error-1.0)*0.028
                    elif error > 4.5 and error <= 10.0:
                        prob = 0.9-(error-4.5)*0.146
                    else:
                        prob = math.exp(-0.23*error)

                    prob = min(prob, 1.0)

                    self.particles.append(Particle(randomX,randomY,randomYaw,prob,self.map.robotAngle))

        elif center.prob > 0.99:
            # In case of total coincidence with real data -> Prediction
            self.setEstimation((center.x,center.y))
            self.particles = [center]
            print("//////////////////////////////////////////////////////") 
            print("L O C A T E D   AT   ({},{})".format(center.x,center.y))
            print("Error: {} cm".format(math.sqrt(math.pow(center.x-self.pose3d.getPose3d().x,2)+math.pow(center.y-self.pose3d.getPose3d().y,2)*100)))
            print("//////////////////////////////////////////////////////") 
            self.located = True;
        else:
            # Rest of cases: Calculate New Generation Based on the Previous
            # Computation of cumulative probability (PAC)
            pac = 0.0
            for i in range(0,len(self.particles)):
                pac += self.particles[i].prob
            print ("pac: {}".format(pac))
            ## ROULETTE ALGORITHM
            if (pac <= 0.012*len(self.particles)):
                # Low PAC -> Resample
                elitism = []
                for i in self.particles:
                    if i.prob >= 0.7:
                        elitism.append(i) ## ELITISM
                # Resampling
                self.particles = []
                for i in range(self.numParticles):
                    randomX = None
                    randomY = None
                    randomYaw = None
                    prob = None
                    while True:
                        randomX = random.uniform(-5, -5+self.map.worldWidth)
                        randomY = random.uniform(-5, -5+self.map.worldHeight)
                        if self.isAvailable(randomX,randomY):
                            break
                    randomYaw =  random.uniform(-math.pi, math.pi)
                    p = Particle(randomX,randomY,randomYaw,0.0,self.map.robotAngle)
                    laserP = []
                    # Ray Tracing
                    for k in range (-90,90,22): # 8 laser beams
                        angle = p.yaw+math.radians(k)
                        stepx = 0.1*math.cos(angle)
                        stepy = 0.1*math.sin(angle)
                        x = p.x-0.15*math.cos(p.yaw)
                        y = p.y-0.15*math.sin(p.yaw)

                        while self.isWhitePixel(x,y):
                            x = x-stepx
                            y = y-stepy

                        dist = math.sqrt(math.pow((x-p.x),2)+math.pow(y-p.y,2))
                        laserP.append((dist, math.radians(k)))
                    # health function
                    error = 0.0
                    realLaser = self.parse_laser_data(self.laser.getLaserData())

                    for j in range(0,len(realLaser),22):
                        realDist = realLaser[j][0]
                        teoricalDist = laserP[j/22][0]
                        error += math.sqrt(math.pow(realDist-teoricalDist,2))

                    if error <= 4.5:
                        prob = 1.0-(error-1.0)*0.028
                    elif error > 4.5 and error <= 10.0:
                        prob = 0.9-(error-4.5)*0.146
                    else:
                        prob = math.exp(-0.23*error)

                    prob = min(prob, 1.0)

                    self.particles.append(Particle(randomX,randomY,randomYaw,prob,self.map.robotAngle))
                d = 0
                for el in elitism:
                    d += 1
                    self.particles.pop(d)
                    self.particles.append(el)
                    
            else:
                # Acceptable PAC -> Thermal Noise
                progenitors = []
                for a in range(0,len(self.particles)):
                    roulette = random.uniform(0.0, pac)
                    beginning = 0
                    for b in range(0,len(self.particles)):
                        end = beginning+self.particles[b].prob
                        if roulette >= beginning and roulette < end:
                            selectedParticle = self.particles[b]
                            break
                        else:
                            beginning = end
                    progenitors.append(selectedParticle)
                newParticles = []
                # particles filter
                for t in range(0,len(progenitors)):
                    if progenitors[t] and self.isAvailable(progenitors[t].x, progenitors[t].y):
                        if (progenitors[t].prob >= 0.82): ## ELITISM
                            if (random.randint(0,2)>1):   # Sometimes the Progenitor Particle is Copied
                                newParticle = copy.deepcopy(progenitors[t])
                            else:                         # Other times, thermal noise is applied
                                while True:
                                    # Thermal noise, centered in progenitors coordinates
                                    newX = np.random.normal(progenitors[t].x,0.1)
                                    newY = np.random.normal(progenitors[t].y,0.1)
                                    if self.isWhitePixel(newX,newY):
                                        break;
                                newYaw = np.random.normal(progenitors[t].yaw,0.1)
                                # Observation Model || Health Function
                                p1 = Particle(newX,newY,newYaw,0.0,self.map.robotAngle)
                                teoricalLaser = []
                                for d in range (-90,90,22): # 8 laser beams
                                    angle = p1.yaw+math.radians(d)
                                    stepx = 0.1*math.cos(angle)
                                    stepy = 0.1*math.sin(angle)
                                    xs = p1.x-0.15*math.cos(p1.yaw)
                                    ys = p1.y-0.15*math.sin(p1.yaw)

                                    while self.isWhitePixel(xs,ys):
                                        xs = xs-stepx
                                        ys = ys-stepy

                                    dist = math.sqrt(math.pow((xs-p1.x),2)+math.pow(ys-p1.y,2))
                                    teoricalLaser.append((dist, math.radians(d)))

                                laserP = teoricalLaser 
                                error = 0.0
                                realLaser = self.parse_laser_data(self.laser.getLaserData())

                                for r in range(0,len(realLaser),22):
                                    realDist = realLaser[r][0]
                                    teoricalDist = laserP[r/22][0]
                                    error += math.sqrt(math.pow(realDist-teoricalDist,2))

                                if error <= 4.5:
                                    prob = 1.0-(error-1.0)*0.028
                                elif error > 4.5 and error <= 10.0:
                                    prob = 0.9-(error-4.5)*0.146
                                else:
                                    prob = math.exp(-0.23*error)

                                prob = min(prob, 1.0)
                                part = Particle(newX,newY,newYaw,prob,self.map.robotAngle)
                                newParticle = part
                        else:           
                            # Thermal noise
                            while True:
                                # Thermal noise, centered in progenitors coordinates
                                newX = np.random.normal(progenitors[t].x,0.1)
                                newY = np.random.normal(progenitors[t].y,0.1)
                                if self.isWhitePixel(newX,newY):
                                    break;
                            newYaw = np.random.normal(progenitors[t].yaw,0.1)
                            # Observation Model || Health Function
                            p2 = Particle(newX,newY,newYaw,0.0,self.map.robotAngle)
                            teoricalLaser = []
                            for f in range (-90,90,22): # 8 laser beams
                                angle = p2.yaw+math.radians(f)
                                stepx = 0.1*math.cos(angle)
                                stepy = 0.1*math.sin(angle)
                                xr = p2.x-0.15*math.cos(p2.yaw)
                                yr = p2.y-0.15*math.sin(p2.yaw)

                                while self.isWhitePixel(xr,yr):
                                    xr = xr-stepx
                                    yr = yr-stepy

                                dist = math.sqrt(math.pow((xr-p2.x),2)+math.pow(yr-p2.y,2))
                                teoricalLaser.append((dist, math.radians(f)))

                            laserP2 = teoricalLaser
                            error = 0.0
                            realLaser = self.parse_laser_data(self.laser.getLaserData())

                            for q in range(0,len(realLaser),22):
                                realDist = realLaser[q][0]
                                teoricalDist = laserP2[q/22][0]
                                error += math.sqrt(math.pow(realDist-teoricalDist,2))

                            if error <= 4.5:
                                prob = 1.0-(error-1.0)*0.028
                            elif error > 4.5 and error <= 10.0:
                                prob = 0.9-(error-4.5)*0.146
                            else:
                                prob = math.exp(-0.23*error)

                            prob = min(prob, 1.0)
                            part = Particle(newX,newY,newYaw,prob,self.map.robotAngle)
                            newParticle = part
                        newParticles.append(newParticle)  
                self.particles = newParticles
    else:
        # when located, restart the algorithm
        print("RESTARTING...")
        self.particles = []
        for i in range(self.numParticles):
            randomX = None
            randomY = None
            randomYaw = None
            prob = None
            while True:
                randomX = random.uniform(-5, -5+self.map.worldWidth)
                randomY = random.uniform(-5, -5+self.map.worldHeight)
                if self.isAvailable(randomX,randomY):
                    break
            randomYaw =  random.uniform(-math.pi, math.pi)
            p = Particle(randomX,randomY,randomYaw,0.0,self.map.robotAngle)
            laserP = []
            # Ray Tracing
            for k in range (-90,90,22): # 8 laser beams
                angle = p.yaw+math.radians(k)
                stepx = 0.1*math.cos(angle)
                stepy = 0.1*math.sin(angle)
                x = p.x-0.15*math.cos(p.yaw)
                y = p.y-0.15*math.sin(p.yaw)

                while self.isWhitePixel(x,y):
                    x = x-stepx
                    y = y-stepy

                dist = math.sqrt(math.pow((x-p.x),2)+math.pow(y-p.y,2))
                laserP.append((dist, math.radians(k)))
            # health function
            error = 0.0
            realLaser = self.parse_laser_data(self.laser.getLaserData())

            for j in range(0,len(realLaser),22):
                realDist = realLaser[j][0]
                teoricalDist = laserP[j/22][0]
                error += math.sqrt(math.pow(realDist-teoricalDist,2))

            if error <= 4.5:
                prob = 1.0-(error-1.0)*0.028
            elif error > 4.5 and error <= 10.0:
                prob = 0.9-(error-4.5)*0.146
            else:
                prob = math.exp(-0.23*error)

            prob = min(prob, 1.0)

            self.particles.append(Particle(randomX,randomY,randomYaw,prob,self.map.robotAngle))
        self.located = False;
        self.iteration = 0
        self.convergence = False;

    self.setParticles(self.particles)
        

'''
///////////////////////////////////////////////////////////////////
                        EXECUTE METHOD
///////////////////////////////////////////////////////////////////
'''    
def execute(self):
    
    # vars initiallization
    if not self.initiallized:
        self.particles = []
        self.particleClicked = None
        self.iteration = 0
        self.numParticles = 650
        self.posePrev = []
        self.sent = False
        self.convergence = False
        self.located = False
        self.initiallized = True

    if self.particles == []: 
        # Random SENDING
        self.particles = []
        for i in range(self.numParticles):
            randomX = None
            randomY = None
            randomYaw = None
            prob = None
            while True:
                randomX = random.uniform(-5, -5+self.map.worldWidth)
                randomY = random.uniform(-5, -5+self.map.worldHeight)
                if self.isAvailable(randomX,randomY):
                    break
            randomYaw =  random.uniform(-math.pi, math.pi)
            p = Particle(randomX,randomY,randomYaw,0.0,self.map.robotAngle)
            laserP = []
            # Ray Tracing
            for k in range (-90,90,22): # 8 laser beams
                angle = p.yaw+math.radians(k)
                stepx = 0.1*math.cos(angle)
                stepy = 0.1*math.sin(angle)
                x = p.x-0.15*math.cos(p.yaw)
                y = p.y-0.15*math.sin(p.yaw)

                while self.isWhitePixel(x,y):
                    x = x-stepx
                    y = y-stepy

                dist = math.sqrt(math.pow((x-p.x),2)+math.pow(y-p.y,2))
                laserP.append((dist, math.radians(k)))
            # health function
            error = 0.0
            realLaser = self.parse_laser_data(self.laser.getLaserData())

            for j in range(0,len(realLaser),22):
                realDist = realLaser[j][0]
                teoricalDist = laserP[j/22][0]
                error += math.sqrt(math.pow(realDist-teoricalDist,2))

            if error <= 4.5:
                prob = 1.0-(error-1.0)*0.028
            elif error > 4.5 and error <= 10.0:
                prob = 0.9-(error-4.5)*0.146
            else:
                prob = math.exp(-0.23*error)

            prob = min(prob, 1.0)

            self.particles.append(Particle(randomX,randomY,randomYaw,prob,self.map.robotAngle))

        # Unique Particle above the robot
        # -----------------------------------------------------------------
        #prob = self.calculateProb(self.pose3d.getPose3d().x,self.pose3d.getPose3d().y,self.pose3d.getPose3d().yaw)
        #self.particles = [Particle(self.pose3d.getPose3d().x,self.pose3d.getPose3d().y,self.pose3d.getPose3d().yaw,prob,self.map.robotAngle)]
        # -----------------------------------------------------------------
        self.setParticles(self.particles)
    
    if self.particleClicked is not None and not self.calculated:
        particle = self.particleClicked
        tLaser = []
        for i in range (-90,90,22): # 8 laser beams
            angle = particle.yaw+math.radians(i)
            stepx = 0.1*math.cos(angle)
            stepy = 0.1*math.sin(angle)
            x = particle.x-0.15*math.cos(particle.yaw)
            y = particle.y-0.15*math.sin(particle.yaw)

            while self.isAvailable(x,y):
                x = x-stepx
                y = y-stepy

            dist = math.sqrt(math.pow((x-particle.x),2)+math.pow(y-particle.y,2))
            tLaser.append((dist, math.radians(i)))

        print("Particle Probability: ", self.particleClicked.prob)
        self.map.parent.paintLaser(self.parse_laser_data(self.laser.getLaserData()))
        self.map.parent.paintLaser(tLaser)
        self.calculated = True

    # New generations each click on the button
    if self.newGeneration:
        self.newGen()
        self.newGeneration = False
