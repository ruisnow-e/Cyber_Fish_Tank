"""
drawing_interface.py

This file builds a "draw a fish" window.

For the user:
1. The user can draw a fish with the mouse.
2. The user can choose brush color and size.
3. The user can clear the canvas or undo the last stroke.
4. When the user clicks "submit", the app asks for a fish name and saves the drawing as a PNG image in the "fish_drawings" folder.
5. The saved image has a transparent background, so it can be used nicely in the tank.
"""

import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import ImageGrab
import os  # Used for file paths and folder creation


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
DEFAULT_COLOR = "#000000"
DEFAULT_BRUSH_SIZE = 5

# Global variables
SAVE_COUNTER = 0
LAST_SAVED_IMAGE = None
LAST_SAVED_NAME = None

def get_drawing_image():
    """
    For other modules: return the file path of the last drawn image.
    """
    return LAST_SAVED_IMAGE

def get_drawing_name():
    """
    For other moddules: return the last fish name entered by the user.
    """
    return LAST_SAVED_NAME

class DrawingInterface:
    def __init__(self, root, save_folder="fish_drawings"):
        self.save_folder = save_folder
        os.makedirs(save_folder, exist_ok=True) # make sure the folder for fish drawings exists.
        self.root = root
        self.root.title("Draw a Fish")

        # Current draw state
        self.current_color = DEFAULT_COLOR
        self.brush_size = DEFAULT_BRUSH_SIZE
        self.last_x = None
        self.last_y = None

        # List to store strokes for undo
        self.strokes = []
        self.current_stroke = []

        # Main frame
        main_frame = tk.Frame(root, bg="#f0f4ff")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(main_frame, text="Draw a Fish! (facing right please)",
                               font=("Arial", 20, "bold"), bg="#f0f4ff")
        title_label.pack(pady=10)

        # Toolbar: colors, brush size, buttons
        toolbar = tk.Frame(main_frame, bg="#f0f4ff")
        toolbar.pack(pady=5, fill=tk.X)

        # list of tuples
        colors = [
            ("#000000", "Black"), ("#e74c3c", "Red"), ("#e67e22", "Orange"),
            ("#f1c40f", "Yellow"), ("#2ecc71", "Green"), ("#3498db", "Blue"),
            ("#9b59b6", "Purple"), ("#8e5b2b", "Brown")
        ]

        # clickable color swatches
        for hex_code, name in colors:
            swatch = tk.Label(toolbar, bg=hex_code, width=2, height=1, relief="ridge", bd=2)
            swatch.bind("<Button-1>", lambda e, c=hex_code: self.set_color(c)) # makes sure each button remember its own color.
            swatch.pack(side=tk.LEFT, padx=2)

        # brush size label and slider
        size_label = tk.Label(toolbar, text="Brush size:", bg="#f0f4ff")
        size_label.pack(side=tk.LEFT, padx=(15,5))
        self.size_scale = ttk.Scale(toolbar, from_=1, to=30, orient=tk.HORIZONTAL,
                                    command=self.on_brush_size_change)
        self.size_scale.set(DEFAULT_BRUSH_SIZE)
        self.size_scale.pack(side=tk.LEFT, padx=5)

        # Buttons: clear, undo, submit
        clear_btn = tk.Button(toolbar, text="Clear", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=(20,5))
        undo_btn = tk.Button(toolbar, text="Undo", command=self.undo_last_stroke)
        undo_btn.pack(side=tk.LEFT, padx=5)
        submit_btn = tk.Button(toolbar, text="Submit (Save & Close)", command=self.save_and_close)
        submit_btn.pack(side=tk.LEFT, padx=5)

        # Canvas
        canvas_frame = tk.Frame(main_frame, bg="#cce6ff", padx=10, pady=10)
        canvas_frame.pack(pady=10)
        self.canvas = tk.Canvas(canvas_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                                bg="white", highlightthickness=0)
        self.canvas.pack()

        # Bind mouse and drawing
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def set_color(self, color):
        """change the current brush color."""
        self.current_color = color

    def on_brush_size_change(self, value):
        """change the brush size."""
        self.brush_size = float(value)

    def on_button_press(self, event):
        """ Mouse press on the canvas and a new stroke will start at this point."""
        self.last_x = event.x
        self.last_y = event.y
        self.current_stroke = []

    def on_move_press(self, event):
        """ Mouse moved while button is pressed. Draw a line."""
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            line_id = self.canvas.create_line(
                self.last_x, self.last_y, x, y,
                width=self.brush_size, fill=self.current_color,
                capstyle=tk.ROUND, smooth=True
            )
            self.current_stroke.append(line_id)
        self.last_x = x
        self.last_y = y

    def on_button_release(self, event):
        """Mouse released. Finish the current stroke."""
        self.last_x = None
        self.last_y = None
        if self.current_stroke:
            self.strokes.append(self.current_stroke)
            self.current_stroke = []

    def clear_canvas(self):
        """Clear the canvas and reset undo history."""
        self.canvas.delete("all")
        self.strokes = []

    def undo_last_stroke(self):
        """ undo the last stroke"""
        if not self.strokes:
            return
        last_stroke = self.strokes.pop()
        for line_id in last_stroke:
            self.canvas.delete(line_id)

    # Saving
    def save_canvas(self):
        global SAVE_COUNTER, LAST_SAVED_IMAGE, LAST_SAVED_NAME

        # Ask user for fish name
        fish_name_input = simpledialog.askstring(
            "Fish Name",
            "Please enter a name for your fish:",
            parent=self.root
        )
        if not fish_name_input:
            fish_name_input = f"fish_{SAVE_COUNTER+1}"

        # Make filename safe
        safe_name = "".join([c if c.isalnum() else "_" for c in fish_name_input])
        LAST_SAVED_NAME = fish_name_input

        self.root.update()  # Make sure the drawing is visible

        # canvas position and size
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Capture the canvas
        img = ImageGrab.grab(bbox=(x+1, y+1, x+w-1, y+h-1)).convert("RGBA")
        new_data = [(255,255,255,0) if r>250 and g>250 and b>250 else (r,g,b,a) for r,g,b,a in img.getdata()]
        img.putdata(new_data)

        SAVE_COUNTER += 1
        file_path = os.path.abspath(os.path.join(self.save_folder, f"{safe_name}.png"))
        img.save(file_path, "PNG")
        LAST_SAVED_IMAGE = file_path
        print(f"Saved drawing to {file_path}")

    def save_and_close(self):
        self.save_canvas()
        self.root.destroy()

def main(save_folder="fish_drawings"): # Allows the module to be used for testing and as an imported module
    os.makedirs(save_folder, exist_ok=True)
    root = tk.Tk()
    app = DrawingInterface(root, save_folder)
    root.mainloop()

if __name__ == "__main__":
    main()
