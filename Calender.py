# simple calender without gui
# import time
# import calendar
# print(time.ctime())
# print(calendar.month(2024,9))

# calender with gui

import time
import calendar
import tkinter as tk
from tkinter import scrolledtext

# Function to show time and calendar
def show_info():
    current_time = time.ctime()
    month_cal = calendar.month(2024, 9)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Current Time:\n{current_time}\n\n")
    output_box.insert(tk.END, f"September 2024 Calendar:\n{month_cal}")

# GUI window
win = tk.Tk()
win.title("Time & Calendar Viewer")
win.geometry("400x300")

# Button to trigger info
btn = tk.Button(win, text="Show Time & Calendar", command=show_info)
btn.pack(pady=10)

# Output box
output_box = scrolledtext.ScrolledText(win, width=40, height=10)
output_box.pack(pady=10)

win.mainloop()
