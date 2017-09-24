import os

print("Start")
graphicsmagick = "gm convert -delay 100 /media/pi/P/pics/photobooth_20170923143155*.jpg /media/pi/P/gifs/photobooth_20170923143155.gif"
os.system(graphicsmagick)
print("End")
