import RPi.GPIO as GPIO
from time import sleep

btnPin = 11
greenPin = 13
redPin = 15
debounce = 0.25


GPIO.setmode(GPIO.BOARD)
GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT)
GPIO.output(greenPin, False)
GPIO.output(redPin, False)

def Startup():
    for x in range(1,5):
        print(x)
        GPIO.output(greenPin, True)
        sleep(.25)
        GPIO.output(greenPin, False)
        sleep(.25)
    GPIO.output(redPin, True)
    sleep(1)

def flash_lights():
    GPIO.output(redPin, True)
    GPIO.output(greenPin, False)
    sleep(.5)
    GPIO.output(redPin, False)
    GPIO.output(greenPin, True)

try:
    Startup()
    GPIO.add_event_detect(btnPin, GPIO.FALLING)
    while True:
        GPIO.output(redPin, False)
        GPIO.output(greenPin, True)
        if GPIO.event_detected(btnPin):
            sleep(debounce)
            flash_lights()
        #GPIO.wait_for_edge(btnPin, GPIO.FALLING)
        #sleep(debounce)
        #GPIO.output(redPin, True)
        #GPIO.output(greenPin, False)
        #print("Button pressed")
        #sleep(.5)
        #GPIO.output(redPin, False)
        #GPIO.output(greenPin, True)

except KeyboardInterrupt:
    print("Keyboard interrupt")

#except:
#    print("Did not exit normally")

finally:
    GPIO.output(redPin, False)
    GPIO.output(greenPin, False)
    GPIO.cleanup()
