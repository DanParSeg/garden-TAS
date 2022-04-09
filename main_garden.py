import time
import cv2
import mss
import numpy as np



with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 150, "left": 80, "width": 1850, "height": 920}

    template = cv2.imread('4.png', cv2.IMREAD_COLOR)
    h, w = template.shape[:2]
    method = cv2.TM_CCOEFF_NORMED
    threshold = 0.90


    while True:
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        image = np.array(sct.grab(monitor))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB) #TODO: wtf is this jhasdgkhasdg

        res = cv2.matchTemplate(image, template, method)
        # fake out max_val for first run through loop
        max_val = 1
        while max_val > threshold:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val > threshold:
                #print("detectado")
                res[max_loc[1]-h//2:max_loc[1]+h//2+1, max_loc[0]-w//2:max_loc[0]+w//2+1] = 0   
                image = cv2.rectangle(image,(max_loc[0],max_loc[1]), (max_loc[0]+w+1, max_loc[1]+h+1), (0,255,0) )

        # Display the picture
        cv2.imshow('frame', image)
        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break