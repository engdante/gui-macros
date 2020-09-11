import os
import sys
import time
import keyboard
from tkinter import *
from tkinter import messagebox
import macros as macros
import config

class Application(Frame):
        """GUI to hold widgets. """
        def __init__(self,master):
            super(Application,self).__init__(master)
            self.grid()
            self.createWidgets()

        def createWidgets(self):
            """GUI widgets. """
            #Label instructing the user to take a guess
            self.runningLabel = Label(self,text="Running", fg="blue", font=("Calibri", 14), padx=15, width=6)
            self.runningLabel.grid(row=0,column=0)
            self.gridLabel = Label(self,text="Grid ON", fg='green', font=("Calibri", 14), padx=15, width=6)
            self.gridLabel.grid(row=0,column=1)
            self.keyLabel = Label(self, text="_", fg='black', font=("Calibri", 14),relief="groove", padx=30, width=2)
            self.keyLabel.grid(row=0,column=2)
            # self.helpLabel = Label(self, text="CapsLk - Disable Macros", fg='black', font=("Calibri", 10), justify="left", padx=10)
            # self.helpLabel.grid(row=0,column=3)

        def update(self):
            disable_macros = config.appSettings["disable_macros"]
            disable_gridSnap = config.appSettings["disable_gridSnap"]
            if disable_macros=="1":
                runningText = config.appSettings["disable_macros_text_1"]
                runningColor = config.appSettings["disable_macros_color_1"]
            else:
                runningText = config.appSettings["disable_macros_text_0"]
                runningColor = config.appSettings["disable_macros_color_0"]
            
            if disable_gridSnap=="1":
                gridSnapText = config.appSettings["disable_gridSnap_text_1"]
                gridSnapColor = config.appSettings["disable_gridSnap_color_1"]
            else:
                gridSnapText = config.appSettings["disable_gridSnap_text_0"]
                gridSnapColor = config.appSettings["disable_gridSnap_color_0"]
            
            lastKey = config.appSettings["last_key"]

            self.runningLabel.config(text=runningText, fg=runningColor)
            self.gridLabel.config(text=gridSnapText, fg=gridSnapColor)
            self.keyLabel.config(text=lastKey)

            # print ("app update!!!")
            self.after(int(config.appSettings["gui_update_ms"]), self.update)

def runGui():
    root = Tk()
    root.title("Macro GUI / press CapsLock to disable macros")
    root.geometry('425x30')
    root.wm_attributes("-topmost", 1)
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

def capslock_state():
    import ctypes
    hllDll = ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x14
    cl_state = hllDll.GetKeyState(VK_CAPITAL) 
    if cl_state == 1 or cl_state == 65409:
        return True
    return False

def macros_togle():
    print ("macros_togle is running")
    capslock = capslock_state()
       
    if capslock:
        config.appSettings["disable_macros"] = "1"
        for key, value in config.appMacros.items():
            try:
                keyboard.remove_hotkey(key)
            except:
                print ("Error while removing {0} hotkey!".format(key))
    else:
        config.appSettings["disable_macros"] = "0"
        for key, value in config.appMacros.items():
            try:
                keyboard.add_hotkey(key, eval(value), args=(), suppress=True, timeout=1, trigger_on_release=True)
            except:
                print ("Error while adding {0} hotkey!".format(key))
    return

def lastKey(key):
    config.appSettings["last_key"] = key.name
    return

def mainApp():
    time.sleep(1)

    macros_togle()
    app.update()
    keyboard.add_hotkey('caps lock', macros_togle, args=(), suppress=False, timeout=1, trigger_on_release=False)
    keyboard.on_release(lastKey, suppress=False)

    # keyboard Package Documentation
    # https://github.com/boppreh/keyboard
    
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    thread1 = executor.submit(runGui)
    thread2 = executor.submit(mainApp)


