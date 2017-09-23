from time import sleep
import RPi.GPIO as GPIO
import datetime

debounce = .25
btnPin = 11
green_ledPin = 13
red_ledPin = 15
#btn_ledPin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(btnPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(red_ledPin, GPIO.OUT)
GPIO.setup(green_ledPin, GPIO.OUT)
#GPIO.setup(btn_ledPin, GPIO.OUT)
GPIO.output(red_ledPin, False)
GPIO.output(green_ledPin, True)
#GPIO.output(btn_ledPin, True)



try:
    while True:
        if (GPIO.input(btnPin) == True):
            GPIO.output(red_ledPin, True)
            GPIO.output(green_ledPin, False)
            print("Pushed the button")
            sleep(debounce)
            GPIO.output(red_ledPin, False)
            GPIO.output(green_ledPin, True)
            sleep(debounce)
            
except KeyboardInterrupt:
    GPIO.cleanup()
