import RPi.GPIO as GPIO
from time import sleep

btnPin = 11
debounce = 0.25

GPIO.setmode(GPIO.BOARD)
GPIO.setup(btnPin, GPIO.IN)

try:
    while True:
        if GPIO.input(btnPin):
            sleep(debounce)
            print("Button Pressed")
            sleep(debounce)
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
