import mouse
import time
import random

while(True):
    print(mouse.get_position())
    time.sleep(0.1)


"""
while(True):
    mouse.move(random.choice([-2,0,2]), random.choice([-2,0,2]), absolute=False, duration=0)
    if(mouse.is_pressed("left")):#needs sudo??????
        break
"""