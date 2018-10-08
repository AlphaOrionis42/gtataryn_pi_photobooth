# Config file for PhotoBooth app
# Author: Greg Tataryn
import sys
import os
# Resolution Settings
monitor_h = 480
monitor_w = 800
photo_w = 1640
photo_h = 1232

# GPIO pins
btnPin = 11
greenLed = 13
redLed = 15
whiteLed = 12
debounce = 0.25 # Time to wait on a button press to avoid multiple inputs on single press

# Camera config
camera_iso = 800 # ISO setting for camera
num_shots = 3 # How many shots to take

# Other constants
gif_delay = 100 # Delay between shots for GIF in miliseconds

# Replay variables
replay_count = 2 # Number of loops through the photo set
slide_wait = 3
replay_wait = 2 # Delay to show each photo in seconds
alpha_vel = 5 # The speed at which the alpha changes to fade in images

# File path variables
#media_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Pictures')
media_paths = []
img_paths = []
small_paths = []
gif_paths = []

if len(os.listdir('/media/pi')) > 0:
    for x in os.listdir('/media/pi'):
        media_paths.append('/media/pi/' + x)
else:
    media_paths.append(os.path.expanduser('~/Pictures/'))

for y in media_paths:
    if not os.path.exists(y + '/pics'):
        os.mkdir(y + '/pics/')
        if not os.path.exists(y + '/pics/FullSize'):
            os.mkdir(y + '/pics/FullSize/')
        if not os.path.exists(y + '/pics/Playback'):
            os.mkdir(y + '/pics/Playback/')
        
    if not os.path.exists(y + '/gifs'):
        os.mkdir(y + '/gifs/')
        
    img_paths.append(y + '/pics/FullSize/')
    small_paths.append(y + '/pics/Playback/')
    gif_paths.append(y + '/gifs/')

playback_path = small_paths[0]
capture_path = os.path.dirname(os.path.realpath(__file__)) + '/tmp/' # temp path to take pictures
slide_path = os.path.dirname(os.path.realpath(__file__)) + '/slides/' # Path for instructional and counddown slides

# Time delay options
prep_delay = 2 # Delay for people to pose in seconds
shot_delay = 1 # Delay between photo captures in seconds
btn_wait = 5
make_gif = False
