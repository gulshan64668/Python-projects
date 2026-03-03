import tkinter as tk
from tkinter import messagebox

class MinimaxFinalVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minimax Alpha-Beta Tree Solver")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f6fa")

        # Terminal Values from your image
        self.leaf_values = [-1, 4, 2, 6, -3, -5, 0, 7]
        self.computed_values = {}
        self.pruned_branches = []
        self.best_path = []

        # UI Setup
        self.canvas = tk.Canvas(self.root, bg="white", width=850, height=450, relief="ridge", bd=2)
        self.canvas.pack(pady=20)

        self.info_text = tk.Text(self.root, height=6, width=90, font=("Consolas", 10))
        self.info_text.pack(pady=10)

        self.btn = tk.Button(self.root, text="Start Minimax Analysis", command=self.run_analysis, 
                             bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), padx=20)
        self.btn.pack()

    def minimax(self, depth, idx, is_max, alpha, beta, path):
        # Base Case: Leaf Nodes
        if depth == 3:
            return self.leaf_values[idx]

        if is_max:
            best = float('-inf')
            for i in range(2):
                val = self.minimax(depth + 1, idx * 2 + i, False, alpha, beta, path + [f"{depth}_{idx}"])
                if val > best:
                    best = val
                alpha = max(alpha, best)
                
                # Pruning Condition
                if beta <= alpha:
                    self.pruned_branches.append((depth + 1, idx * 2 + 1))
                    break
            self.computed_values[f"{depth}_{idx}"] = best
            return best
        else:
            best = float('inf')
            for i in range(2):
                val = self.minimax(depth + 1, idx * 2 + i, True, alpha, beta, path + [f"{depth}_{idx}"])
                if val < best:
                    best = val
                beta = min(beta, best)
                
                # Pruning Condition
                if beta <= alpha:
                    self.pruned_branches.append((depth + 1, idx * 2 + 1))
                    break
            self.computed_values[f"{depth}_{idx}"] = best
            return best

    def get_best_path(self):
        # Trace path from Root to Leaf
        path = ["0_0"]
        curr_val = self.computed_values["0_0"]
        
        # Level 1
        if self.computed_values.get("1_0") == curr_val: path.append("1_0")
        else: path.append("1_1")
        
        # Level 2
        last = path[-1]
        if self.computed_values.get(f"2_{int(last[-1])*2}") == curr_val: path.append(f"2_{int(last[-1])*2}")
        else: path.append(f"2_{int(last[-1])*2+1}")
        
        return path

    def draw_tree(self):
        self.canvas.delete("all")
        # Coordinates for nodes
        pos = {
            "0_0": (425, 50),
            "1_0": (225, 150), "1_1": (625, 150),
            "2_0": (125, 250), "2_1": (325, 250), "2_2": (525, 250), "2_3": (725, 250)
        }
        
        # Draw Lines & Pruning
        for parent, (px, py) in pos.items():
            d, i = map(int, parent.split('_'))
            for child_idx in range(2):
                child_key = f"{d+1}_{i*2+child_idx}"
                if child_key in pos or d+1 == 3:
                    cx, cy = (pos[child_key] if d+1 < 3 else (75 + (i*2+child_idx)*100, 350))
                    
                    # Highlight Best Path
                    color = "#e67e22" if parent in self.best_path and (child_key in self.best_path or (d==2 and self.leaf_values[i*2+child_idx] == self.computed_values[parent])) else "#bdc3c7"
                    width = 4 if color == "#e67e22" else 1
                    
                    self.canvas.create_line(px, py, cx, cy, fill=color, width=width)

        # Draw Nodes
        for key, (x, y) in pos.items():
            val = self.computed_values.get(key, "?")
            color = "#ff7675" if "0" in key.split('_')[0] else "#74b9ff"
            self.canvas.create_oval(x-22, y-22, x+22, y+22, fill=color, outline="black")
            self.canvas.create_text(x, y, text=str(val), font=("Arial", 10, "bold"))
            self.canvas.create_text(x, y-35, text=f"Node {key.replace('_','')}", font=("Arial", 8))

        # Draw Terminal Leaves
        for i, val in enumerate(self.leaf_values):
            x = 75 + i*100
            self.canvas.create_rectangle(x-15, 350-15, x+15, 350+15, fill="#dfe6e9")
            self.canvas.create_text(x, 350, text=str(val), font="Arial 9 bold")

    def run_analysis(self):
        self.computed_values = {}
        self.pruned_branches = []
        ans = self.minimax(0, 0, True, float('-inf'), float('inf'), [])
        self.best_path = self.get_best_path()
        self.draw_tree()
        
        # Step-by-Step Explanation
        steps = f"STEP 1: Starting at Root (Maximizer). Value found: {ans}\n"
        steps += f"STEP 2: Path Chosen: {' -> '.join(self.best_path)} -> Leaf Value {ans}\n"
       
        steps += f"RESULT: The AI 'Absolute' decision is to follow the Orange highlighted path."
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, steps)

if __name__ == "__main__":
    MinimaxFinalVisualizer().root.mainloop()

    
