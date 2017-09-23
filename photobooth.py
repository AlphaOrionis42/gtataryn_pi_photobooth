#!/usr/bin/env python
# Author: Greg Tataryn

import config
import RPi.GPIO as GPIO
import picamera
import sys
import pygame
from pygame.locals import *
import time
from PIL import Image

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
#pygame.init()
#pygame.display.set_mode((config.slide_w, config.slide_h))
#screen = pygame.display.get_surface()
#pygame.mouse.set_visible(False)
#pygame.display.toggle_gullscreen()

def overlay_img(imgPath, cam):
    img = Image.open(imgPath)
    oLay = cam.add_overlay(img.tobytes(), size=img.size)
    oLay.alpha = 100
    oLay.layer = 3
    return oLay

#def show_slide():

def run_booth():
    print("Running photobooth")
    GPIO.output(config.greenLed, False)
    now = time.strftime("%Y%m%d%H%M%S")
    print(now)
    # Try to run the preview and take a series of photots
    try:
        camera = picamera.PiCamera(sensor_mode=4)
        camera.iso = config.camera_iso
        #camera.resolution = (1640, 1232)
        for i in range(1,config.num_shots+1):
            GPIO.output(config.redLed, False)
            camera.hflip = True
            #camera.vflip = True
            camera.start_preview()
            filename = config.save_path + '_' + now + '_' + str(i) + '.jpg'
            time.sleep(.5)
            o = overlay_img(config.slide_path + 'pose.png', camera)
            GPIO.output(config.greenLed, True)
            time.sleep(2)
            camera.remove_overlay(o)
            GPIO.output(config.greenLed, False)
            time.sleep(.5)
            o = overlay_img(config.slide_path + 'countdown3.png', camera)
            GPIO.output(config.greenLed, True)
            time.sleep(.5)
            camera.remove_overlay(o)
            GPIO.output(config.greenLed, False)
            time.sleep(.5)
            o = overlay_img(config.slide_path + 'countdown2.png', camera)
            GPIO.output(config.greenLed, True)
            time.sleep(.5)
            camera.remove_overlay(o)
            GPIO.output(config.greenLed, False)
            time.sleep(.5)
            o = overlay_img(config.slide_path + 'countdown1.png', camera)
            GPIO.output(config.greenLed, True)
            time.sleep(.5)
            camera.remove_overlay(o)
            GPIO.output(config.greenLed, False)
            time.sleep(.5)
            camera.hflip = False
            GPIO.output(config.redLed, True)
            camera.capture(filename)
            print(filename)
            camera.stop_preview()
            time.sleep(2)
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

def Startup():
    for x in range(1,5):
        GPIO.output(config.greenLed, True)
        time.sleep(0.25)
        GPIO.output(config.greenLed, False)
        time.sleep(0.25)
    GPIO.output(config.redLed, True)

try:
    # Run startup to blink the green light.
    Startup()
    time.sleep(.25)
    while True:
        GPIO.output(config.redLed, False)
        GPIO.output(config.greenLed, True)
        #print("Green LED on")
        if GPIO.input(config.btnPin):
            time.sleep(config.debounce)
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
#finally:
#    GPIO.cleanup()
#    pygame.quit()
