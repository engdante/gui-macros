#gui-macros
import numpy as np 
import cv2
#import time
import os
import sys
import pyautogui
from PIL import ImageGrab
from pynput import keyboard
from pynput.keyboard import Listener as KeyboardListener

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

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
    threshold = 0.8
    loc = np.where( res >= threshold)
    return loc

def on_press(key):
    print (key)
    if key == keyboard.Key.esc:
        sys.exit()
    
    icon_name = "Logo.png"
    find = find_pic_in_screen(icon_name)
    print (find)
    

scrPath = get_script_path()
imgPath = scrPath + "\Image"

with KeyboardListener(on_press=on_press) as listener:
        listener.join()

while True:
    frame = get_screen()
    frWidth = frame.shape[1]
    frHeight = frame.shape[0]
    frameS = cv2.resize(frame, (int(frWidth/4), int(frHeight/4)))
    cv2.imshow("Screen", frameS)
    
    logo = find_pic_in_screen("Logo.png")
    print (logo)
    
    if cv2.waitKey(2000) == 27:
        print('exitting loop')
        cv2.destroyAllWindows()
        break
    

    