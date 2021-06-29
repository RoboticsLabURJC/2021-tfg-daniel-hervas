
def execute(self):

    # Saving input image
    #input_image = self.getImage()
    #self.set_color_image(input_image)
    #input_image_copy = np.copy(input_image)

    if not self.has_position: 
        # initialization
        self.one=True
        self.velx = 0.0
        self.vely = 0.0
        self.init = [0.0,0.0]
        self.has_position = False
        self.cpos = 0
        self.cit = 0
        self.next = self.AREA[self.cpos]

        centroid = [0, 0];
        signedArea = 0.0;
        x0 = 0.0 # Current vertex X
        y0 = 0.0 # Current vertex Y
        x1 = 0.0 # Next vertex X
        y1 = 0.0 # Next vertex Y
        a = 0.0  # Partial signed area

        for i in range(len(self.AREA)):
          x0 = self.AREA[i][0]
          y0 = self.AREA[i][1]
          x1 = self.AREA[(i+1) % len(self.AREA)][0]
          y1 = self.AREA[(i+1) % len(self.AREA)][1]
          a = x0*y1 - x1*y0
          signedArea += a
          centroid[0] += (x0 + x1)*a
          centroid[1] += (y0 + y1)*a

        signedArea *= 0.5
        centroid[0] /= (6.0*signedArea)
        centroid[1] /= (6.0*signedArea)
        self.centroid = centroid
        self.search_done = False
        #self.searching = True
        self.finished = False
        self.faces = []

        global MAX_VEL
        MAX_VEL = 0.8
        global MAX_ITERATIONS
        MAX_ITERATIONS = 4
        global DIST_MARGIN
        DIST_MARGIN = 0.1
        global FACES_DIST
        FACES_DIST = 2.0

        print ("Centroid is:", self.centroid)
        print ("First target is:", self.next)
    
        #save initial position
        self.init[0] = self.pose.getPose3d().x
        self.init[1] = self.pose.getPose3d().y
        self.has_position = True

    # SEARCH PEOPLE
    # Check if we have reached last position
    dx = self.next[0] - self.pose.getPose3d().x
    dy = self.next[1] - self.pose.getPose3d().y
    dist = math.sqrt(dx*dx+dy*dy)
    if not dist <= DIST_MARGIN:
      self.searching = True
      
    else:
        # Get next position
        self.cpos = (self.cpos+1)%len(self.AREA)
        vcent = [self.centroid[0] - self.AREA[self.cpos][0], self.centroid[1] - self.AREA[self.cpos][1]]
        dcent = [vcent[0]*self.cit/MAX_ITERATIONS, vcent[1]*self.cit/MAX_ITERATIONS]
        self.next = [self.AREA[self.cpos][0]+dcent[0], self.AREA[self.cpos][1]+dcent[1]] 
        self.searching = True
        print "Change target to:", self.next
        # Add iteration
        if self.cpos == 0:
          self.cit += 1
          if self.cit > MAX_ITERATIONS:
            self.searching = False

    if not self.search_done and self.searching:
      # Read image
      im = self.getImage()

      #Convert to gray scale
      gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

      # Detect faces in the image
      faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20), flags = cv2.CASCADE_SCALE_IMAGE)

      #save face
      for (x, y, w, h) in faces:

        # saving segmented image
        #cv2.rectangle(input_image_copy,(x,y),(x+w,y+h),(255,0,0),2)
        #self.set_threshold_image(input_image_copy)

        found = False
        # Get position in 3D
        # Cam position
        cx = self.pose.getPose3d().x
        cy = self.pose.getPose3d().y
        cz = self.pose.getPose3d().z

        # Backproject point
        fdist = 187.3358
        u0 = 160.0
        v0 = 120.0
        vx = (float(y+h/2)-u0)/fdist
        vy = (float(x+w/2)-v0)/fdist
        vz = 1.0

        # Change to world coordinates
        # Get Rotation translation matrix
        qw = self.pose.getPose3d().q[0]
        qx = self.pose.getPose3d().q[1]
        qy = self.pose.getPose3d().q[2]
        qz = self.pose.getPose3d().q[3]
        RT = np.array([
            [1.0 - 2.0*qy*qy - 2.0*qz*qz, 2.0*qx*qy - 2.0*qz*qw, 2.0*qx*qz + 2.0*qy*qw, self.pose.getPose3d().x],
            [2.0*qx*qy + 2.0*qz*qw, 1.0 - 2.0*qx*qx - 2.0*qz*qz, 2.0*qy*qz - 2.0*qx*qw, self.pose.getPose3d().y],
            [2.0*qx*qz - 2.0*qy*qw, 2.0*qy*qz + 2.0*qx*qw, 1.0 - 2.0*qx*qx - 2.0*qy*qy, self.pose.getPose3d().z],
            [0.0, 0.0, 0.0, 1.0]])
        # Relative to absolute coordinates
        p = np.array([[vx],[vy],[vz],[1.0]])
        res = np.dot(RT,p)
        vx = res[0,0]
        vy = res[1,0]
        vz = res[2,0]
            
        # Solve equation (X-x1)/(x2-x1) = (Z-z1)/(z2-z1)
        # p1 = Cam position, p2 = Backprojected point, Z = 0
        Z = 0.0
        X = cx + (vx-cx)*(Z-cz)/(vz-cz)
        Y = cy + (vy-cy)*(Z-cz)/(vz-cz)
        # Compare with current faces
        for f in self.faces:
          dx = f[0] - X
          dy = f[1] - Y
          dist = math.sqrt(dx*dx+dy*dy)
          if dist <= FACES_DIST:
            found = True
        if not found:
          print "Saved new face in", X, ",", Y
          self.faces.append([X,Y])

      # Continue moving to target
      distx = self.next[0] - self.pose.getPose3d().x;
      disty = self.next[1] - self.pose.getPose3d().y
      dist = abs(distx) + abs(disty)
      if dist > 0:
        if distx >= 0:
          velx = min(distx, distx/dist)
        else:
          velx = max(distx, distx/dist)
        if disty >=0:
          vely = min(disty, disty/dist)
        else:
          vely = max(disty, disty/dist)
        
        self.velx = velx*MAX_VEL
        self.vely = vely*MAX_VEL
      else:
        self.velx = 0.0
        self.vely = 0.0
    else:
      if not self.search_done:
        print "Go back to initial position"
      self.search_done = True

    # Go back to initial position
    if self.search_done:
      dx = self.init[0] - self.pose.getPose3d().x
      dy = self.init[1] - self.pose.getPose3d().y
      dist = math.sqrt(dx*dx+dy*dy)
      if not dist <= DIST_MARGIN:
        distx = self.init[0] - self.pose.getPose3d().x;
        disty = self.init[1] - self.pose.getPose3d().y
        dist = abs(distx) + abs(disty)
        if dist > 0:
          if distx >=0:
            velx = min(distx, distx/dist)
          else:
            velx = max(distx, distx/dist)
          if disty >=0:
            vely = min(disty, disty/dist)
          else:
            vely = max(disty, disty/dist)
          self.velx = velx*MAX_VEL
          self.vely = vely*MAX_VEL
        else:
          self.velx = 0.0
          self.vely = 0.0
      else:
        if not self.finished:
          print "Found", len(self.faces), "faces:"
          for f in self.faces:
            print "Position:", f
        self.finished = True
        self.velx = 0.0
        self.vely = 0.0

    self.cmdvel.sendCMDVel(self.velx,self.vely,0,0,0,0)

