import picamera
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

with picamera.PiCamera() as camera:
    camera.flash_mode = 'on'
    #camera.resolution = (high_res_w, high_res_h)
    now = time.strftime("%Y-%m-%d-%H-%M-%S")

    try:
        for i in range(1,4):
            #print("Begin. " + str(i))
            camera.hflip = True
            camera.start_preview()
            camera.annotate_text = 'Strike a pose!'
            time.sleep(2)
            camera.annotate_text = '3'
            time.sleep(1)
            camera.annotate_text = '2'
            time.sleep(1)
            camera.annotate_text = '1'
            time.sleep(1)
            camera.annotate_text = ''
            time.sleep(1)
            #GPIO.output(11, True)
            filename = '/home/pi/Desktop/pose_' + now + '_' + str(i) + '.jpg'
            camera.hflip = False
            camera.capture(filename)
            #GPIO.output(11, False)
            camera.stop_preview()
            #show_image(filename)
            time.sleep(3)
            #clear_screen()
            #print("End. " + str(i))
            if i == 4:
                break
            
    finally:
        camera.close()
        GPIO.cleanup()
