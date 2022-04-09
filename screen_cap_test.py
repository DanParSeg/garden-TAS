import time
import cv2
import mss
import numpy as np

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 150, "left": 80, "width": 1900, "height": 920}

    while True:
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow('frame', img)

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break