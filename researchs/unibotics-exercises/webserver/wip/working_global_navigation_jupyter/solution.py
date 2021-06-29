''' ///////////////////////////////////////////////////////////////////////'''
                        ''' execute method'''
''' ///////////////////////////////////////////////////////////////////////'''
    def execute(self):
        print("GOING TO DESTINATION")

        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        #self.vel.setV(10)
        #self.vel.setW(5)
        #self.vel.sendVelocities()

        # Position of the robot
        posRobotX = self.sensor.getRobotX()
        posRobotY = self.sensor.getRobotY()
        orientationRobot = self.sensor.getRobotTheta()

        # Destination
        dest = self.grid.getDestiny()
        destWorld = self.grid.gridToWorld(dest[0], dest[1])

        posRobotImage = self.grid.worldToGrid(posRobotX, posRobotY)

        if (abs(posRobotX)<(abs(destWorld[0])+2) and abs(posRobotX)>(abs(destWorld[0])-2)) and (abs(posRobotY)<(abs(destWorld[1])+2) and abs(posRobotY)>(abs(destWorld[1])-2)):
            # We have arrived at the destination
            self.vel.setV(0)
            self.vel.setW(0)
            print("DESTINATION")
        else:
            # We haven't arrived at the destination
            print(" NOT ARRIVED AT DESTINATION")
            
            # We calculate the next objective and the next one to do an interpolation
            found = False
            mapIm = self.grid.getMap()
            valMin = 2000000000000
            r = 5
            for i in range(posRobotImage[0]-r, posRobotImage[0]+r+1):
                for j in range(posRobotImage[1]-r, posRobotImage[1]+r+1):
                    if ((((i==(posRobotImage[0]-r)) or(i==(posRobotImage[0]+r)) and (posRobotImage[1]-r<=j<=posRobotImage[1]+r)) or (((j==(posRobotImage[1]-r)) or (j==(posRobotImage[1]+r))) and (posRobotImage[0]-r-1<=i<=posRobotImage[0]+r-1)))):
                        val = self.grid.getVal(i, j)
                        if (found == False and mapIm[j, i] == 255):
                            found = True
                            valMin = val
                            tar = [i, j]
                        else:
                            if(val < valMin and mapIm[j, i] == 255):
                                tar = [i, j]
                                valMin = val
            targetImage = tar
            target = self.grid.gridToWorld(targetImage[0], targetImage[1])
            
            found = False
            mapIm = self.grid.getMap()
            valMin = 2000000000000
            # Radio
            r = 5
            for i in range(targetImage[0]-r, targetImage[0]+r+1):
                for j in range(targetImage[1]-r, targetImage[1]+r+1):
                    if ((((i==(targetImage[0]-r)) or(i==(targetImage[0]+r)) and (targetImage[1]-r<=j<=targetImage[1]+r)) or (((j==(targetImage[1]-r)) or (j==(targetImage[1]+r))) and (targetImage[0]-r-1<=i<=targetImage[0]+r-1)))):
                        val = self.grid.getVal(i, j)
                        if (found == False and mapIm[j, i] == 255):
                            found = True
                            valMin = val
                            tar = [i, j]
                        else:
                            if(val < valMin and mapIm[j, i] == 255):
                                tar = [i, j]
                                valMin = val
            targetNextImage = tar
            targetNext = self.grid.gridToWorld(targetNextImage[0], targetNextImage[1])
            
            # Interpolation
            targetInterpolationx = (target[0] + targetNext[0]) / 2
            targetInterpolationy = (target[1] + targetNext[1]) / 2            
            
            # Convert targetInterpolationx y targetInterpolationy to relative coordinates
            directionx,directiony = self.absolutas2relativas(targetInterpolationx,targetInterpolationy,posRobotX,posRobotY,orientationRobot)

            if directionx == 0:
                # If directionx is 0 we change it by 0.01
                directionx = 0.01
            # We calculate the angle between our position and the goal
            angle = math.atan((directiony/directionx))

            # Correct position    
            if directionx < 0 and directiony > 0:
                # If the target is behind
                angle = -angle
                
            # Angle of turn
            if abs(angle) < 0.05:
                angleTurn = 0.3
            elif abs(angle) > 0.8:
                angleTurn = 1.2
            else:
                angleTurn = 0.5
            
            # Angular speed
            if angle < 0:
                self.vel.setW(-angleTurn)
            else:
                self.vel.setW(angleTurn)

            # Linear speed
            if abs(angle) < 0.1:
                speed = 10
            else:
                speed = 3

            if directionx < 0 and directiony > 0:
                speed = 3
                
            self.vel.setV(speed)

''' ///////////////////////////////////////////////////////////////////////'''
                        ''' generatePath function'''
''' ///////////////////////////////////////////////////////////////////////'''
def generatePath(self):
    if not self.initiallized:
        self.posObstaclesBorder = []
        self.targets = []
        self.rejilla = np.zeros((400, 400),np.uint8)
        self.initiallized = True

    # mapIm is the image of the map
    mapIm = self.grid.getMap()
    # dest is the selected destination, and is a tuple (x, y)  
    dest = self.grid.getDestiny()
    if not dest:
        print("Destiny not yet selected!")
        return None
    # gridPos is the position on the map, (x, y)
    gridPos = self.grid.getPose()

    # Position of the robot
    world_robotX = self.sensor.getRobotX()
    world_robotY = self.sensor.getRobotY()
    posRobot = self.grid.worldToGrid(world_robotX, world_robotY)

    # We need some variables in the loop while
    fin = "false"
    margin = 20

    # Evaluating the value of the field on position (dest[0], dest[1])
    if (mapIm[dest[1]][dest[0]] == 255):
        self.grid.setVal(dest[0], dest[1], 0.0)
        nodo = [[dest[0], dest[1]]]
        print("LOOKING FOR SHORTEST PATH")
    else:
        print("Please, select a valid destination")
        return None

    # New nodes
    nodos = []

    # Expansion of the field
    while (fin == "false"):
        for i in range(0, len(nodo)):
            if ((mapIm[nodo[i][1], nodo[i][0]] == 255) and nodo[i][0] >= 0 and nodo[i][0] < mapIm.shape[0] and nodo[i][1] >= 0 and nodo[i][1] < mapIm.shape[1]):
                # Wave fronts of each node
                # frente1 are the pixels to which 1 is added
                frente1 = [[nodo[i][0]-1, nodo[i][1]], [nodo[i][0], nodo[i][1]-1], [nodo[i][0]+1, nodo[i][1]], [nodo[i][0], nodo[i][1]+1]]
                # frente2 are the pixels to which sqrt(2) is added
                frente2 = [[nodo[i][0]-1, nodo[i][1]-1], [nodo[i][0]+1, nodo[i][1]-1], [nodo[i][0]+1, nodo[i][1]+1], [nodo[i][0]-1, nodo[i][1]+1]]
                # val_init is the value of the central pixel of the expansion
                val_init = self.grid.getVal(nodo[i][0], nodo[i][1])
                # Expansion of the nodes
                valAdd = 1
                frente = frente1
                for a in range(0, len(frente)):
                    if (frente[a][1] >= 0) and (frente[a][1] < mapIm.shape[1]) and (frente[a][0] >= 0) and (frente[a][0] < mapIm.shape[0]):
                        if mapIm[frente[a][1], frente[a][0]] == 255:
                            val = self.grid.getVal(frente[a][0], frente[a][1])
                            if ((math.isnan(val)) or ((val_init + valAdd) < val) or (val <= 0)):
                                
                                if frente[a][0] != dest[0] or frente[a][1] != dest[1]:
                                    self.grid.setVal(frente[a][0], frente[a][1], val_init+valAdd)
                                    pos0 = frente[a][0]
                                    pos1 = frente[a][1]
                                    found = False
                                    for z in range(0, len(nodos)):
                                        if self.grid.getVal(pos0, pos1) == self.grid.getVal(nodos[z][0][0], nodos[z][0][1]):
                                            nodos[z].append([pos0, pos1])
                                            found = True
                                    if found == False:
                                        nodos.append([[pos0, pos1]])
                        else:
                            if valAdd == 1:
                                p0 = frente[a][0]
                                p1 = frente[a][1]
                                found = False
                                for y in range(0, len(self.posObstaclesBorder)):
                                    if (self.posObstaclesBorder[y][0] == p0) and (self.posObstaclesBorder[y][1]) == p1:
                                        found = True
                                if (found == False):
                                    self.posObstaclesBorder.append([p0, p1])

                #nodos = self.expansionNode(frente2, math.sqrt(2.0), mapIm, val_init, dest, nodos) 
                # Expansion of the nodes
                valAdd = math.sqrt(2.0)
                frente = frente2
                for b in range(0, len(frente)):
                    if (frente[b][1] >= 0) and (frente[b][1] < mapIm.shape[1]) and (frente[b][0] >= 0) and (frente[b][0] < mapIm.shape[0]):
                        if mapIm[frente[b][1], frente[b][0]] == 255:
                            val = self.grid.getVal(frente[b][0], frente[b][1])
                            if ((math.isnan(val)) or ((val_init + valAdd) < val) or (val <= 0)):
                                
                                if frente[b][0] != dest[0] or frente[b][1] != dest[1]:
                                    self.grid.setVal(frente[b][0], frente[b][1], val_init+valAdd)
                                    pos0 = frente[b][0]
                                    pos1 = frente[b][1]
                                    found = False
                                    for u in range(0, len(nodos)):
                                        if self.grid.getVal(pos0, pos1) == self.grid.getVal(nodos[u][0][0], nodos[u][0][1]):
                                            nodos[u].append([pos0, pos1])
                                            found = True
                                    if found == False:
                                        nodos.append([[pos0, pos1]])
                        else:
                            if valAdd == 1:
                                p0 = frente[b][0]
                                p1 = frente[b][1]
                                found = False
                                for v in range(0, len(self.posObstaclesBorder)):
                                    if (self.posObstaclesBorder[v][0] == p0) and (self.posObstaclesBorder[v][1]) == p1:
                                        found = True
                                if (found == False):
                                    self.posObstaclesBorder.append([p0, p1])    
                           
            # Cases of the margins, we check if we finish the expansion
            if ((dest[0] <= posRobot[0]) and (dest[1] <= posRobot[1])):
                if((nodo[i][0] > (posRobot[0] + margin)) and (nodo[i][1] > (posRobot[1] + margin))):
                    fin = "true"
            elif ((dest[0] >= posRobot[0]) and (dest[1] <= posRobot[1])):
                if((nodo[i][0] < (posRobot[0] - margin)) and (nodo[i][1] > (posRobot[1] + margin))):
                    fin = "true"
            elif ((dest[0] >= posRobot[0]) and (dest[1] >= posRobot[1])):
                if((nodo[i][0] < (posRobot[0] - margin)) and (nodo[i][1] < (posRobot[1] - margin))):
                    fin = "true"
            elif ((dest[0] <= posRobot[0]) and (dest[1] >= posRobot[1])):
                if((nodo[i][0] > (posRobot[0] + margin)) and (nodo[i][1] < (posRobot[1] - margin))):
                    fin = "true"
    
        if (nodos != []):
            # We update the node that will expand values ​​and remove the previous node
            nodo = nodos[0]
            nodos.pop(0)
    for d in range(0, len(self.posObstaclesBorder)):
        for k in range(self.posObstaclesBorder[d][0]-3, self.posObstaclesBorder[d][0]+4):
            for l in range(self.posObstaclesBorder[d][1]-3, self.posObstaclesBorder[d][1]+4):
                if ((k >= 0) and (k < mapIm.shape[0]) and (l >= 0) and (l < mapIm.shape[1])):
                    if (mapIm[l][k] == 255):
                        # Penaltie's Obstacles
                        penaltie =  0
                        penaltieMax = 180
                        d0 = self.posObstaclesBorder[d][0]
                        d1 = self.posObstaclesBorder[d][1]
                        destino = dest
                        for c in range(1, 4):
                            if ((((k == (d0-c)) or (k == (d0+c)) and (d1-c <= l <= d1+c)) or (((l == (d1-c)) or (l == (d1+c))) and (d0-c-1 <= k <= d0+c-1)))):
                                penaltie = penaltieMax - c * 6
                        if (penaltie > self.rejilla[l][k] and (k != destino[0] or l != destino[1])):
                            self.rejilla[l][k] = penaltie

    # We add our grid and the penalty grid
    self.grid.grid = self.rejilla+self.grid.grid

    # Find the path
    # We need some variables in the loop while
    pixelCentral = [posRobot[0], posRobot[1]]
    valMin = self.grid.getVal(posRobot[0], posRobot[1])
    posMin = pixelCentral
    self.grid.setPathVal(posRobot[0], posRobot[1], valMin)
    found = "false"
    posPath= []

    while (found == "false"):
        foundNeighbour = "false"
        for m in range(pixelCentral[0]-1, pixelCentral[0]+2):
            for n in range(pixelCentral[1]-1, pixelCentral[1]+2):
                if ((m >= 0) and (m < mapIm.shape[0]) and (n >= 0) and (n < mapIm.shape[1]) and (mapIm[n][m] !=0)):
                    val = self.grid.getVal(m, n)
                    arrayPath = posPath
                    f = "false"
                    for x in range(0, len(arrayPath)):
                        if (arrayPath[x][0] == m) and (arrayPath[x][1] == n):
                            f = "true"
                    posFound = f

                    if (foundNeighbour == "false" and posFound == "false"):
                        foundNeighbour = "true"
                        valNeighbour = val
                    if posFound == "false":
                        if ((val < valMin) and (val >=  0.0)):
                            if (((val == 0.0) and (m == dest[0]) and (n == dest[1])) or (val > 0.0)):
                                valMin = val
                                posMin = [m, n]
                        elif val <= valNeighbour:
                            valMin = val
                            valNeighbour = val
                            posMin = [m, n]

        self.grid.setPathVal(posMin[0], posMin[1], valMin)
        pixelCentral = posMin
        posPath.append(posMin)
        if ((valMin == 0.0) and (posMin[0] == dest[0]) and (posMin[1] == dest[1])):
            found = "true"
            self.grid.setPathFinded()
    print("Shortest path found!")
    return self.grid.getPath()
