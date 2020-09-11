import numpy as np 
import cv2
import os
import sys
import time
import keyboard
import mouse
from PIL import ImageGrab
import config

scrPath = os.path.dirname(os.path.realpath(sys.argv[0]))
imgPath = scrPath + "\Image"

def get_screen():
    img = ImageGrab.grab(bbox = None)
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    return frame

def find_pic_in_screen(pic_name):
    template = cv2.imread(imgPath + "/" + pic_name,0)
    tmWidth, tmHeight = template.shape[::-1]
    
    frame = get_screen()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= float(config.appSettings["threshold"]))
    #print (loc)
    if loc[0].size == 0:
        print ("{} is not find!".format(pic_name))
        return None
    pic_xy = np.array([round(np.average(loc[1])+tmWidth/2,0), round(np.average(loc[0])+tmHeight/2,0)])
    return pic_xy

def fallback():
    print ("fallback is running")
    return

def macGrid_view_togle():
    current_xy = mouse.get_position()
    print ("macGrid_view_togle is running")
    
    icon_name = "view_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        mouse.move(pic_xy[0],pic_xy[1],absolute=True)
        mouse.click()
    except:
        pass
    time.sleep(0.25)
    icon_name = "show_grid_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        mouse.move(pic_xy[0],pic_xy[1],absolute=True)
        mouse.click()
    except:
        pass
    time.sleep(0.25)

    mouse.move(current_xy[0],current_xy[1],absolute=True)
    return

def macGrid_onoff_togle():
    current_xy = mouse.get_position()
    print ("macGrid_onoff_togle is running")

    icon_name = "view_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        mouse.move(pic_xy[0],pic_xy[1],absolute=True)
        mouse.click()
    except:
        pass
    time.sleep(0.25)
    icon_name = "snap_grid_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        mouse.move(pic_xy[0],pic_xy[1],absolute=True)
        mouse.click()
    except:
        pass
    time.sleep(0.25)

    mouse.move(current_xy[0],current_xy[1],absolute=True)

    if config.appSettings["disable_gridSnap"] == "1":
        config.appSettings["disable_gridSnap"] = "0"
    else:
        config.appSettings["disable_gridSnap"] = "1"
    return

def macMove():
    print ("macMove is running")
    current_xy = mouse.get_position()

    icon_name = "move.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        mouse.move(pic_xy[0],pic_xy[1],absolute=True)
        mouse.click()
    except:
        return
    time.sleep(0.25)

    icon_name = "copy_active.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        mouse.move(pic_xy[0],pic_xy[1],absolute=True)
        mouse.click()
    except:
        pass
    time.sleep(0.25)

    mouse.move(current_xy[0],current_xy[1],absolute=True)
    return

def macCopy():
    print ("macCopy is running")
    current_xy = mouse.get_position()

    icon_name = "move.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        mouse.move(pic_xy[0],pic_xy[1],absolute=True)
        mouse.click()
    except:
        return
    time.sleep(0.25)

    icon_name = "move_active.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        mouse.move(pic_xy[0],pic_xy[1],absolute=True)
        mouse.click()
    except:
        pass
    time.sleep(0.25)

    mouse.move(current_xy[0],current_xy[1],absolute=True)
    return
