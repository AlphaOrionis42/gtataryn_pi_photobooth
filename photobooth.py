#!/usr/bin/env python
# Author: Greg Tataryn

import os
import config
import RPi.GPIO as GPIO
import picamera
import sys
import pygame
from pygame.locals import *
import time
from time import sleep
from PIL import Image

# Debug variable used in testing. Set to false for production
debug = True

# Run variable for main program
run = True

###################
# Other Variables #
###################
transform_x = config.monitor_w
transform_y = config.monitor_h
offset_x = 0
offset_y = 0

##############
# GPIO Setup #
##############
GPIO.setmode(GPIO.BOARD)
GPIO.setup(config.btnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(config.greenLed, GPIO.OUT)
GPIO.setup(config.redLed, GPIO.OUT)
GPIO.output(config.greenLed, False)
GPIO.output(config.redLed, False)

################
# Pygame Setup #
################
pygame.init()
pygame.display.set_mode((config.monitor_w, config.monitor_h))
screen = pygame.display.get_surface()
pygame.mouse.set_visible(False)
pygame.display.toggle_fullscreen()

def clear_screen():
    screen.fill( (0,0,0) )
    pygame.display.flip()
    
def chk_input(events):
    for event in events:
        if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
            run = False
            pygame.quit()
            sys.exit()

def overlay_img(imgPath, cam):
    img = Image.open(imgPath)
    oLay = cam.add_overlay(img.tobytes(), size=img.size)
    oLay.alpha = 100
    oLay.layer = 3
    return oLay

def set_img_dimension(img_w, img_h):
    global transform_y, transformx, offset_y, offset_x

    ratio_h = (config.monitor_w * img_h) / img_w

    if (ratio_h < config.monitor_h):
        transform_y = ratio_h
        transform_x = config.monitor_w
        offset_y = (config.monitor_h - ratio_h) / 2
        offset_x = 0
    elif (ratio_h > config.monitor_h):
        transform_x = (config.monitor_h * img_w) / img_h
        transform_y = config.monitor_h
        offset_x = (config.monitor_w - transform_x) / 2
        offset_y = 0
    else:
        transform_x = config.monitor_w
        transform_y = config.monitor_h
        offset_y = offset_x = 0

def show_slide(img_path, offset_x, offset_y):
    screen.fill( (0,0,0) )

    img = pygame.image.load(img_path)
    img = img.convert()

    #set_img_dimension(int(img.get_width()), int(img.get_height()))

    #img = pygame.transform.scale(img, (transform_x, transform_y))

    screen.blit(img, (offset_x, offset_y))
    pygame.display.flip()

def make_gif(jpg_group, ts):
    if debug:
        print('Making animated gif')
    for x in range(1, config.num_shots+1):
        graphicsmagick = "gm convert -size 800x480 " + jpg_group + "_" + str(x) + ".jpg -thumbnail 800x480 " + jpg_group + "_" + str(x) + "_sm.jpg"
        os.system(graphicsmagick)
    
    graphicsmagick = "gm convert -delay " + str(config.gif_delay) + " " + jpg_group + "*.jpg" + " " + config.gif_path + "photobooth_" + ts + ".gif"
    #print(graphicsmagick)
    os.system(graphicsmagick)

def display_imgs(jpg_group):
    for i in range(0, config.replay_count):
        for j in range(1,config.num_shots+1):
            print("Loop: " + str(i) + " Photo: " + str(j))
            show_slide(jpg_group + "_" + str(j) + "_sm.jpg", 80, 0)
            sleep(config.replay_wait)

def run_booth():
    if debug:
        print("Running photobooth")
    GPIO.output(config.greenLed, False)
    now = time.strftime("%Y%m%d%H%M%S")
    if debug:
        print(now)
    # Try to run the preview and take a series of photots
    try:
        #camera = picamera.PiCamera(sensor_mode=4, resolution='1640x1232')
        camera = picamera.PiCamera()
        camera.iso = config.camera_iso
        
        #camera.preview_fullscreen = True
        clear_screen()
        for i in range(1,config.num_shots+1):
            GPIO.output(config.redLed, False)
            camera.hflip = True
            #camera.sensor_mode = 4
            camera.resolution = (800, 480)
            camera.start_preview()
            filename = config.save_path + 'photobooth_' + now + '_' + str(i) + '.jpg'
            sleep(.5)
            o = overlay_img(config.slide_path + 'pose.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(2)
            camera.remove_overlay(o)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            o = overlay_img(config.slide_path + 'countdown3.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(o)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            o = overlay_img(config.slide_path + 'countdown2.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(o)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            o = overlay_img(config.slide_path + 'countdown1.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(o)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            camera.hflip = False
            camera.stop_preview()
            camera.resolution = (1640, 1232)
            GPIO.output(config.redLed, True)
            camera.capture(filename)
            if debug:
                print(filename)
            time.sleep(1)
    except Exception as err:
        print("Error in function run_booth")
        print(type(err))
        print(err.args)
        print(err)
        camera.stop_preview()
        camera.close()
    finally:
        camera.stop_preview()
        camera.close()

    show_slide(config.slide_path + "wait.png", 0, 0)
    make_gif(config.save_path + "photobooth_" + now, now)
    clear_screen()
    display_imgs(config.save_path + "photobooth_" + now)

    
    show_slide(config.slide_path + 'intro.png', 0, 0)

# Function that runs on startup to blink the LED.
def Startup():
    for x in range(1,5):
        GPIO.output(config.greenLed, True)
        time.sleep(0.25)
        GPIO.output(config.greenLed, False)
        time.sleep(0.25)
    GPIO.output(config.redLed, True)

################
# Main Program #
################
try:
    # Run startup to blink the green light.
    Startup()
    time.sleep(.25)
    show_slide(config.slide_path + 'intro.png', 0, 0)
    while run:
        GPIO.output(config.redLed, False)
        GPIO.output(config.greenLed, True)
        chk_input(pygame.event.get())
        #print("Green LED on")
        if GPIO.input(config.btnPin):
            time.sleep(config.debounce)
            if debug:
                print("Button pressed")
            run_booth()
except KeyboardInterrupt:
    print("Keyboard interrupt")
    GPIO.output(config.greenLed, False)
    GPIO.output(config.redLed, False)
    GPIO.cleanup()
    pygame.quit()
except Exception as inst:
    print(type(inst))
    print(inst.args)
    print(inst)
    print("Exited unexpectedly")
    GPIO.output(config.greenLed, False)
    GPIO.output(config.redLed, False)
    GPIO.cleanup()
    pygame.quit()
finally:
    GPIO.cleanup()
    pygame.quit()
