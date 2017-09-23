import RPi.GPIO as GPIO
import picamera
import time
import config
from PIL import Image

green_led = 11
red_led = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)

with picamera.PiCamera() as camera:
    camera.flash_mode = 'on'
    now = time.strftime("%Y-%m-%d-%H-%M-%S")

    try:
        for i in range(1,4):
            camera.hflip = True
            camera.start_preview()
            GPIO.output(green_led, True)
            img = Image.open('/home/pi/drumminhands_photobooth/instructions.png')
            pad = Image.new('RGB', (((img.size[0] + 31) // 32) * 32, ((img.size[1] + 15) // 16) * 16,))
            pad.paste(img, (0, 0))
            o = camera.add_overlay(pad.tobytes(), size=img.size)
            o.alpha = 128
            o.layer = 3
            time.sleep(3)
            GPIO.output(green_led, False)
            time.sleep(0.5)
            GPIO.output(green_led, True)
            camera.annotate_text = '3'
            time.sleep(1)
            GPIO.output(green_led, False)
            time.sleep(0.5)
            GPIO.output(green_led, True)
            camera.annotate_text = '2'
            time.sleep(1)
            GPIO.output(green_led, False)
            time.sleep(0.5)
            GPIO.output(green_led, True)
            camera.annotate_text = '1'
            time.sleep(1)
            GPIO.output(green_led, False)
            camera.annotate_text = ''
            time.sleep(0.25)
            filename = '/home/pi/Desktop/pose_' + now + '_' + str(i) + '.jpg'
            camera.hflip = False
            camera.capture(filename)
            camera.stop_preview()
            time.sleep(3)

        #Turn on the red LED
        GPIO.output(red_led, True)
        time.sleep(2)
        GPIO.output(red_led, False)

    finally:
        camera.close()
        GPIO.cleanup()
