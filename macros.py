import numpy as np 
import cv2
import os
import sys
import time
import pyautogui
from PIL import ImageGrab
from configparser import ConfigParser
from pynput import keyboard
from pynput.keyboard import Key, Controller
from pynput.keyboard import Listener as KeyboardListener

keyCont = Controller()


scrPath = os.path.dirname(os.path.realpath(sys.argv[0]))
imgPath = scrPath + "\Image"

def get_config():
    conf_file = ConfigParser()
    conf_file.read("macros.ini")
    return conf_file

def set_config(level1, level2, value):
    # print (level1, level2, value)
    conf_file = ConfigParser()
    conf_file.read("macros.ini")
    conf_file.set(level1, level2, value)
    with open('./macros.ini', 'w') as f:
        conf_file.write(f)

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

def capslock_state():
    import ctypes
    hllDll = ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)

def macMacros_togle():
    print ("macMacros_togle is running")
    # capslock = capslock_state()
    
    # if capslock == 65409:
    #     set_config("settings", "disable_macros","1")
    #     conf_file = get_config()
    #     # print ('disable_macros is {}'.format(conf_file.getboolean("settings", "disable_macros")))
    # else:
    #     set_config("settings", "disable_macros","0")
    #     conf_file = get_config()
    #     # print ('disable_macros is {}'.format(conf_file.getboolean("settings", "disable_macros")))
    return
    
def macGrid_view_togle():
    current_xy = pyautogui.position()
    print ("macGrid_view_togle is running")
    
    icon_name = "view_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        pass
    time.sleep(0.25)
    icon_name = "show_grid_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        pass
    time.sleep(0.25)

    pyautogui.moveTo(current_xy)
    return

def macGrid_onoff_togle():
    current_xy = pyautogui.position()
    print ("macGrid_onoff_togle is running")

    icon_name = "view_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        pass
    time.sleep(0.25)
    icon_name = "snap_grid_menu.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        pass
    time.sleep(0.25)

    pyautogui.moveTo(current_xy)

    conf_file = get_config()
    status_snap = conf_file.getboolean("settings", "disable_gridsnap")
    if status_snap:
        set_config("settings", "disable_gridSnap","0")
    else:
        set_config("settings", "disable_gridSnap","1")
    conf_file = get_config()

    return

def macMove():
    print ("macMove is running")
    current_xy = pyautogui.position()

    icon_name = "move.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        return
    time.sleep(0.25)

    icon_name = "copy_active.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        pass
    time.sleep(0.25)

    pyautogui.moveTo(current_xy)
    return

def macCopy():
    print ("macCopy is running")
    current_xy = pyautogui.position()

    icon_name = "move.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        return
    time.sleep(0.25)

    icon_name = "move_active.png"
    pic_xy = find_pic_in_screen(icon_name)
    try:
        pyautogui.click(pic_xy[0],pic_xy[1])
    except:
        pass
    time.sleep(0.25)

    pyautogui.moveTo(current_xy)
    return

