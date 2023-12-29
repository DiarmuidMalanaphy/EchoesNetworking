from Networking import playerPayload
from Entities import player

class EntityHandler:
    
    def __init__(self,entityCount ,entityMap = {},background = None):

        self.entityMap = entityMap
        self.entityCount = entityCount
        self.background = background

    def addEntity(self,entity,entityID = None):
        if entityID is None:

            self.entityMap[self.entityCount] = entity
            self.entityCount += self.entityCount 
        else:
            self.entityMap[entityID] = entity
        
    def removeEntity(self,entityID):
        del self.entityMap[entityID]

    def updateEntities(self,dt):
        delList = []
        enemyList = []
        for key,entity in self.entityMap.items():
            if entity.isConnected():
                if key<1000 and entity.local:
                    enemyList.append(entity)
                entity.update(dt)
                entity.updateSprite()
            else:
                delList.append(key)
        for key in delList:
            del self.entityMap[key]
        return(enemyList)

    def updateOrAddEntity(self,entity):
        if entity[0] in self.entityMap and not self.entityMap[entity[0]].local:
            self.entityMap[entity[0]].incrementAliveCount()
            self.entityMap[entity[0]].update_from_network(playerPayload.PlayerPayload.from_tuple(entity))
            
        else:
            self.entityMap[entity[0]] = player.Player.from_payload(screen= self.background.screen,background=self.background,player_payload=entity)




    

    def resetEntities(self,dt):
        for key,entity in self.entityMap.items():
            entity.resetEntity(dt)
        
            