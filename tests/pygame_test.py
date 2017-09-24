import time
import pygame
import sys
from pygame.locals import *

# Init variables
#img = pygame.image.load('/home/pi/gtataryn_pi_photobooth/slides/intro.png')
running = True

# Init pygame
pygame.init()
pygame.display.set_mode((800,480))
screen = pygame.display.get_surface()
pygame.mouse.set_visible(False)
#pygame.display.toggle_fullscreen()

def show_img(img_path):
    screen.fill( (0,0,0) )

    img = pygame.image.load(img_path)
    img = img.convert()

    screen.blit(img, (0,0))
    pygame.display.flip()

def chk_input(events):
    for event in events:
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

show_img('/home/pi/gtataryn_pi_photobooth/slides/intro.png')

while running:
    print("Running? " + str(running))
    chk_input(pygame.event.get())
    #for event in pygame.event.get():
    #    if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
    #        pygame.quit()
    #        sys.exit()
