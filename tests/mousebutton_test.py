import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import time
from time import sleep
from PIL import Image
import sys

pygame.init()
pygame.display.set_mode((800,480))
screen = pygame.display.get_surface()
pygame.mouse.set_visible(False)
#pygame.display.toggle_fullscreen()

def clear_screen():
    screen.fill( (0,0,0) )
    pygame.display.flip()

def chk_input(events):
    for event in events:
        if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            print("Mouse button down")

def show_slide(img_path, offset_x, offset_y):
    screen.fill( (0,0,0) )

    img = pygame.image.load(img_path)
    img = img.convert()


    screen.blit(img, (offset_x, offset_y))
    pygame.display.flip()

while True:
    show_slide('/home/pi/gtataryn_pi_photobooth/slides/intro.png', 0, 0)
    sleep(1)
    chk_input(pygame.event.get())
    clear_screen()
    sleep(2)
