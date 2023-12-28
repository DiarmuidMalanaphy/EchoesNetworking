

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
    
    def __init__(self, ID=0, direction = 0, xPosition = 10, yPosition=10, health=100, game=0,xVelocity = 0, yVelocity = 0):
        self.ID = ID
        self.direction = direction
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.health = health
        self.game = game
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity

    def update(self, new_info_tuple):
        # Update the player's attributes based on the tuple
        self.ID, self.direction, self.xPosition, self.yPosition, self.health, self.game, self.xVelocity, self.yVelocity = new_info_tuple


    def to_tuple(self):
        return (self.ID,self.direction,self.xPosition,self.yPosition,self.health,self.game,self.xVelocity,self.yVelocity)
    
    @staticmethod
    def from_tuple(data_tuple):
        """
        Create a PlayerPayload object from a tuple.

        :param data_tuple: A tuple containing player data in the order:
                           (ID, direction, xPosition, yPosition, health, game, xVelocity, yVelocity)
        :return: A PlayerPayload object initialized with the provided data.
        """
        if len(data_tuple) != 8:
            raise ValueError("Tuple must have exactly 8 elements")

        return PlayerPayload(*data_tuple)
    
