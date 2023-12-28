from .bot import Bot
from .gun import Gun
import random
from Vector import Vector
from .node import Node
import numpy as np
import math
import threading
import time
class Goblin(Bot):
    def __init__(self,screen,background,rendered = False):
        super().__init__(screen,background)
        gobbo = threading.Thread(target=self.run, args=())
        self.brain = Pathing(background.map)
        self.path = ()
        
        gobbo.start()

    def run(self):
        while self.health>0:
           
            self.path = self.brain.calculatePath(self.coordinates)
            if self.path != [] and self.path != None:
                if (self.path[0].count<10):
                    
                    vel = self.brain.stepNeeded(self.coordinates, self.path.pop().coordinates)
                    self.move(vel.x,vel.y)
            

            time.sleep(1)
    def move(self,x,y):
        self.changeXVelocity(x*10)
        self.changeYVelocity(y*10)
        


class Pathing:
    def __init__(self,grid,rateOfThinking = 0):
        self.MAX = len(grid)**2
        self.grid = grid
        self.thinkingBase = rateOfThinking
        self.thinkingCount = 0

    def recalculationRequired(self):
        if self.thinkingCount == 0:
            self.thinkingCount = self.thinkingBase
            return(True)
        else:
            self.thinkingCount=-0
            return(False)


    def calculatePath(self,startingPosition):
        grid = np.copy(self.grid)
        openSet,endPosition = self.getEndPosition(startingPosition,grid)
        count = 0
        closedSet = {}

        ###########################MASSIVE OPTIMISATIONS CAN BE MADE BY CONVERTING OPENSET TO DICTIONARY
        while openSet: 
            
            for node in openSet:
                currentNode = min(openSet, key=lambda node: node.heuristic)
                


                if currentNode.key == self.calculateKey(endPosition.x,endPosition.y):
                    path = self.getPath(currentNode)
                    return (path)
                    #path = self.getPath()
                else:
                    
                    openSet.remove(currentNode)
                    closedSet[currentNode.key] = currentNode
                    neighbours = self.generateNeighbours(currentNode.coordinates)
                    for neighbour in neighbours:
                        key = self.calculateKey(neighbour.x, neighbour.y)
                        if key in closedSet:
                            pass
                        exists,position = self.isKeyinOpenSet(openSet, key)##NON ISSUE IF DICTIONARY
                        if exists:
                            if currentNode.count < openSet[position].count:
                                openSet[position].parentNode = currentNode
                        else:

                            neighbour = Node(neighbour,self.calculateKey(neighbour.x, neighbour.y),endPosition,parentNode= currentNode)
                            openSet.append(neighbour)
                            #closedSet[]

    def isKeyinOpenSet(self,openSet,key):
        count = 0
        for node in openSet:
            if node.key == key:
                return(True,count)
            count += 1
            
        return(False,0)

    def getPath(self,targetNode):
        path = []
        for x in range(0,targetNode.count-1):
            targetNode = targetNode.parentNode
            path.append(targetNode)
            
        return(path)
            


    def getEndPosition(self,startingPosition,grid):
        for x in range(0,len(self.grid)):
            for y in range(0,len(self.grid)):
                    if grid[x][y] == 2:
                        endingPosition = Vector(x,y)
                        openSet = [Node(startingPosition,self.calculateKey(startingPosition.x, startingPosition.y),endingPosition)]
                        return(openSet,endingPosition)
        return([],())

    def calculateKey(self,x,y):
        return(x*self.MAX+y)

        


    def generateNeighbours(self,coordinates):
        neighbours = []
        count = 1
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                
                if -1<x+coordinates.x<32 and  -1<y+coordinates.y<32:
                    if self.grid[x+coordinates.x][y+coordinates.y] != 0 and count % 2 == 0:
                        neighbours.append(Vector(x+coordinates.x,y+coordinates.y))
                count +=1
        return neighbours

    def stepNeeded(self,startCoordinate,endCoordinate): ##RIGHT IS 1, LEFT IS -1 # UP IS 1
        #I'm fairly sure it's treating x as y



        xDirection = 0
        if startCoordinate.y- endCoordinate.y>0:
            print("down")
            yDirection = -1
        elif startCoordinate.y- endCoordinate.y<0:
            print("up")
            yDirection = 1
        yDirection = 0
        if startCoordinate.x - endCoordinate.x>0:
            print("left")
            xDirection = -1
        elif startCoordinate.x- endCoordinate.x<0:
            print("right")
            xDirection = 1

        
        return(Vector(xDirection,yDirection))
            

    
        
    #neighbors = generate_neighbors(current_node, grid)