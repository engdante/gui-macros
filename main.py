import os
import sys
from configparser import ConfigParser
from pynput import keyboard
from pynput.keyboard import Listener as KeyboardListener

import macros as macros

#Global variables
os.system('python create_config_file.py')

def get_config():
    conf_file = ConfigParser()
    conf_file.read('macros.ini')
    return conf_file

def on_press(key):
    conf_file = get_config()
    key_string = str(key)
    try:
        call_macros = conf_file.get('macros', str(key))
    except:
        call_macros = "fallback"
    call_macros = "macros." + call_macros + "()"
    # print (call_macros)
    eval(call_macros)
   
with KeyboardListener(on_press=on_press) as listener:
    listener.join()