import tkinter as tk
from datetime import datetime
import screen_brightness_control as sbc

# -------------------------------
# KNOWLEDGE BASE & INFERENCE
# -------------------------------
knowledge_base = {"HIGH": 100, "MEDIUM": 60, "LOW": 30, "NIGHT": 10}

def infer_light_level(hour):
    if 6 <= hour < 11: return "HIGH"
    elif 11 <= hour < 17: return "MEDIUM"
    elif 17 <= hour < 20: return "LOW"
    else: return "NIGHT"

def apply_brightness():
    current_hour = datetime.now().hour
    light_level = infer_light_level(current_hour)
    brightness_value = knowledge_base[light_level]

    try:
        sbc.set_brightness(brightness_value)
        status_var.set(f"Mode: {light_level}")
        value_var.set(f"{brightness_value}%")
        msg_label.config(text="Brightness Adjusted Successfully!", fg="#00FF7F") # Spring Green
    except:
        msg_label.config(text="Error: Hardware Not Supported", fg="#FF4500") # Orange Red

# -------------------------------
# BEAUTIFUL GUI DESIGN
# -------------------------------
root = tk.Tk()
root.title("AI Brightness Agent")
root.geometry("450x400")
root.configure(bg="#1e1e2e") # Deep Dark Blue Background

# Variables for Dynamic Updates
status_var = tk.StringVar(value="Mode: Unknown")
value_var = tk.StringVar(value="--%")

# Main Container
main_frame = tk.Frame(root, bg="#282a36", bd=2, relief="flat")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=320)

# Title Header
title_label = tk.Label(
    main_frame, text="KNOWLEDGE-BASED AGENT", 
    bg="#282a36", fg="#bd93f9", font=("Segoe UI", 14, "bold"), pady=10
)
title_label.pack()

separator = tk.Frame(main_frame, height=2, bd=0, bg="#44475a")
separator.pack(fill="x", padx=20, pady=5)

# Display Area
info_frame = tk.Frame(main_frame, bg="#282a36")
info_frame.pack(pady=20)

tk.Label(info_frame, textvariable=status_var, bg="#282a36", fg="#f8f8f2", font=("Segoe UI", 12)).pack()
tk.Label(info_frame, textvariable=value_var, bg="#282a36", fg="#50fa7b", font=("Segoe UI", 30, "bold")).pack()

# Stylish Button
btn_adjust = tk.Button(
    main_frame, text="ADJUST NOW", command=apply_brightness,
    bg="#6272a4", fg="white", font=("Segoe UI", 10, "bold"),
    activebackground="#bd93f9", activeforeground="white",
    relief="flat", padx=30, pady=10, cursor="hand2"
)
btn_adjust.pack(pady=10)

# Message Footer
msg_label = tk.Label(
    main_frame, text="System Ready", 
    bg="#282a36", fg="#6272a4", font=("Segoe UI", 9, "italic")
)
msg_label.pack(side="bottom", pady=10)

root.mainloop()
