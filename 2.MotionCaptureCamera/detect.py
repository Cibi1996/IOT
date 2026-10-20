import time
import numpy as np
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (320, 240), "format": "YUV420"}
)
picam2.configure(config)
picam2.start()
time.sleep(2)  # let the camera adjust to the light

prev = None

while True:
    # Brightness of each pixel, as a 240x320 grid
    frame = picam2.capture_array()[:240, :320].astype(np.int16)

    if prev is not None:
        diff = np.abs(frame - prev)       # how much each pixel changed
        changed = (diff > 25).mean()      # fraction of pixels that changed a lot
        if changed > 0.01:
            print(f"MOTION! {changed:.1%} of the frame changed")

    prev = frame
    time.sleep(0.2)
