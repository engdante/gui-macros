import os
import sys
import time
import ctypes
from pynput.keyboard import Listener as KeyboardListener
from tkinter import *
from tkinter import messagebox


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

# Проблемът е в следващите три функции
def on_press(key): #Изпълнява се когато се натисне клавиш
    print (str(key)  + " is pressed")
    return   

def win32_event_filter(msg, data): #Изпълнява се когато се натисне клавиш
    if msg == 256 and data.vkCode == 20:
        dll = ctypes.WinDLL('User32.dll')
        # msdn.microsoft.com/en-us/library/dd375731
        VK_CAPITAL = 0X14
        capsStatus = dll.GetKeyState(VK_CAPITAL)
        print ("Caps Lock is pressed. Status is :" + str(capsStatus))
    return

def mainApp():
    time.sleep(1)
   
    with KeyboardListener(on_press=on_press, win32_event_filter=win32_event_filter, suppress=True) as listener:
        listener.join()

    # pynput Package Documentation
    # https://pynput.readthedocs.io/en/latest/index.html
    
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    thread1 = executor.submit(runGui)
    thread2 = executor.submit(mainApp)
