import os
import sys
import time
from configparser import ConfigParser
# from pynput.keyboard import Key, Controller
import ctypes
from pynput.keyboard import Listener as KeyboardListener
from tkinter import *
from tkinter import messagebox
# import macros.py file
import macros as mac

os.system("python create_config_file.py")
# keyCont = Controller()

class Application(Frame):
        """GUI to hold widgets. """
        def __init__(self,master):
            super(Application,self).__init__(master)
            self.grid()
            self.createWidgets()

        def createWidgets(self):
            """GUI widgets. """
            #Label instructing the user to take a guess
            self.runningLabel = Label(self,text="Running", fg="blue", font=("Calibri", 14), padx=10)
            self.runningLabel.grid(row=0,column=0)
            self.gridLabel = Label(self,text="Grid ON", fg='green', font=("Calibri", 14), padx=10)
            self.gridLabel.grid(row=0,column=1)
            self.keyLabel = Label(self, text="_", fg='black', font=("Calibri", 14),relief="groove", padx=30)
            self.keyLabel.grid(row=0,column=2)
            self.helpLabel = Label(self, text="CapsLk - Disable Macros", fg='black', font=("Calibri", 10), justify="left", padx=10)
            self.helpLabel.grid(row=0,column=3)

        def update(self):
            conf_file = get_config()
            disable_macros = conf_file.getboolean("settings", "disable_macros")
            disable_gridSnap = conf_file.getboolean("settings", "disable_gridSnap")
            if disable_macros==True:
                runningText = conf_file.get("settings", "disable_macros_text_1")
                runningColor = conf_file.get("settings", "disable_macros_color_1")
            else:
                runningText = conf_file.get("settings", "disable_macros_text_0")
                runningColor = conf_file.get("settings", "disable_macros_color_0")
            
            if disable_gridSnap==True:
                gridSnapText = conf_file.get("settings", "disable_gridSnap_text_1")
                gridSnapColor = conf_file.get("settings", "disable_gridSnap_color_1")
            else:
                gridSnapText = conf_file.get("settings", "disable_gridSnap_text_0")
                gridSnapColor = conf_file.get("settings", "disable_gridSnap_color_0")
            
            lastKey = conf_file.get("settings", "last_key")

            self.runningLabel.config(text=runningText, fg=runningColor)
            self.gridLabel.config(text=gridSnapText, fg=gridSnapColor)
            self.keyLabel.config(text=lastKey)

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
    key_string = str(key)
    key_string = key_string.replace("\'", "")
    key_string = key_string.replace("\"", "")
    key_string = key_string.lower()

    set_config("settings", "last_key",key_string)
    conf_file = get_config()
    disable_macros = conf_file.getboolean("settings", "disable_macros")

    if disable_macros==True and key_string != 'key.caps_lock':
        print ('Macros are DIASBLE !!!')
        return
    try:
        call_macros = conf_file.get("macros", key_string)
    except:
        call_macros = "fallback"
    call_macros = "mac." + call_macros + "()"
    eval(call_macros)

    app.update()
    return   

def win32_event_filter(msg, data):
    if msg == 256 and data.vkCode == 20:
        dll = ctypes.WinDLL('User32.dll')
        # msdn.microsoft.com/en-us/library/dd375731
        VK_CAPITAL = 0X14
        if dll.GetKeyState(VK_CAPITAL) == 0:
            dll.keybd_event(VK_CAPITAL, 0X3a, 0X1, 0)
            time.sleep(0.01)
            dll.keybd_event(VK_CAPITAL, 0X3a, 0X3, 0)
            time.sleep(0.01)
        
        print("test")
        
    return

def runGui():
    root = Tk()
    root.title("Macro GUI")
    root.geometry('425x30')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    global app
    app = Application(root)
    root.mainloop()

def on_closing():
    answer = messagebox.askquestion("Quit", "Do you want to quit?")
    if answer == "yes":
        exitApp()
    else:
        return

def exitApp():
    global app
    app.destroy()
    os._exit(0)
    return

def mainApp():
    time.sleep(1)
   
    with KeyboardListener(on_press=on_press, win32_event_filter=win32_event_filter, suppress=True) as listener:
        listener.join()
    
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    thread1 = executor.submit(runGui)
    thread2 = executor.submit(mainApp)
