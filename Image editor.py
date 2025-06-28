import cv2
from tkinter import *
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

# Function to open an image file
def open_image():
    global img, img_display, img_backup
    img_path = filedialog.askopenfilename(filetypes=[("Image files", ".jpg;.jpeg;.png;.bmp")])
    if img_path:
        img = cv2.imread(img_path)
        img_backup = img.copy()
        redo_stack = []  # Clear redo stack on new image load
        display_image(img)

# Function to rotate the image
def rotate_image():
    global img, img_backup
    if img is not None:
        img_backup = img.copy()  # Backup the current image
        try:
            angle = simpledialog.askinteger("Input", "Enter the rotation angle (in degrees, e.g., 90, 180, 270):")
            if angle is not None:
                (h, w) = img.shape[:2]
                center = (w // 2, h // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                img = cv2.warpAffine(img, rotation_matrix, (w, h))
                display_image(img)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No image loaded to rotate.")
        
def save_image():
    if img is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", ".jpg"), ("PNG", ".png")])
        if save_path:
            cv2.imwrite(save_path, img)

# Function to display the image on the canvas
def display_image(image):
    global img_display
    if len(image.shape) == 2: 
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    img_display = ImageTk.PhotoImage(image=image)
    canvas.config(width=img_display.width(), height=img_display.height())
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=NW, image=img_display)

def activate_crop_mode():
    canvas.bind("<Button-1>", start_crop)
    canvas.bind("<B1-Motion>", draw_crop_rectangle)
    canvas.bind("<ButtonRelease-1>", end_crop)
    print("Crop mode activated! Click and drag to select the crop region.")

def start_crop(event):
    global crop_start_x, crop_start_y
    if img is not None:
        crop_start_x, crop_start_y = event.x, event.y

def draw_crop_rectangle(event):
    global crop_start_x, crop_start_y
    if img is not None:
        canvas.delete("crop_rectangle")
        canvas.create_rectangle(crop_start_x, crop_start_y, event.x, event.y, outline="red", tag="crop_rectangle")

def end_crop(event):
    global img, crop_start_x, crop_start_y, img_backup
    if img is not None:
        x1, y1 = crop_start_x, crop_start_y
        x2, y2 = event.x, event.y
        x1, x2 = sorted((max(0, x1), min(img.shape[1], x2)))
        y1, y2 = sorted((max(0, y1), min(img.shape[0], y2)))

        if x2 > x1 and y2 > y1:
            img_backup = img.copy()
            img = img[y1:y2, x1:x2]
            display_image(img)
        canvas.delete("crop_rectangle")

def apply_grayscale():
    global img, img_backup
    if img is not None:
        img_backup = img.copy()  # Save the current state
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        display_image(img)

def apply_blur():
    global img, img_backup
    if img is not None:
        img_backup = img.copy()  # Save the current state
        img = cv2.GaussianBlur(img, (15, 15), 0)
        display_image(img)

# Functions for drawing on the image
def start_drawing(event):
    global prev_x, prev_y, draw_mode, img_backup
    if img is not None:
        img_backup = img.copy()  # Backup before drawing
        prev_x, prev_y = event.x, event.y
        draw_mode = True

def draw(event):
    global prev_x, prev_y, img, draw_mode
    if img is not None and draw_mode:
        cv2.line(img, (prev_x, prev_y), (event.x, event.y), (0, 0, 255), 2)  # Red line
        prev_x, prev_y = event.x, event.y
        display_image(img)

def stop_drawing(event):
    global draw_mode
    draw_mode = False

def activate_draw_mode():
    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<ButtonRelease-1>", stop_drawing)
    print("Draw mode activated! Click and drag to draw on the image.")    

def add_text():
    global img, img_backup
    if img is not None:
        img_backup = img.copy()
        text = simpledialog.askstring("Input", "Enter text to add to the image:")
        if text:
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            display_image(img)


def undo():
    global img, img_backup, redo_stack
    if img_backup is not None:
        redo_stack.append(img.copy())  # Save the current state to redo stack
        img = img_backup.copy()
        display_image(img)
    else:
        print("No previous image to undo!")

def redo():
    global img, redo_stack
    if redo_stack:
        img_backup = img.copy()  # Save the current state to backup
        img = redo_stack.pop()
        display_image(img)
    else:
        print("No action to redo!")



# Function to set background color
def set_background_color():
    color = simpledialog.askstring("Input", "Enter a background color (e.g., red, black, purple):")
    if color:
        try:
            canvas.config(bg=color)
            print(f"Background color set to {color}")
        except TclError:
            print(f"Invalid color: {color}. Please enter a valid color name.")

def delete_image():
    global img, img_backup
    img = None
    img_backup = None
    canvas.delete("all")
    print("Image deleted!")


def apply_sepia():
    global img, img_backup
    if img is not None:
        img_backup = img.copy()
        sepia_filter = cv2.transform(img, 
            [[0.272, 0.534, 0.131], 
             [0.349, 0.686, 0.168], 
             [0.393, 0.769, 0.189]])
        img = cv2.convertScaleAbs(sepia_filter)
        display_image(img)

def apply_invert():
    global img, img_backup
    if img is not None:
        img_backup = img.copy()
        img = cv2.bitwise_not(img)
        display_image(img)

def apply_brightness_contrast(brightness=30, contrast=30):
    global img, img_backup
    if img is not None:
        img_backup = img.copy()
        img = cv2.convertScaleAbs(img, alpha=1 + contrast / 100, beta=brightness)
        display_image(img)

def apply_edge_detection():
    global img, img_backup
    if img is not None:
        img_backup = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        display_image(img)

# Initialize global variables
img = None
img_backup = None
img_display = None
draw_mode = False  # Keeps track of the drawing state
redo_stack = []  # Stack for redo functionality

# Create the main window
root = Tk()
root.title("Image Editor")

# Create canvas to display images
canvas = Canvas(root, width=500, height=500,bg="white")
canvas.pack(side=RIGHT)

# Button Functions 
def create_buttons():
    button_frame = Frame(root)
    button_frame.pack(side=LEFT, padx=10, pady=10)

    Button(button_frame, text="Open Image", command=open_image, bg="#4CAF50", fg="white").pack(fill=X, pady=5)
    Button(button_frame, text="Rotate Image", command=rotate_image, bg="#FF5722", fg="white").pack(fill=X, pady=5)
    Button(button_frame, text="Save Image", command=save_image, bg="#4CAF50", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Grayscale", command=apply_grayscale, bg="#2196F3", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Blur", command=apply_blur, bg="#2196F3", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Crop", command=activate_crop_mode, bg="#FF9800", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Add Text", command=add_text, bg="#FF9800", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Undo", command=undo, bg="#F44336", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Redo", command=redo, bg="#F44336", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Set Background", command=set_background_color, bg="#795548", fg="white").pack(fill=X, pady=5)
    Button(button_frame, text="Delete Image", command=delete_image, bg="#E91E63", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Sepia", command=apply_sepia, bg="#9C27B0", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Invert", command=apply_invert, bg="#9C27B0", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Edge Detection", command=apply_edge_detection, bg="#E91E63", fg="white").pack(fill=X, pady=2)
    Button(button_frame, text="Brightness/Contrast", command=lambda: apply_brightness_contrast(30, 30), bg="#FFC107", fg="black").pack(fill=X, pady=2)
    Button(button_frame, text="Draw", command=activate_draw_mode, bg="#795548", fg="white").pack(fill=X, pady=5)

# Call the function to create buttons
create_buttons()

# Start the main event loop
root.mainloop()