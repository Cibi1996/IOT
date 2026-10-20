import os
import subprocess
import time
from datetime import datetime

import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput

MEDIA_DIR = os.path.expanduser("~/cctv/media")
FPS = 15
PRE_SECONDS = 3       # seconds kept from before the motion
POST_SECONDS = 5      # keep recording this long after motion stops
PIXEL_DIFF = 25
MOTION_LEVEL = 0.01

os.makedirs(MEDIA_DIR, exist_ok=True)

picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (1280, 720)},                      # for video and photos
    lores={"size": (320, 240), "format": "YUV420"},  # for detection
    controls={"FrameRate": FPS},
)
picam2.configure(config)

# Encoder that always keeps the last few seconds in memory
encoder = H264Encoder(bitrate=1_500_000, repeat=True)
encoder.output = CircularOutput(buffersize=PRE_SECONDS * FPS)

picam2.start()
picam2.start_encoder(encoder)
time.sleep(2)

prev = None
recording = False
last_motion = 0
video_path = None

print("Motion camera running... Ctrl+C to stop")

try:
    while True:
        frame = picam2.capture_array("lores")[:240, :320].astype(np.int16)

        if prev is not None:
            changed = (np.abs(frame - prev) > PIXEL_DIFF).mean()
            now = time.time()

            if changed > MOTION_LEVEL:
                last_motion = now

                if not recording:
                    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    video_path = os.path.join(MEDIA_DIR, stamp + ".h264")
                    photo_path = os.path.join(MEDIA_DIR, stamp + ".jpg")

                    encoder.output.fileoutput = video_path
                    encoder.output.start()        # writes the buffered 3s, then keeps recording
                    picam2.capture_file(photo_path)
                    recording = True
                    print(f"MOTION ({changed:.1%}) -> recording {stamp}")

            elif recording and now - last_motion > POST_SECONDS:
                encoder.output.stop()
                recording = False
                mp4_path = video_path.replace(".h264", ".mp4")
                # Convert to mp4 in the background, then delete the raw file
                subprocess.Popen(
                    f'ffmpeg -y -loglevel error -framerate {FPS} -i "{video_path}" '
                    f'-c copy "{mp4_path}" && rm "{video_path}"',
                    shell=True,
                )
                print(f"  saved {os.path.basename(mp4_path)}")

        prev = frame
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    if recording:
        encoder.output.stop()
    picam2.stop_encoder()
    picam2.stop()
