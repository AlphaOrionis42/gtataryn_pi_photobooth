import time
import pygame
import sys
from pygame.locals import *
img = pygame.image.load('/home/pi/gregtataryn_photobooth/app_images/pose.png')

pygame.init()
pygame.display.init()
w = 800
h = 480
screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
#pygame.display.toggle_fullscreen()
#white = (255, 64, 64)

#screen.fill((white))
running = 1
loop = 1

while running:
    print(loop)
    loop = loop + 1
    for event in pygame.event.get():
        if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()
            sys.exit()
        
    #screen.fill((white))
    screen.blit(img,(0,0))
    pygame.display.flip()
