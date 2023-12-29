import threading
import pygame
from Networking import networking, playerPayload,projectilePayload




from .sprite import Sprite
from .gun import Gun

from Handlers.projectileHandler import ProjectileHandler
from Handlers.animationHandler import AnimationHandler
from Vector import Vector
import math

class Player(Sprite):
    moveSpeed = 1.5
    gravity = 1.5
    local = True
    dead = False

    def update(self,dt):
        self.changeYVelocity(self.gravity*dt)
        self.background.modifyCoordinateMap(self.coordinates,self.calculateCoordinates(self.position.x, self.position.y),2)
        
        self.coordinates = self.calculateCoordinates(self.position.x, self.position.y)
        if not self.local:
            self.decrementAliveCount()
        
        
        # self.updatePosition()
        super().update(dt)
        self.background.addLight((self.position.x+(self.width/2)+3),(self.position.y+(self.height/2)+3),50,10)

    def passAngleToGun(self,angle):
        self.movementFacing = angle
        self.gun.setAngle(angle)
    


    def takeDamage(self, damage):
        
        ###Play sound
        
        super().takeDamage(damage)
        pygame.mixer.Sound("Entities/audio/ow.mp3").play()
        self.health = round(self.health)
        if damage<=0:
            damage = 0
            self.dead = True

        if self.dead:
            #pygame.mixer.Sound("audio/giggle.mp3").play()
            self.rendered = False
            pass
            ##Play dead noises
        
            

    def checkDead(self):
        return self.dead
    
    def isConnected(self):
        return(self.aliveCount>=0)
    
    def decrementAliveCount(self): # -> used to check if the persons internet connection or game has crashed, (response check)
        self.aliveCount = self.aliveCount-1

    def incrementAliveCount(self):
        if self.aliveCount<100:
            self.aliveCount = 100

    def updateSprite(self):
        self.AnimationHandler.moveConductor.play()
        super().updateSprite(self.AnimationHandler.animObjs)
    
    def fire(self, angle, click_duration):
        projectile = self.gun.fire_gun(angle, click_duration, self.background, self.screen)

        
        thread = threading.Thread(target=self.handle_projectile_update, args=([projectile]))
        thread.start()



    def handle_projectile_update(self, originalProjectile):
        projectile = projectilePayload.ProjectilePayload(PlayerID= self.internetID,GameID=self.gameID,XPosition=round(originalProjectile.position.x),YPosition=round(originalProjectile.position.y),Direction=round(self.movementFacing),XVelocity=round(originalProjectile.velocity.x),YVelocity=round(originalProjectile.velocity.y))
        projectile = self.networkTool.send_initialise_projectile_request(projectile)[0]
        
        originalProjectile.ID = projectile[0]
        originalProjectile.position.x = projectile[3]
        originalProjectile.position.y = projectile[4]
        originalProjectile.velocity.x = projectile[6]
        originalProjectile.velocity.y = projectile[7]
        self.projectileHandler.addProjectile(originalProjectile)
       

        
        

    def addBoost(self, x, y, size, intensity):
        # Calculate the distance between the player's position and the boost point
        dx = x - self.position.x
        dy = y - self.position.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Check if the player is within the boost radius
        if distance <= size:
            # Calculate the direction vector away from the boost point
            direction = (dx / distance, dy / distance)
            
            # Apply the boost to the player's velocity
            self.velocity.x-=(direction[0] * intensity)
            self.velocity.y-=(direction[1] * intensity)
        return True
    
    def addGrapple(self, x, y, intensity):
        # Calculate the distance between the player's position and the boost point
        dx = x - self.position.x
        dy = y - self.position.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Check if the player is within the boost radius
        
            # Calculate the direction vector away from the boost point
        direction = (dx / distance, dy / distance)
            
            # Apply the boost to the player's velocity
        self.velocity.x-=(direction[0] * intensity)
        self.velocity.y-=(direction[1] * intensity)
        return True
    
    def to_player_payload(self, payload=None):
        if payload is None:
            # Create a PlayerPayload instance with the current state of the Player
            player_payload = playerPayload.PlayerPayload(
                ID = self.internetID,
                direction = round(self.movementFacing),
                xPosition = round(self.position.x),
                yPosition = round(self.position.y),
                health = self.health,
                game = self.gameID,
                xVelocity = round(self.velocity.x),
                yVelocity = round(self.velocity.y)
            )
        else:
            player_payload = playerPayload.PlayerPayload.from_tuple(payload)

        return player_payload
    

    def initialisePlayerOnline(self,serverIP):
        self.networkTool = networking.Networking(serverIP)
        self.movementFacing = 270
        if self.networkTool is not None:
            self.gameID = 1
            self.internetID = 0
            # print("pee2S")
            # print(self.to_player_payload().ID)
            newPlayerInformation = None
            while newPlayerInformation is None:
                newPlayerInformation = self.networkTool.send_initialise_player_request(self.to_player_payload())
            newPlayerInformation = newPlayerInformation[0]
            
            self.update_from_network(self.to_player_payload(payload = newPlayerInformation))

            # print(self.to_player_payload().ID)
        return(self.gameID)


    def update_from_network(self, player_data_payload):
        # Update the Player's attributes based on the received payload
        self.internetID = player_data_payload.ID
        self.movementFacing = player_data_payload.direction
        self.position.x = player_data_payload.xPosition
        self.position.y = player_data_payload.yPosition
        self.health = player_data_payload.health
        self.gameID = player_data_payload.game
        self.velocity.x = player_data_payload.xVelocity
        self.velocity.y = player_data_payload.yVelocity

    
    def retrieve_enemies(self):
        player_data_payload = self.to_player_payload()#
        # print("personal location", player_data_payload.xPosition)
        if player_data_payload:
            # print(player_data_payload)
            enemies = self.networkTool.send_update_player_request(player_data_payload)
            if enemies is not None:

                return(enemies)
            return([])
        
    def removePlayer(self):
        player_data_payload = self.to_player_payload()
        if player_data_payload:
            
            return(self.networkTool.send_remove_player_request(player_data_payload))
        

    @staticmethod
    def from_payload(screen, background, player_payload, networkTool=None,local = False):
        """
        Create a Player object from a player payload.

        :param screen: The screen where the player will be rendered.
        :param background: The background context of the player.
        :param player_payload: An instance of PlayerPayload or a tuple containing player data.
        :param networkTool: Optional, a network tool instance for the player.
        :return: A Player object initialized with the provided data.
        """
        # Extract data from player_payload
        
        
        # Unpack the payload data
        ID, direction, xPosition, yPosition, health, game, xVelocity, yVelocity = player_payload

        # Create a new Player instance
        player = Player(
            screen=screen, 
            background=background, 
            moveSpeed=1.5,  # moveSpeed needs to be set
            x=xPosition, 
            y=yPosition, 
            rendered=True,  # Assuming rendered is always True
            
            networkTool=networkTool
        )
        player.local = local  # If it's being created like this i'm going to assume it's not the local client.

        # Set additional attributes from payload
        player.internetID = ID
        player.movementFacing = direction
        player.health = health
        player.gameID = game
        player.velocity.x = xVelocity
        player.velocity.y = yVelocity


        return player
    
    
    

    def __init__(self,screen,background,moveSpeed,x = 400,y = 400,rendered = True,networkTool = None,aliveCount = 250):
        super().__init__(screen,background,Vector(x,y),rendered=rendered)
        
        self.aliveCount = aliveCount
        self.moveSpeed = moveSpeed
        self.networkTool = networkTool
        self.gun = Gun(self,screen)
        self.projectileHandler = ProjectileHandler()
        self.AnimationHandler = AnimationHandler("Entities/images/Oldman.png", 2, 4, ['idle_right', 'walk_right'])
        
        