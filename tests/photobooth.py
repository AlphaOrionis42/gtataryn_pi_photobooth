import time
import pygame
import sys
from pygame.locals import *
import RPi.GPIO as GPIO
import picamera
import config

print(config.camera_iso)

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(config.btn_led_pin, GPIO.OUT)
GPIO.setup(config.ready_led_pin, GPIO.OUT)
GPIO.setup(config.wait_led_pin, GPIO.OUT)
GPIO.setup(config.btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(config.btn_led_pin, False)
GPIO.output(config.ready_led_pin, False)
GPIO.output(config.wait_led_pin, False)

# Pygame init
pygame.init()
pygame.display.set_mode((config.slide_w, config.slide_w))
screen = pygame.display.get_surface()
pygame.mouse.set_visible(False)
#pygame.display.toggle_fullscreen()


for x in range(0,5):
    GPIO.output(config.wait_led_pin, True)
    time.sleep(0.25)
    GPIO.output(config.wait_led_pin, False)
    time.sleep(0.25)

img = pygame.image.load(config.slide_path + 'pose.png')
screen.blit(img,(0,0))
pygame.display.flip()

while True:
    time.sleep(3)
    camera = picamera.PiCamera()
    camera.iso = config.camera_iso
    camera.start_preview()
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE):
            camera.stop_preview()
            camera.close()
            GPIO.cleanup()
            pygame.quit()
            sys.exit()
