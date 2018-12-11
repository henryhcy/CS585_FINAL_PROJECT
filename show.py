import time

import psutil
from PIL import Image

# open and show image
im = Image.open('new0.jpg')
im.show()

# display image for 10 seconds
time.sleep(10)

# hide image
for proc in psutil.process_iter():
    if proc.name() == "display":
        proc.kill()
