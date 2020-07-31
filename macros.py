import numpy as np 
import cv2
import os
import sys
#import time
import pyautogui
from PIL import ImageGrab

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
    conf_file = get_config()
    threshold = conf_file.getfloat('settings', 'threshold')
    print (threshold)
    loc = np.where( res >= threshold)
    #print (loc)
    if loc[0].size == 0:
        print ("{} is not find!".format(pic_name))
        return None
    pic_xy = np.array([round(np.average(loc[1])+tmWidth/2,0), round(np.average(loc[0])+tmHeight/2,0)])
    return pic_xy

def fallback():
    print ("fallback is running")
    return

def macExit():
    print ("macExit is running")
    sys.exit()
    return

