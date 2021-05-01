import ctypes
import tkinter as tk
from win32api import GetSystemMetrics

print("win32api Width =", GetSystemMetrics(0))
print("win32api Height =", GetSystemMetrics(1))


root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print("tkinter Width =", screen_width)
print("tkinter Height =", screen_height)

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
print("dpiaware w={}, h={}".format(w, h))
