#!/usr/bin/env python
# Author: Greg Tataryn

import os
import config
import shutil
import fnmatch
import RPi.GPIO as GPIO
import picamera
import sys
import pygame
from pygame.locals import *
import time
from time import sleep
from PIL import Image
# Local variables
debug = False # Debug toggle
run = True #Run variable for main program
run_show = True # Run variable for the slide show
last_img = 0 # Used inside the slide show to track the last photo shown
transform_x = config.monitor_w
transform_y = config.monitor_h
offset_x = 0
offset_y = 0

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
screen = pygame.display.get_surface()
background = pygame.Surface((config.monitor_w, config.monitor_h))
background.fill((0,0,0))
pygame.mouse.set_visible(False)
pygame.display.toggle_fullscreen()

################################################
# Function to clear the slides from the screen #
################################################
def clear_screen():
    # Fill the screen with black
    screen.fill( (0,0,0) )
    pygame.display.flip()

##################################################
# Function to check for input to end the program #
# Use the escape key to exit                     #
##################################################
def chk_input(events):
    global run
    global run_show
    for event in events:
        # If the input received was an escape key, then exit the program.
        if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
            run = False
            run_show = False
            pygame.quit()
            sys.exit()
        # If the input was a mouse button press, return true
        # used for ending the slide show when users tap the touch screen.
        elif event.type == MOUSEBUTTONDOWN:
            if debug:
                print("Mouse button")
            run_show = False

#################################
# Function to set imgage offset #
#################################
def set_demensions(img_w, img_h):
    global transform_y, transform_x, offset_y, offset_x

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
        offset_x = offset_y = 0

####################################################
# Function to overlay images to the camera preview #
####################################################
def overlay_img(imgPath, cam):
    img = Image.open(imgPath)
    oLay = cam.add_overlay(img.tobytes(), size=img.size)
    oLay.alpha = 100
    oLay.layer = 3
    return oLay

#############################################
# Function to display an image using pygame #
#############################################
def show_img(img_path):
    clear_screen()

    img = pygame.image.load(img_path)
    img = img.convert()

    set_demensions(img.get_width(), img.get_height())

    screen.blit(img, (offset_x, offset_y))
    pygame.display.flip()

#############################################
# Function to fade in an image using pygame #
#############################################
def fade_img(img_path):
    done = False
    global run_show
    alpha = 0
    img = pygame.image.load(img_path)
    set_demensions(img.get_width(), img.get_height())
    clear_screen()
    if debug:
        print('begin fade image')
    while not done:
        chk_input(pygame.event.get())
        if not run_show:
            done = True
            if debug:
                print('end fade image')
            return

        img.set_alpha(alpha)
        screen.blit(img, (offset_x, offset_y))
        pygame.display.flip()
        alpha += config.alpha_vel

        if alpha >= 255:
            if debug:
                print('end fade image')
            done = True


###############################################
# Function to make animated GIF of the photos #
###############################################
def make_gif(jpg_group, ts):
    if debug:
        print('Making animated gif')
    
    graphicsmagick = "gm convert -delay " + str(config.gif_delay) + " " + \
        jpg_group + "*.jpg" + " " + config.gif_path + "photobooth_" + ts + \
        ".gif"
    os.system(graphicsmagick)

#############################
# Function to resize photos #
#############################
def resize_imgs(jpg_group):
    if debug:
        print("Resizing images")
    for x in range(1, config.num_shots+1):
        # Use Graphics Magick to resize the files for display on a screen. Uses the monitor resolution from confic.py
        graphicsmagick = "gm convert -size " + str(config.monitor_w) + "x" + \
            str(config.monitor_h) + " " + jpg_group + "_" + str(x) + \
            ".jpg -thumbnail " + str(config.monitor_w) + "x" + str(config.monitor_h) + \
            " " + jpg_group + "_" + str(x) + "_sm.jpg"
        if debug:
            print(graphicsmagick)
        os.system(graphicsmagick)

#######################################################
# Function to move images from temp folder to storage #
#######################################################
def copy_imgs(img_grp):
    if debug:
        print("Copying images")

    
    for x in range(1, config.num_shots+1):
        sm_src = config.capture_path + img_grp + "_" + str(x) + "_sm.jpg"
        orig_src = config.capture_path + img_grp + "_" + str(x) + ".jpg"
        for i in range(len(config.img_paths)):
            sm_dest = config.small_paths[i] + img_grp + "_" + str(x) + "_sm.jpg"
            orig_dest = config.img_paths[i] + img_grp + "_" + str(x) + ".jpg"
            if debug:
                print("Original source: " + orig_src)
                print("Original destination: " + orig_dest)
                print("Small source: " + sm_src)
                print("Small destination: " + sm_dest)
            shutil.copyfile(sm_src, sm_dest)
            shutil.copyfile(orig_src, orig_dest)
        os.remove(sm_src)
        os.remove(orig_src)

###################################################
# Function to display the preview images to users #
###################################################
def img_replay(jpg_group):
    clear_screen()
    for i in range(0, config.replay_count):
        for j in range(1,config.num_shots+1):
            if debug:
                print("Loop: " + str(i) + " Photo: " + str(j))
                print("Image file: " + jpg_group + "_" + str(j) + "_sm.jpg")
            show_img(jpg_group + "_" + str(j) + "_sm.jpg")
            sleep(config.replay_wait)

###################################################
# Function to run slide show of  all photos taken #
###################################################
def run_slide_show():
    file_list = sorted(os.listdir(config.playback_path))
    num_files = len(file_list)
    if debug:
        print("Number of files: " + str(num_files))
    slide_count = 0
    GPIO.output(config.whiteLed, False)
    global run_show
    global last_img
    if debug:
        print("Last image number: " + str(last_img))
    run_show = True
    while run_show:
        chk_input(pygame.event.get())
        if not run_show:
            break
        if num_files >= 3:
            clear_screen()
            if last_img > num_files:
                if debug:
                    print("Last image higher than number of files")
                    print(str(last_img))
                last_img = 0
                if debug:
                    print(str(last_img))
            for i in range(last_img,num_files):
                if debug:
                    print("i = " + str(i))
                    print("last_img = " + str(last_img))
                    print("slide_count = " + str(slide_count))
                    print("num_files = " + str(num_files))
                chk_input(pygame.event.get())
                if not run_show:
                    break
                fade_img(config.playback_path + file_list[i])
                wait_for_input(config.slide_wait, 'mouse')
                if not run_show:
                   break
                slide_count += 1
                last_img = i

                if last_img == (num_files - 1):
                    if debug:
                        print("More than 6 files and at the end")
                    fade_img(config.slide_path + 'start.png')
                    wait_for_input(config.slide_wait, 'mouse')
                    if not run_show:
                        break
                    clear_screen()
                    slide_count = 0
                    last_img = 0
                elif slide_count == 6:
                    fade_img(config.slide_path + 'start.png')
                    wait_for_input(config.slide_wait, 'mouse')
                    if not run_show:
                        break
                    clear_screen()
                    slide_count = 0
                    if last_img == (num_files - 1):
                        last_img = 0
        else:
            run_show = False
            break
    GPIO.output(config.whiteLed, True)
    show_img(config.slide_path + 'intro.png')
                    

#############################
# Function to run the booth #
#############################
def run_booth():
    if debug:
        print("Running photobooth")
    GPIO.output(config.whiteLed, False)
    now = time.strftime("%Y%m%d%H%M%S")
    if debug:
        print(now)
    # Try to run the preview and take a series of photots
    try:
        camera = picamera.PiCamera()
        camera.iso = config.camera_iso
        
        clear_screen()
        for i in range(1,config.num_shots+1):
            chk_input(pygame.event.get())
            GPIO.output(config.redLed, False)
            GPIO.output(config.greenLed, False)
            camera.hflip = True
            camera.resolution = (config.monitor_w, config.monitor_h)
            camera.start_preview()
            filename = 'photobooth_' + now + '_' + str(i) + '.jpg'
            sleep(.5)
            o = overlay_img(config.slide_path + 'pose.png', camera)
            GPIO.output(config.greenLed, True)
            sleep(config.prep_delay)
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
            camera.resolution = (config.photo_w, config.photo_h)
            GPIO.output(config.redLed, True)
            camera.capture(config.capture_path + filename)
            if debug:
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
        
    if debug:
        print("Wait for resize")
    show_img(config.slide_path + "wait.png")
    resize_imgs(config.capture_path + "photobooth_" + now)
    copy_imgs("photobooth_" + now)
    if debug:
        print("Wait for GIF")
    if config.make_gif:
        make_gif(config.save_path + "photobooth_" + now, now)
    clear_screen()
    img_replay(config.playback_path + "photobooth_" + now)
    GPIO.output(config.redLed, False)
    GPIO.output(config.greenLed, True)
    GPIO.output(config.whiteLed, True)
    clear_screen()    
    show_img(config.slide_path + 'intro.png')

##################################################
# Function that runs on startup to blink the LED #
# Lets us know everything is working.            #
##################################################
def Startup():
    for x in range(1,5):
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
    if debug:
        print('Input type awaited: ' + input_type)
    if input_type == 'mouse':
        while time.time() <= timer:
            #if debug:
                #print('Run show before check? ' + str(run_show))
            chk_input(pygame.event.get())
            #if debug:
                #print('Run show after check? ' + str(run_show))
            if run == False or run_show == False:
                if debug:
                    print('Return to parent')
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
    Startup()
    time.sleep(0.5)
    show_img(config.slide_path + 'intro.png')
    while run:
        if debug:
            print('Top of main run')
        # Turn off the red LED and turn on the green LED.
        GPIO.output(config.redLed, False)
        GPIO.output(config.greenLed, True)
        GPIO.output(config.whiteLed, True)
        # Check for input to exit, then wait for the button press.
        #chk_input(pygame.event.get())
        wait_for_input(config.btn_wait, 'button')
        # Check again for input to exit and begin the slide show.
        chk_input(pygame.event.get())
        run_slide_show()
        if debug:
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
