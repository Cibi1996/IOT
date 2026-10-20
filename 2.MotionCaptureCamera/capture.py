import os
import time
from datetime import datetime

import numpy as np
from picamera2 import Picamera2

PHOTO_DIR = os.path.expanduser("~/cctv/photos")
COOLDOWN = 5          # seconds between photos
PIXEL_DIFF = 25       # how much a pixel must change to count
MOTION_LEVEL = 0.01   # fraction of the frame that must change (1%)

os.makedirs(PHOTO_DIR, exist_ok=True)

picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (1280, 720)},                      # for saved photos
    lores={"size": (320, 240), "format": "YUV420"},  # for detection
)
picam2.configure(config)
picam2.start()
time.sleep(2)

prev = None
last_photo = 0

print("Watching for motion... Ctrl+C to stop")

while True:
    frame = picam2.capture_array("lores")[:240, :320].astype(np.int16)

    if prev is not None:
        changed = (np.abs(frame - prev) > PIXEL_DIFF).mean()

        if changed > MOTION_LEVEL and time.time() - last_photo > COOLDOWN:
            name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            path = os.path.join(PHOTO_DIR, name)
            picam2.capture_file(path)
            last_photo = time.time()
            print(f"MOTION ({changed:.1%}) -> saved {name}")

    prev = frame
    time.sleep(0.2)
