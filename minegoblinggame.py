import sys
import pygame

from Handlers import  mouseHandler, entityHandler,projectileHandler,keyHandler,networkHandler
from Background import Background
from Entities import *

import os

class main:
    
    def __init__(self,serverIP):


        pygame.init()
        SCREEN_WIDTH = 768
        SCREEN_HEIGHT = 768
        
        self.screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])
        
        pygame.display.set_caption("Mine Goblin")
        icon_image = pygame.image.load("images/jumboBroadclothIcon.png")
        pygame.display.set_icon(icon_image)
        
        
        self.story(pygame.time.Clock(),story=False)
        clock = pygame.time.Clock()
        background = Background(self.screen,SCREEN_WIDTH,SCREEN_HEIGHT)
 
            
        
        
        entity_handler = entityHandler.EntityHandler(background.entityCount,entityMap=background.entityMap,background=background)
        key_handler = keyHandler.KeyHandler(background.player,background)
        projectile_handler = projectileHandler.ProjectileHandler()
        mouse_handler = mouseHandler.MouseHandler()
        network_Handler = networkHandler.NetworkHandler(background.player,entity_handler,projectile_handler,serverIP)


        
        
        running = True
        while running:
            # MAIN GAME LOOP
            dt = clock.tick(60)
            dt = dt/40
            for event in pygame.event.get():
                mouse_handler.handleClicks(event,background.player)
                if event.type == pygame.QUIT:
                    running = False
                    
                
                    
                                  
                      
            # Get state of all keys
            keys = pygame.key.get_pressed()
            key_handler.handleKeys(keys,dt)
            self.screen.fill((0, 0, 0))
            enemies = entity_handler.updateEntities(dt) # DRAW ALL HITBOXES
            remove_list = projectile_handler.update(enemies,background.player)
            network_Handler.update(remove_list,self.screen,background)
            
            
            background.updateMap() # Update light

            if background.player.dead:
                entity_handler.resetEntities(dt)

            pygame.display.flip()
            


        # Done! Time to quit.
        network_Handler.removePlayer()
        pygame.quit()

    def story(self,clock,story = False):
        SONG_END = pygame.USEREVENT+1


        def playMusic(songName):
            pygame.mixer.init()
            song = os.path.join(songName)
            pygame.mixer.music.load(song)
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
            pygame.mixer.music.play()

        #story = False # SET TO FALSE FOR NO STORY
        # playMusic("audio/IntroSong.mp3")
        # pygame.mixer.Sound("audio/munch.mp3").play()
        storyImage = pygame.image.load(os.path.join("images/story0.png"))
        pressCount = 0
        TOTAL_STORY_FRAMES = 3
        while story:
            dt = clock.tick(60)
            dt = dt/40
            # STORYBOARD LOOP
            for event in pygame.event.get():
                if event.type == SONG_END:
                    print("song over")
                    pygame.mixer.music.unload()
                    playMusic("audio/IntroSong.mp3")     
                if event.type == pygame.QUIT:
                    story=False
                    running = False
                    continue
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.Surface.convert_alpha(storyImage)
                    end = 255
                    while end > 0:
                        pygame.Surface.fill(self.screen,(0,0,0))
                        self.screen.blit(storyImage,(0,0))
                        storyImage.set_alpha(end)
                        pygame.display.flip()
                        end-=3
                        if end<0:
                            end=0               
                    if pressCount >=TOTAL_STORY_FRAMES-1:
                        story = False
                        pygame.mixer.Sound("audio/im_coming_to_get_you.mp3").play()
                    else:
                        pressCount+=1
                        storyImage = pygame.image.load(os.path.join("story" + str(pressCount) + ".png"))
                        storyImage.set_alpha(255)
                    pass
            self.screen.blit(storyImage,(0,0))
            pygame.display.flip()
    
if __name__ == "__main__":

    if len(sys.argv) > 1:
        IP = sys.argv[1]  # Set the global IP variable
    else:
        print("No IP argument provided. Exiting.")
        # sys.exit(1)
        IP = "82.6.12.81"
        # IP = '127.0.0.1'
    main(IP)