import picamera
import time
from PIL import Image
import pygame
import sys
from pygame.locals import *

width = 1824
height = 984

#Pygame init
pygame.init()
screen = pygame.display.set_mode((width, height), FULLSCREEN)
pygame.display.set_caption('Photo booth')
pygame.mouse.set_visible(False)
#pygame.display.toggle_fullscreen()


with picamera.PiCamera() as camera:
    while True:
        try:
            #show_img('app_images/pose.png')
            pose = pygame.image.load('app_images/pose.png')
            screen.blit(pose,(0,0))
            pygame.display.flip()
            time.sleep(3)
            camera.start_preview()
            pygame.quit()
            time.sleep(3)
            img = Image.open('app_images/countdown3.png')
            pad = Image.new('RGB', (((img.size[0] + 31) //32) *32, ((img.size[1] + 15) // 16) * 16,))
            pad.paste(img, (0,0), img)
            o = camera.add_overlay(img.tobytes(), size=img.size)
            o.alpha = 100
            o.layer = 3
            time.sleep(.5)
            camera.remove_overlay(o)
            time.sleep(.5)
            img = Image.open('app_images/countdown2.png')
            pad = Image.new('RGB', (((img.size[0] + 31) //32) *32, ((img.size[1] + 15) // 16) * 16,))
            pad.paste(img, (0,0), img)
            o = camera.add_overlay(img.tobytes(), size=img.size)
            o.alpha = 100
            o.layer = 3
            time.sleep(.5)
            camera.remove_overlay(o)
            time.sleep(.5)
            img = Image.open('app_images/countdown1.png')
            pad = Image.new('RGB', (((img.size[0] + 31) //32) *32, ((img.size[1] + 15) // 16) * 16,))
            pad.paste(img, (0,0), img)
            o = camera.add_overlay(img.tobytes(), size=img.size)
            o.alpha = 100
            o.layer = 3
            time.sleep(.5)
            camera.remove_overlay(o)
            time.sleep(.5)
            #screen.fill( (0,0,0) )
            #pygame.display.flip()
            

        finally:
            
            camera.close()
            pygame.quit()
            #sys.exit()
    
