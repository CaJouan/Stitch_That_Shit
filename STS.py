#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

#modules
from GUI import *
from tkinter import *


# Master widget and GUI creation
window = Tk()
window.title("Stitch That Shit !")
interface = Interface(window)


# Mainloop -> ready for events
window.mainloop()

# Closing the window
window.destroy()