from Networking import networking, playerPayload,projectilePayload
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
        for enemy in self.mainPlayer.retrieve_enemies():
            self.entity_handler.updateOrAddEntity(enemy) 
        if remove_list:
            for i in range(0,len(remove_list)):
                remove_list[i] = projectilePayload.ProjectilePayload.from_projectile(remove_list[i])
            self.networkTool.send_remove_projectile_request(remove_list)
        locals = self.projectile_handler.get_locals()
        if locals:
            opponentProjectiles = self.networkTool.send_update_projectiles_request(locals) # -> this is if you're sending information in
            
            
            if opponentProjectiles:
                self.projectile_handler.takeOpposingProjectiles(opponentProjectiles,screen,background,self.mainPlayer)
                
        else:
            opponentProjectiles = self.networkTool.send_request_projectiles_request(self.mainPlayer.to_player_payload()) # -> this is if you're just requesting information
           
            if opponentProjectiles:
                self.projectile_handler.takeOpposingProjectiles(opponentProjectiles,screen,background,self.mainPlayer)
                
                # print(op)
            
            

    def removePlayer(self):
        self.mainPlayer.removePlayer()
        