

from Entities import projectile


class ProjectileHandler():
    projectiles = {}
    

    def addProjectile(self,proj):
        #self.projectiles.append(proj)
        self.projectiles[proj.ID] = proj

    def removeProjectile(self,proj):
        del self.projectiles[proj.ID]
        

    def update(self,enemies):
        removeList = []
        for _,proj in self.projectiles.items():

            remove = proj.update()
            

            
            if remove or proj.hitPlayer(enemies):
                removeList.append(proj)
                continue
            proj.draw()
        for proj in removeList:
            self.removeProjectile(proj)
        return removeList
    
    def get_locals(self):
        locals = []
        for _,projectile in self.projectiles.items():
            if projectile.isLocal():
                locals.append(projectile)

    def takeOpposingProjectiles(self,opponentProjectiles,screen,background,player):
        for proj in opponentProjectiles:
            if proj[0] in self.projectiles:
                self.projectiles[proj[0]].update_from_network(proj)
            else:
                self.projectiles[proj[0]] = projectile.Projectile.from_payload(screen,background,proj,player)

    def __init__(self):
        pass