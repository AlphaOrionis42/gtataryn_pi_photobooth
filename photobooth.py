#!/usr/bin/env python
# Author: Greg Tataryn

import os
import sys
import time
from time import sleep
import fnmatch
import RPi.GPIO as GPIO
import picamera
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_ESCAPE
from PIL import Image
import config

# Local variables
DEBUG = False # Debug toggle
RUN = True #Run variable for main program
RUN_SHOW = True # Run variable for the slide show
LAST_IMG = 0 # Used inside the slide show to track the last photo shown

#######################
# GPIO Initialization #
#######################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(config.btnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(config.greenLed, GPIO.OUT)
GPIO.setup(config.redLed, GPIO.OUT)
GPIO.setup(config.whiteLed, GPIO.OUT)
GPIO.output(config.greenLed, False)
GPIO.output(config.redLed, False)
GPIO.output(config.whiteLed, False)

#########################
# Pygame Initialization #
#########################
pygame.init()
pygame.display.set_mode((config.monitor_w, config.monitor_h))
SCREEN = pygame.display.get_surface()
pygame.mouse.set_visible(False)
pygame.display.toggle_fullscreen()

################################################
# Function to clear the slides from the screen #
################################################
def clear_screen():
    # Fill the screen with black
    SCREEN.fill((0, 0, 0))
    pygame.display.flip()

##################################################
# Function to check for input to end the program #
# Use the escape key to exit                     #
##################################################
def chk_input(events):
    global RUN
    global RUN_SHOW
    for event in events:
        # If the input received was an escape key, then exit the program.
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            RUN = False
            RUN_SHOW = False
            pygame.quit()
            sys.exit()
        # If the input was a mouse button press, return true
        # used for ending the slide show when users tap the touch screen.
        elif event.type == MOUSEBUTTONDOWN:
            if DEBUG:
                print("Mouse button")
            RUN_SHOW = False

####################################################
# Function to overlay images to the camera preview #
####################################################
def overlay_img(img_path, cam):
    img = Image.open(img_path)
    overlay = cam.add_overlay(img.tobytes(), size=img.size)
    overlay.alpha = 100
    overlay.layer = 3
    return overlay

#############################################
# Function to display an image using pygame #
#############################################
def show_img(img_path, offset_x, offset_y):
    clear_screen()

    img = pygame.image.load(img_path)
    img = img.convert()

    SCREEN.blit(img, (offset_x, offset_y))
    pygame.display.flip()

#############################################
# Function to fade in an image using pygame #
#############################################
def fade_img(img_path, offset_x, offset_y):
    done = False
    global RUN_SHOW
    alpha = 0
    img = pygame.image.load(img_path)
    if DEBUG:
        print('Begin fade')
    while not done:
        chk_input(pygame.event.get())
        if not RUN_SHOW:
            done = True
            return

        img.set_alpha(alpha)
        SCREEN.blit(img, (offset_x, offset_y))
        pygame.display.flip()
        alpha += config.alpha_vel

        if alpha >= 255:
            done = True


###############################################
# Function to make animated GIF of the photos #
###############################################
def make_gif(jpg_group, timestamp):
    if DEBUG:
        print('Making animated gif')

    graphicsmagick = "gm convert -delay " + str(config.gif_delay) + " " + \
        jpg_group + "*.jpg" + " " + config.gif_path + "photobooth_" + timestamp + \
        ".gif"
    os.system(graphicsmagick)

#############################
# Function to resize photos #
#############################
def resize_imgs(jpg_group):
    if DEBUG:
        print("Resizing images")
    for shot in range(1, config.num_shots+1):
        # Use Graphics Magick to resize the files for display on a screen.
        # Uses the monitor resolution from confic.py
        graphicsmagick = "gm convert -size " + str(config.monitor_w) + "x" + \
            str(config.monitor_h) + " " + jpg_group + "_" + str(shot) + \
            ".jpg -thumbnail " + str(config.monitor_w) + "x" + str(config.monitor_h) + \
            " " + jpg_group + "_" + str(shot) + "_sm.jpg"
        if DEBUG:
            print(graphicsmagick)
        os.system(graphicsmagick)

###################################################
# Function to display the preview images to users #
###################################################
def img_replay(img_group):
    clear_screen()
    for i in range(0, config.replay_count):
        for j in range(1, config.num_shots+1):
            if DEBUG:
                print("Replay round: " + str(i) + " Photo: " + img_group + "_" + str(j) + "_sm.jpg")
            fade_img(img_group + "_" + str(j) + "_sm.jpg", 80, 0)
            sleep(config.replay_wait)

###################################################
# Function to run slide show of  all photos taken #
###################################################
def run_slide_show():
    file_list = os.listdir(config.save_path)
    num_files = len(file_list)
    slide_count = 0
    GPIO.output(config.whiteLed, False)
    global RUN_SHOW
    global LAST_IMG
    if DEBUG:
        print(str(LAST_IMG))
    RUN_SHOW = True
    while RUN_SHOW:
        chk_input(pygame.event.get())
        if not RUN_SHOW:
            break
        if num_files >= 3:
            clear_screen()
            if LAST_IMG > num_files:
                if DEBUG:
                    print("Last image higher than number of files")
                    print(str(LAST_IMG))
                LAST_IMG = 0
                if DEBUG:
                    print(str(LAST_IMG))
            for i in range(LAST_IMG, num_files):
                if DEBUG:
                    print("i = " + str(i))
                    print("last_img = " + str(LAST_IMG))
                chk_input(pygame.event.get())
                if not RUN_SHOW:
                    break
                if fnmatch.fnmatch(file_list[i], '*sm.jpg'):
                    fade_img(config.save_path + file_list[i], 80, 0)
                    wait_for_input(config.slide_wait, 'mouse')
                    if not RUN_SHOW:
                        break
                    slide_count += 1
                    LAST_IMG = i

                if num_files < 6 and slide_count == num_files:
                    fade_img(config.slide_path + 'start.png', 0, 0)
                    wait_for_input(config.slide_wait, 'mouse')
                    if not RUN_SHOW:
                        break
                    clear_screen()
                    slide_count = 0
                elif slide_count == 6:
                    fade_img(config.slide_path + 'start.png', 0, 0)
                    wait_for_input(config.slide_wait, 'mouse')
                    if not RUN_SHOW:
                        break
                    clear_screen()
                    slide_count = 0
        else:
            RUN_SHOW = False
            break
    GPIO.output(config.whiteLed, True)
    show_img(config.slide_path + 'intro.png', 0, 0)

#############################
# Function to run the booth #
#############################
def run_booth():
    if DEBUG:
        print("Running photobooth")
    GPIO.output(config.whiteLed, False)
    now = time.strftime("%Y%m%d%H%M%S")
    if DEBUG:
        print(now)
    # Try to run the preview and take a series of photots
    try:
        #camera = picamera.PiCamera(sensor_mode=4, resolution='1640x1232')
        camera = picamera.PiCamera()
        camera.iso = config.camera_iso

        #camera.preview_fullscreen = True
        clear_screen()
        for i in range(1, config.num_shots+1):
            chk_input(pygame.event.get())
            GPIO.output(config.redLed, False)
            GPIO.output(config.greenLed, False)
            camera.hflip = True
            camera.resolution = (config.monitor_w, config.monitor_h)
            camera.start_preview()
            filename = config.save_path + 'photobooth_' + now + '_' + str(i) + '.jpg'
            sleep(.5)
            overlay = overlay_img(config.slide_path + 'pose.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(config.prep_delay)
            camera.remove_overlay(overlay)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            overlay = overlay_img(config.slide_path + 'countdown3.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(overlay)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            overlay = overlay_img(config.slide_path + 'countdown2.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(overlay)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            overlay = overlay_img(config.slide_path + 'countdown1.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(overlay)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            camera.hflip = False
            camera.stop_preview()
            camera.resolution = (config.photo_w, config.photo_h)
            GPIO.output(config.redLed, True)
            camera.capture(filename)
            if DEBUG:
                print(filename)
            sleep(config.shot_delay)
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

    if DEBUG:
        print("Wait for resize")
    show_img(config.slide_path + "wait.png", 0, 0)
    resize_imgs(config.save_path + "photobooth_" + now)
    #print("Wait for GIF")
    #make_gif(config.save_path + "photobooth_" + now, now)
    clear_screen()
    img_replay(config.save_path + "photobooth_" + now)
    GPIO.output(config.redLed, False)
    GPIO.output(config.greenLed, True)
    GPIO.output(config.whiteLed, True)
    clear_screen()
    show_img(config.slide_path + 'intro.png', 0, 0)

##################################################
# Function that runs on startup to blink the LED #
# Lets us know everything is working.            #
##################################################
def startup():
    for x in range(1, ):
        GPIO.output(config.greenLed, True)
        time.sleep(0.25)
        GPIO.output(config.greenLed, False)
        time.sleep(0.25)
    GPIO.output(config.redLed, True)

###################################################
# Function to handle waiting for the button press #
# Taks in a wait_time in seconds for how long it  #
# should wait for a button press.                 #
###################################################
def wait_for_input(wait_time, input_type):
    timer = time.time() + wait_time
    btn_pressed = False
    if DEBUG:
        print('Input type awaited: ' + input_type)
    if input_type == 'mouse':
        while time.time() <= timer:
            chk_input(pygame.event.get())
            if not RUN or not RUN_SHOW:
                timer = time.time() + 1
                return
    if input_type == 'button':
        while time.time() <= timer:
            chk_input(pygame.event.get())
            if GPIO.input(config.btnPin):
                sleep(config.debounce)
                btn_pressed = True
                run_booth()
            chk_input(pygame.event.get())
        # If the button was pressed, wait for another press before proceeding on.
        if btn_pressed:
            wait_for_input(wait_time, input_type)

################
# Main Program #
################
def main():
    # Run startup to blink the green light.
    startup()
    time.sleep(0.5)
    show_img(config.slide_path + 'intro.png', 0, 0)
    while RUN:
        if DEBUG:
            print('Top of main run')
        # Turn off the red LED and turn on the green LED.
        GPIO.output(config.redLed, False)
        GPIO.output(config.greenLed, True)
        GPIO.output(config.whiteLed, True)
        wait_for_input(config.btn_wait, 'button')
        # Check for input to exit and begin the slide show.
        chk_input(pygame.event.get())
        run_slide_show()
        if DEBUG:
            print('Bottom of main run')

####################
# Try Running Main #
####################
try:
    main()
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
    