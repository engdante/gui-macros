import os
import sys
import time
from configparser import ConfigParser
from pynput.keyboard import Listener as KeyboardListener
import tkinter as tk
from tkinter import messagebox
import macros as mac

#Global variables
os.system("python create_config_file.py")
global window

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

def on_press(key):
    conf_file = get_config()
    disable_macros = conf_file.getboolean("settings", "disable_macros")
    # print ('DISABLE MACROS is {}'.format(disable_macros))
    key_string = str(key)
    key_string = key_string.replace("\'", "")
    key_string = key_string.replace("\"", "")
    key_string = key_string.lower()

    set_config("settings", "last_key",key_string)
    conf_file = get_config()

    if disable_macros==True and key_string != 'key.caps_lock':
        print ('Macros are DIASBLE !!!')
        return
    conf_file = get_config()
    try:
        call_macros = conf_file.get("macros", key_string)
    except:
        call_macros = "fallback"
    call_macros = "mac." + call_macros + "()"
    #print (call_macros)
    eval(call_macros)
    listener.join()
    refreshGui()
    return

def runListener():
    with KeyboardListener(on_press=on_press, suppress=True) as listener:
        listener.join()
    return

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        exitApp()
    return

def exitApp():
    # sys.exit()
    global window
    window.destroy()
    os._exit(0)
    return

def runGui():
    global window
    window = tk.Tk()
    window.title('User Macros') 
    window.geometry('200x120')
    # content = tk.LabelFrame(window).pack()
    global running_label, grid_label, key_label 
    running_label = tk.Label(window, text="Running", fg="blue", font=("Calibri", 14))
    grid_label = tk.Label(window, text="Grid ON", fg='green', font=("Calibri", 14))
    key_label = tk.Label(window, text="_", fg='black', font=("Calibri", 14),relief="groove")
    help_label = tk.Label(window, text="CapsLk - Disable Macros", fg='black', font=("Calibri", 10), justify="left")
    
    # content.pack()
    running_label.pack()
    grid_label.pack()
    key_label.pack()
    help_label.pack()
   
    # content.grid(row=0, column=0)
    # running_label.grid(row=0, column=0)
    # grid_label.grid(row=0, column=1)
    # key_label.grid(row=0, column=2) 
    # help_label.grid(row=0, column=3)  
    
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

def refreshGui():
    global window
    conf_file = get_config()
    status_macros = conf_file.getboolean("settings", "disable_macros")
    status_snap = conf_file.getboolean("settings", "disable_gridSnap")
    last_key = conf_file.get("settings", "last_key")
    global running_label, grid_label, key_label 
    if status_macros:
        text = conf_file.get("settings", "disable_macros_text_1")
        color = conf_file.get("settings", "disable_macros_color_1")
        running_label.config(text=text, fg=color)
    else:
        text = conf_file.get("settings", "disable_macros_text_0")
        color = conf_file.get("settings", "disable_macros_color_0")
        running_label.config(text=text, fg=color)
    if status_snap:
        text = conf_file.get("settings", "disable_gridSnap_text_1")
        color = conf_file.get("settings", "disable_gridSnap_color_1")
        grid_label.config(text=text, fg=color)
    else:
        text = conf_file.get("settings", "disable_gridSnap_text_0")
        color = conf_file.get("settings", "disable_gridSnap_color_0")
        grid_label.config(text=text, fg=color)

    key_label.config(text=last_key)
    
    time.sleep(0.10)
    return

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    thread1 = executor.submit(runGui)
    thread2 = executor.submit(runListener)