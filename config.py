# Config file for PhotoBooth app
# Author: Greg Tataryn

# Resolution Settings
monitor_h = 480
monitor_w = 800
photo_w = 1640
photo_h = 1232

btnPin = 11
greenLed = 13
redLed = 15
debounce = 0.25

# Camera config
camera_iso = 800 # ISO setting for camera
num_shots = 3 # How many shots to take

# Other constants
gif_delay = 100 # Delay between shots for GIF in miliseconds

# Replay variables
replay_count = 2 # Number of loops through the photo set
replay_wait = 1 # Delay to show each photo in seconds

# File path variables
save_path = '/media/pi/P/pics/' # Path to save the photos
gif_path = '/media/pi/P/gifs/' # Path for gifs
slide_path = '/home/pi/gtataryn_pi_photobooth/slides/' # Path for instructional and counddown slides

prep_delay = 2 # Delay for people to pose in seconds
shot_delay = 1 # Delay between photo captures in seconds
