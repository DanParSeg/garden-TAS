import time
import cv2
import mss
import numpy as np

import mouse

monitor = {"top": 150, "left": 95, "width": 1850, "height": 920}
scale_percent = 0.25
mouse_direction=5

def mouse_in_square(squares):
    global scale_percent, monitor
    pos=mouse.get_position()
    
    for s in squares:
        margin=7
        s=list(s)
        s[0]=s[0]/scale_percent+monitor["left"]-margin
        s[1]=s[1]/scale_percent+monitor["top"]-margin
        s[2]=s[2]/scale_percent+monitor["left"]+margin
        s[3]=s[3]/scale_percent+monitor["top"]+margin
        s=tuple(s)
        if(pos[0]>s[0] and pos[1]>s[1] and pos[0]<s[2] and pos[1]<s[3]):
            return (True,s)
    return (False,None)

def control_mouse(squares):
    global mouse_direction, monitor
    vertical_move=41
    print(mouse.get_position())
    if(mouse_in_square(squares)[0]):
        print("good")
        sq=mouse_in_square(squares)[1]
        sq_center=((sq[0]+sq[2])/2,(sq[1]+sq[3])/2)
        mouse.move(sq_center[0], sq_center[1],absolute=True, duration=0)
        while(mouse_in_square(squares)[0]):
            mouse.move(mouse_direction, 0,absolute=False, duration=0)
    if(mouse.get_position()[0]+35>=(monitor["left"]+monitor["width"])):#change line if right
        print("change line")
        
        mouse.move(-20,vertical_move,absolute=False, duration=0)
        mouse_direction=-5
    elif(mouse.get_position()[0]-20<monitor["left"]):#change line if left
        print("change line")
        
        mouse.move(20,vertical_move,absolute=False, duration=0)
        mouse_direction=5
    else:
        print("change")
        
        pos=mouse.get_position()
        mouse.move(0, 0, absolute=True, duration=0)
        mouse.move(pos[0],pos[1], absolute=True, duration=0)
        time.sleep(0.1)



with mss.mss() as sct:
    # Part of the screen to capture
    

    template = cv2.imread('4.png', cv2.IMREAD_COLOR)
    template=cv2.cvtColor(np.array(template), cv2.COLOR_RGB2GRAY)
    method = cv2.TM_CCOEFF_NORMED
    threshold = 0.80

    
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

        squares=[]
        # fake out max_val for first run through loop
        max_val = 1
        while max_val > threshold:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val > threshold:
                res[max_loc[1]-h//2:max_loc[1]+h//2+1, max_loc[0]-w//2:max_loc[0]+w//2+1] = 0
                image = cv2.rectangle(image,(max_loc[0],max_loc[1]), (max_loc[0]+w+1, max_loc[1]+h+1), (0,255,0) )
                squares.append((max_loc[0],max_loc[1], (max_loc[0]+w+1),(max_loc[1]+h+1)))

        print(squares)
        # Display the picture
        cv2.imshow('frame', image)
        print("fps: {}".format(1 / (time.time() - last_time)))

        control_mouse(squares)

        # Press "q" to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break