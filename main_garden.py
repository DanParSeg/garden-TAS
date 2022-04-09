import time
import cv2
import mss
import numpy as np

def control_mouse():
    pass



with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 150, "left": 80, "width": 1850, "height": 920}

    template = cv2.imread('4.png', cv2.IMREAD_COLOR)
    template=cv2.cvtColor(np.array(template), cv2.COLOR_RGB2GRAY)
    method = cv2.TM_CCOEFF_NORMED
    threshold = 0.90

    scale_percent = 0.25
    # resize image
    template = cv2.resize(template, (int(template.shape[1] * scale_percent), int(template.shape[0] * scale_percent)))
    h, w = template.shape[:2]
    #cv2.imshow('template', template)


    while True:
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        image = np.array(sct.grab(monitor))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        # resize image
        image = cv2.resize(image, (int(image.shape[1] * scale_percent), int(image.shape[0] * scale_percent)))

        res = cv2.matchTemplate(image, template, method)
        # fake out max_val for first run through loop
        max_val = 1
        while max_val > threshold:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val > threshold:
                #print(max_val)
                res[max_loc[1]-h//2:max_loc[1]+h//2+1, max_loc[0]-w//2:max_loc[0]+w//2+1] = 0   
                image = cv2.rectangle(image,(max_loc[0],max_loc[1]), (max_loc[0]+w+1, max_loc[1]+h+1), (0,255,0) )
            #break

        # Display the picture
        #cv2.imshow('frame', image)
        print("fps: {}".format(1 / (time.time() - last_time)))

        control_mouse()

        # Press "q" to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break