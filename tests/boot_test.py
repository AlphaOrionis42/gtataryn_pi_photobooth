from time import sleep
import RPi.GPIO as GPIO

red_ledPin = 15
green_ledPin = 13
btnPin = 11
debounce = .25

GPIO.setmode(GPIO.BOARD)
GPIO.setup(red_ledPin, GPIO.OUT)
GPIO.setup(green_ledPin, GPIO.OUT)
GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(red_ledPin, False)
GPIO.output(green_ledPin, False)

try:
    for x in range(0,5):
        GPIO.output(green_ledPin, True)
        sleep(.25)
        GPIO.output(green_ledPin, False)
        sleep(.25)

    while True:
        GPIO.output(green_ledPin, True)
        if GPIO.input(btnPin):
            sleep(debounce)
            GPIO.output(green_ledPin, False)
            GPIO.output(red_ledPin, True)
            sleep(1)
            GPIO.output(red_ledPin, False)

except KeyboardInterrupt:
    GPIO.cleanup()
