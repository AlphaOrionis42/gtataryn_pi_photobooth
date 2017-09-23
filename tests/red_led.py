import RPi.GPIO as GPIO
from time import sleep

redPin = 15
debounce = 0.25

GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.output(redPin, False)

try:
    while True:
        GPIO.output(redPin, True)
        sleep(.25)
        GPIO.output(redPin, False)
        sleep(.25)
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
