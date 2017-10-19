"""
This module runs a photo booth on a Raspberry Pi
It makes use of the Raspberry Pi camera modeule
It uses GPIO pins to control LED lights and accept button presses
It also makes use of a touch screen or mouse.
"""
#!/usr/bin/env python
# Author: Greg Tataryn

import os
import sys
import fnmatch
import time
from time import sleep
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
#background = pygame.Surface((config.monitor_w, config.monitor_h))
#background.fill((0, 0, 0))
pygame.mouse.set_visible(False)
pygame.display.toggle_fullscreen()

def clear_screen():
    """ Function to clear the screen filling it with black"""
    # Fill the screen with black
    SCREEN.fill((0, 0, 0))
    pygame.display.flip()

def chk_input(events):
    """
    Function to check for input to end the program
    Use the escape key to exit, the program, mouse/screen click to exit slide show

    Args:
    events: a pygame event stack
    """
    global RUN, RUN_SHOW
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
            #print("Mouse button")
            RUN_SHOW = False

def overlay_img(img_path, cam):
    """
    Function to overlay images to the camera preview

    Args:
    img_path: the path to the image to be used
    cam: a PiCamera object
    """
    img = Image.open(img_path)
    olay = cam.add_overlay(img.tobytes(), size=img.size)
    olay.alpha = 100
    olay.layer = 3
    return olay

def show_img(img_path, offset_x, offset_y):
    """
    Function to display an image using pygame

    Arge:
    img_path: the path to the image
    offset_x: how many pixels to offset the image horizontally
    offset_y: how many pixels to offset the image vertically
    """
    clear_screen()

    img = pygame.image.load(img_path)
    img = img.convert()

    SCREEN.blit(img, (offset_x, offset_y))
    pygame.display.flip()

def fade_img(img_path, offset_x, offset_y):
    """
    Function to fade in an image using pygame
    Similar to show image only it fades an image in gradually

    Args:
    img_path: The path to the image
    offset_x: how many pixels to offset the image horizontally
    offset_y: how many pixels to offset the image vertically
    """
    done = False
    global RUN_SHOW
    alpha = 0
    img = pygame.image.load(img_path)
    #clear_screen()
    #print('begin fade image')
    while not done:
        #print('Alpha value: ' + str(alpha))
        chk_input(pygame.event.get())
        if not RUN_SHOW:
            done = True
            #print('end fade image')
            return

        #background.fill((0,0,0))
        img.set_alpha(alpha)
        SCREEN.blit(img, (offset_x, offset_y))
        pygame.display.flip()
        alpha += config.alpha_vel

        if alpha >= 255:
            #print('end fade image')
            done = True

def make_gif(jpg_group, time_stamp):
    """
    Function to turn a series of images into an animated GIF

    Args:
    jpg_group: the group of images to be joined together.
    All photos in the group will have similar names.
    time_stamp: the time stamp used in the group
    """
    if DEBUG:
        print('Making animated gif')

    graphicsmagick = "gm convert -delay " + str(config.gif_delay) + " " + \
        jpg_group + "*.jpg" + " " + config.gif_path + "photobooth_" + time_stamp + \
        ".gif"
    os.system(graphicsmagick)

def resize_imgs(jpg_group):
    """
    Function to resize images. Used to resize larger photos to display on smaller screens

    Args:
    jpg_group: the group of photos to be resized. All photos in the group will have similar names.
    """
    print("Resizing images")
    for shot in range(1, config.num_shots+1):
        # Use Graphics Magick to resize the files for display on a screen.
        # Uses the monitor resolution from confic.py
        graphicsmagick = "gm convert -size " + str(config.monitor_w) + "x" + \
            str(config.monitor_h) + " " + jpg_group + "_" + str(shot) + \
            ".jpg -thumbnail " + str(config.monitor_w) + "x" + str(config.monitor_h) + \
            " " + jpg_group + "_" + str(shot) + "_sm.jpg"
        print(graphicsmagick)
        os.system(graphicsmagick)

def img_replay(jpg_group):
    """
    Function to replay the series of photos just taken a prescribed number of times

    Args:
    jpg_group: the series of photos to show. All photos in the group will have similar names.
    """
    clear_screen()
    for i in range(0, config.replay_count):
        for j in range(1, config.num_shots+1):
            print("Loop: " + str(i) + " Photo: " + str(j))
            fade_img(jpg_group + "_" + str(j) + "_sm.jpg", 80, 0)
            sleep(config.replay_wait)

def run_slide_show():
    """
    Function to run the slide show screen saver
    """
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
                    print("LAST_IMG = " + str(LAST_IMG))
                chk_input(pygame.event.get())
                if not RUN_SHOW:
                    break
                if fnmatch.fnmatch(file_list[i], '*sm.jpg'):
                    fade_img(config.save_path + file_list[i], 80, 0)
                    wait_for_input(config.slide_wait, 'mouse')
                    #print('Done waiting. Run_show = ' + str(RUN_SHOW))
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

def run_booth():
    """
    Function to run the photobooth
    """
    if DEBUG:
        print("Running photobooth")
    GPIO.output(config.whiteLed, False)
    now = time.strftime("%Y%m%d%H%M%S")
    if DEBUG:
        print(now)
    # Try to RUN the preview and take a series of photots
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
            countdown = overlay_img(config.slide_path + 'pose.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(config.prep_delay)
            camera.remove_overlay(countdown)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            countdown = overlay_img(config.slide_path + 'countdown3.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(countdown)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            countdown = overlay_img(config.slide_path + 'countdown2.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(countdown)
            GPIO.output(config.greenLed, False)
            sleep(.5)
            countdown = overlay_img(config.slide_path + 'countdown1.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(.5)
            camera.remove_overlay(countdown)
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
        print("Error in function RUN_booth")
        print(type(err))
        print(err.args)
        print(err)
        camera.stop_preview()
        camera.close()
    finally:
        camera.stop_preview()
        camera.close()

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
# Function that RUNs on startup to blink the LED #
# Lets us know everything is working.            #
##################################################
def startup():
    for x in range(1, 5):
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
    global RUN, RUN_SHOW
    #print('Input type awaited: ' + input_type)
    if input_type == 'mouse':
        while time.time() <= timer:
            #print('Run show before check? ' + str(RUN_SHOW))
            chk_input(pygame.event.get())
            #print('Run show after check? ' + str(RUN_SHOW))
            if not RUN or not RUN_SHOW:
                #print('Return to parent')
                timer = time.time() + 1
                return
    if input_type == 'button':
        while time.time() <= timer:
            chk_input(pygame.event.get())
            if GPIO.input(config.btnPin):
                sleep(config.debounce)
                btn_pressed = True
                RUN_booth()
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
        print('Top of main RUN')
        # Turn off the red LED and turn on the green LED.
        GPIO.output(config.redLed, False)
        GPIO.output(config.greenLed, True)
        GPIO.output(config.whiteLed, True)
        # Check for input to exit, then wait for the button press.
        #chk_input(pygame.event.get())
        wait_for_input(config.btn_wait, 'button')
        # Check again for input to exit and begin the slide show.
        chk_input(pygame.event.get())
        RUN_slide_show()
        print('Bottom of main RUN')

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
