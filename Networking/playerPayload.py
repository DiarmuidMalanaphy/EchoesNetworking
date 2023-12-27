

'''
type player struct {
	ID        uint16
	Direction uint8
	XPosition uint16
	YPosition uint16
	Health    int16
	Game      uint8
	XVelocity int16
	YVelocity int16
}
'''

class PlayerPayload:
    
    def __init__(self, ID, xPosition, yPosition, health, game, direction = 0,xVelocity = 0, yVelocity = 0):
        self.ID = ID
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.health = health
        self.game = game
        self.direction = direction 
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity

    def update(self, new_info_tuple):
        # Update the player's attributes based on the tuple
        self.ID, self.direction, self.xPosition, self.yPosition, self.health, self.game, self.xVelocity, self.yVelocity = new_info_tuple


    def to_tuple(self):
        return (self.ID,self.direction,self.xPosition,self.yPosition,self.health,self.game,self.xVelocity,self.yVelocity)
    
