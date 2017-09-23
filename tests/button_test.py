from time import sleep
import RPi.GPIO as GPIO

sleepTime = 0.1
green_ledPin = 13
red_ledPin = 15
btnPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(green_ledPin, GPIO.OUT)
GPIO.setup(red_ledPin, GPIO.OUT)
GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(green_ledPin, True)
GPIO.output(red_ledPin, False)

try:
    while True:
        GPIO.output(green_ledPin, not GPIO.input(btnPin))
        GPIO.output(red_ledPin, GPIO.input(btnPin))
        sleep(sleepTime)
except KeyboardInterrupt:
    GPIO.cleanup()
