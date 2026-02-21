import tkinter as tk
from tkinter import messagebox
import time

class EightQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Queens Visualizer")
        self.board_size = 8
        self.board = [-1] * self.board_size
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)
        
        for r in range(self.board_size):
            row_btns = []
            for c in range(self.board_size):
                # Checkerboard pattern colors
                color = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
                btn = tk.Label(self.frame, text="", width=4, height=2, 
                               font=('Arial', 18, 'bold'), bg=color, 
                               relief="raised", borderwidth=1)
                btn.grid(row=r, column=c)
                row_btns.append(btn)
            self.buttons.append(row_btns)
            
        self.start_btn = tk.Button(self.root, text="Start Visualizer", 
                                   command=self.solve, bg="blue", fg="white")
        self.start_btn.pack(pady=10)

    def is_safe(self, row, col):
        for i in range(row):
            # Check column and diagonals
            if self.board[i] == col or \
               abs(self.board[i] - col) == abs(i - row):
                return False
        return True

    def solve(self):
        self.start_btn.config(state="disabled")
        if self.backtrack(0):
            messagebox.showinfo("Done", "All 8 Queens Placed!")
        else:
            messagebox.showerror("Error", "No solution found.")

    def backtrack(self, row):
        if row == self.board_size:
            return True
        
        for col in range(self.board_size):
            # Visual feedback: highlighting current cell
            self.buttons[row][col].config(bg="yellow")
            self.root.update()
            time.sleep(0.1) # Slow down for visualization
            
            if self.is_safe(row, col):
                self.board[row] = col
                self.buttons[row][col].config(text="♛", fg="black") # Queen icon
                self.root.update()
                
                if self.backtrack(row + 1):
                    return True
                
                # Backtrack: remove queen
                self.board[row] = -1
                self.buttons[row][col].config(text="")
            
            # Reset color
            orig_color = "#eeeed2" if (row + col) % 2 == 0 else "#769656"
            self.buttons[row][col].config(bg=orig_color)
            self.root.update()
            
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = EightQueensGUI(root)
    root.mainloop()
