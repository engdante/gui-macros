import numpy as np 
import cv2
import os
import sys
import time
import pyautogui
from PIL import ImageGrab
from configparser import ConfigParser

scrPath = os.path.dirname(os.path.realpath(sys.argv[0]))
imgPath = scrPath + "\Image"

def get_config():
    conf_file = ConfigParser()
    conf_file.read("macros.ini")
    return conf_file

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
    threshold = conf_file.getfloat("settings", "threshold")
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

def macGrid_view_togle():
    print ("macGrid_view_togle is running")
    icon_name = "view_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        return
    time.sleep(250)
    icon_name = "show_grid_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        return
    time.sleep(250)
    return

def macGrid_onoff_togle():
    print ("macGrid_onoff_togle is running")
    icon_name = "view_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        return
    time.sleep(250)
    icon_name = "snap_grid_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        return
    time.sleep(250)
    return

