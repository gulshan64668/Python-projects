import tkinter as tk
from tkinter import messagebox
import time

class VacuumAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Vacuum Agent - Step by Step Logic")
        # Fixed: Removed (px) - Tkinter only needs numbers
        self.root.geometry("700x550") 
        self.root.configure(bg="#f4f4f4")

        # 1. Environment Data: 1 means Dirty, 0 means Clean
        self.offices = ["Mam Rabia", "Sir Waseem", "Sir Waqar"]
        self.states = {name: 1 for name in self.offices} 
        
        self.setup_ui()

    def setup_ui(self):
        # Title
        tk.Label(self.root, text="AI VACUUM CLEANER AGENT", 
                 font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#333").pack(pady=15)

        # 2. Logic Logger
        self.status_var = tk.StringVar(value="System Ready: Press 'Start' to begin")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, 
                                     font=("Consolas", 11), fg="white", bg="#333", 
                                     width=70, height=3, wraplength=500, relief="sunken")
        self.status_label.pack(pady=10)

        # 3. Offices Visuals
        self.office_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.office_frame.pack(pady=20)

        self.office_widgets = {}
        for office in self.offices:
            container = tk.Frame(self.office_frame, bd=3, relief="flat", bg="#f4f4f4")
            container.pack(side=tk.LEFT, padx=20)
            
            lbl = tk.Label(container, text=f"{office}\n\n[DIRTY]", 
                           bg="#e74c3c", fg="white", width=15, height=6, 
                           font=("Arial", 10, "bold"), bd=5, relief="raised")
            lbl.pack()
            self.office_widgets[office] = lbl

        # 4. Control Button
        self.btn_start = tk.Button(self.root, text="START CLEANING PROCESS", 
                                   command=self.start_cleaning, 
                                   bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), 
                                   padx=20, pady=10, cursor="hand2")
        self.btn_start.pack(pady=20)

    def update_log(self, text, delay=1.2):
        self.status_var.set(f"LOG: {text}")
        self.root.update()
        time.sleep(delay)

    def start_cleaning(self):
        self.btn_start.config(state=tk.DISABLED, bg="#bdc3c7")
        
        for i, office in enumerate(self.offices):
            # STEP 1: Perception
            self.update_log(f"Agent moving towards {office}'s office...")
            self.office_widgets[office].config(relief="sunken", bd=8)
            
            self.update_log(f"PERCEIVING: Checking sensors for {office}...")
            
            # STEP 2: Logic/Action
            if self.states[office] == 1:
                self.update_log(f"LOGIC: Dust detected! Action triggered: [SUCK]")
                self.states[office] = 0
                self.office_widgets[office].config(text=f"{office}\n\n[CLEAN]", bg="#27ae60")
                self.update_log(f"ACTION SUCCESS: {office} is now clean.")
            else:
                self.update_log(f"LOGIC: Office is already clean.")

            # STEP 3: Movement Logic
            if i < len(self.offices) - 1:
                self.update_log(f"NEXT STEP: Moving 'Right' to the next location...")
                self.office_widgets[office].config(relief="raised", bd=5)
            else:
                self.update_log("GOAL REACHED: All offices processed.")
                self.office_widgets[office].config(relief="raised", bd=5)

        messagebox.showinfo("Assignment Complete", "Vacuum Agent has finished all tasks!")
        self.btn_start.config(state=tk.NORMAL, bg="#2ecc71")

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumAgentGUI(root)
    root.mainloop()
