import RPi.GPIO as GPIO
from time import sleep

#red_led = 11
green_led = 13
#white_led = 12

while True:
        try:
                GPIO.setmode(GPIO.BOARD)
                #GPIO.setup(red_led, GPIO.OUT)
                GPIO.setup(green_led, GPIO.OUT)
                #GPIO.setup(white_led, GPIO.OUT)
                #GPIO.output(red_led, True)
                sleep(.5)
                GPIO.output(green_led, True)
                #sleep(.5)
                #GPIO.output(white_led, True)
                #sleep(1)
                #GPIO.output(red_led, False)
                sleep(.5)
                GPIO.output(green_led, False)
                #sleep(.5)
                #GPIO.output(white_led, False)
                #sleep(.5)             

        except KeyboardInturrupt:
                GPIO.cleanup()

