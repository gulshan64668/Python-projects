import tkinter as tk
from tkinter import messagebox
import time

class EightPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver (BFS Logic)")
        
        # Initial State (Mixed) and Goal State
        self.state = [1, 2, 3, 4, 0, 5, 7, 8, 6] 
        self.goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        
        self.buttons = []
        self.create_widgets()
        self.update_grid()

    def create_widgets(self):
        # Create 3x3 Grid of Buttons
        self.frame = tk.Frame(self.root, bg='gray')
        self.frame.pack(pady=20)
        
        for i in range(9):
            btn = tk.Button(self.frame, text="", font=('Arial', 24, 'bold'), 
                            width=5, height=2, bg="white")
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
        
        # Control Buttons
        self.solve_btn = tk.Button(self.root, text="Solve Step-by-Step", 
                                   command=self.solve_puzzle, bg="green", fg="white")
        self.solve_btn.pack(pady=10)

    def update_grid(self, current_state=None):
        if current_state is None: current_state = self.state
        for i in range(9):
            val = current_state[i]
            self.buttons[i].config(text=str(val) if val != 0 else "", 
                                   bg="#add8e6" if val != 0 else "gray")
        self.root.update()

    def get_neighbors(self, state):
        neighbors = []
        zero_pos = state.index(0)
        row, col = zero_pos // 3, zero_pos % 3
        
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 3 and 0 <= c < 3:
                new_state = list(state)
                target_pos = r * 3 + c
                new_state[zero_pos], new_state[target_pos] = new_state[target_pos], new_state[zero_pos]
                neighbors.append(new_state)
        return neighbors

    def solve_puzzle(self):
        # BFS Logic to find path
        queue = [(self.state, [])]
        visited = {tuple(self.state)}
        
        while queue:
            current, path = queue.pop(0)
            
            if current == self.goal:
                self.animate_solution(path)
                return

            for neighbor in self.get_neighbors(current):
                if tuple(neighbor) not in visited:
                    visited.add(tuple(neighbor))
                    queue.append((neighbor, path + [neighbor]))

    def animate_solution(self, path):
        for step in path:
            self.update_grid(step)
            time.sleep(0.5) # Delay to show the step
        messagebox.showinfo("Success", "Goal State Reached!")

if __name__ == "__main__":
    root = tk.Tk()
    gui = EightPuzzleGUI(root)
    root.mainloop()
