import os
import sys
from configparser import ConfigParser
from pynput.keyboard import Listener as KeyboardListener
import tkinter as tk
from tkinter import messagebox
import macros as mac

#Global variables
os.system("python create_config_file.py")
global closeApp
global window
closeApp = False

def get_config():
    conf_file = ConfigParser()
    conf_file.read("macros.ini")
    return conf_file

def on_press(key):
    conf_file = get_config()
    disable_macros = conf_file.getboolean("settings", "disable_macros")
    # print ('DISABLE MACROS is {}'.format(disable_macros))
    key_string = str(key)
    key_string = key_string.replace("\'", "")
    key_string = key_string.replace("\"", "")
    key_string = key_string.lower()
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

def runListener():
    with KeyboardListener(on_press=on_press) as listener:
        listener.join()

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
    window.geometry('425x40')
    running_label = tk.Label(window, text="Running", fg="blue", font=("Calibri", 14),padx=15, pady=5).grid(row=0, column=0)
    grid_label = tk.Label(window, text="Grid ON", fg='green', font=("Calibri", 14),padx=15, pady=5).grid(row=0, column=1)
    key_label = tk.Label(window, text="_", fg='black', font=("Calibri", 14),padx=20, pady=5,relief="groove").grid(row=0, column=2)
    help_label_1 = tk.Label(window, text="CapsLk - Disable Macros", fg='black', font=("Calibri", 10),padx=15, pady=0, justify="left").grid(row=0, column=3)
    
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    thread1 = executor.submit(runGui)
    thread2 = executor.submit(runListener)