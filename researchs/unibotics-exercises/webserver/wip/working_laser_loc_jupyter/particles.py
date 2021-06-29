class Particle:
    def __init__(self, x, y, yaw, prob, mapAngle):
        self.x = x
        self.y=y
        self.yaw=mapAngle+yaw
        self.prob=prob 
    
