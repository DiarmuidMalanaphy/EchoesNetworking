from Networking import networking, playerPayload,projectilePayload

import threading

class NetworkHandler:
    def __init__(self,mainPlayer,entity_handler,projectile_handler,serverIP):  
        self.serverIP = serverIP 
        self.mainPlayer = mainPlayer
        self.entity_handler = entity_handler
        self.projectile_handler = projectile_handler
        self.initialisePlayer()
        entity_handler.removeEntity(0)
        entity_handler.addEntity(mainPlayer,entityID=mainPlayer.internetID)
        self.networkTool = networking.Networking(serverIP)

    def initialisePlayer(self):

        self.mainPlayer.initialisePlayerOnline(self.serverIP)

    def update(self,remove_list,screen,background):

        enemy_thread = threading.Thread(target=self.threadToRetrieveEnemies, args=(self.mainPlayer, self.entity_handler))
        enemy_thread.start()
        projectile_thread = threading.Thread(target=self.projectileHandlingThread, args=(self.networkTool, remove_list,self.projectile_handler, self.mainPlayer, screen, background))
        projectile_thread.start()
        
            
    def threadToRetrieveEnemies(self,mainPlayer, entity_handler):

        enemies = mainPlayer.retrieve_enemies()  # Retrieve enemies
        for enemy in enemies:
            entity_handler.updateOrAddEntity(enemy)

    def projectileHandlingThread(self,networkTool,remove_list, projectile_handler, mainPlayer, screen, background):
    
        

        if remove_list:
            remove_payload_list = [projectilePayload.ProjectilePayload.from_projectile(proj) for proj in remove_list]
            networkTool.send_remove_projectile_request(remove_payload_list)

        locals = projectile_handler.get_locals()
        if locals:
            opponentProjectiles = networkTool.send_update_projectiles_request(locals)
            if opponentProjectiles:
                projectile_handler.takeOpposingProjectiles(opponentProjectiles, screen, background, mainPlayer)
        else:
            opponentProjectiles = networkTool.send_request_projectiles_request(mainPlayer.to_player_payload())
            if opponentProjectiles:
                projectile_handler.takeOpposingProjectiles(opponentProjectiles, screen, background, mainPlayer)

    


    def removePlayer(self):
        self.mainPlayer.removePlayer()
        