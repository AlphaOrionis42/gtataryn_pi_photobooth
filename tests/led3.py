from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, False)

while True:
    try:
        GPIO.output(13, True)
        sleep(.5)
        GPIO.output(13, False)
        sleep(.5)

    except KeyboardInterrupt:
        GPIO.cleanup()
