import os
import sys
from configparser import ConfigParser
from pynput import keyboard
from pynput.keyboard import Listener as KeyboardListener

import macros as mac

#Global variables
os.system("python create_config_file.py")

def get_config():
    conf_file = ConfigParser()
    conf_file.read("macros.ini")
    return conf_file

def on_press(key):
    conf_file = get_config()
    key_string = str(key)
    key_string = key_string.replace("\'", "")
    key_string = key_string.replace("\"", "")
    print (key_string)
    try:
        call_macros = conf_file.get("macros", key_string)
    except:
        call_macros = "fallback"
    call_macros = "mac." + call_macros + "()"
    #print (call_macros)
    eval(call_macros)
   
with KeyboardListener(on_press=on_press) as listener:
    listener.join()