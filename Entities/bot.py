from .sprite import Sprite
import threading
class Bot(Sprite):
    
    def __init__(self,screen,background,rendered = False):
        super().__init__(screen,background,size = 24)
    
    def update(self,dt):
        self.changeYVelocity(self.gravity*dt)
        self.background.modifyCoordinateMap(self.coordinates,self.calculateCoordinates(self.coordinates.x, self.coordinates.y),3)
        # self.updatePosition()
        self.coordinates = self.calculateCoordinates(self.position.x, self.position.y)
        super().update(dt)

        
    