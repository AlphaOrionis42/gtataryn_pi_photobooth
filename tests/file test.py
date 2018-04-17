import os
import fnmatch

photo_files = os.listdir('/media/pi/P/pics/')
num_files = len(photo_files)
count = 0
print("Total files: " + str(num_files))

for i in range(0, num_files):
    #print(photo_files[i])
    if fnmatch.fnmatch(photo_files[i], '*sm.jpg'):
        print("File name: " + photo_files[i])
        count = count + 1

print("Small file count: " + str(count))
