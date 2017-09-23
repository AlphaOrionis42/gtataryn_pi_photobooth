import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, False)

try:
    while True:
        GPIO.output(11, True)
        sleep(.25)
        GPIO.output(11, False)
        sleep(.25)

except KeyboardInterrupt:
    GPIO.output(11, False)
    GPIO.cleanup()
