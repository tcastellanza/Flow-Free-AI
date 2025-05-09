from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

import cv2
from FlowFreePuzzleSolver import FlowFreeSolver
from test import ColorGridDetector

import io
import sys

root = TkinterDnD.Tk()
root.title("Flow Free Puzzle Solver")
root.geometry("800x500")

# Main layout
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True)

# Left: Image and buttons
image_frame = Frame(main_frame)
image_frame.pack(side=LEFT, padx=20, fill=Y)

image_label = Label(image_frame)
image_label.pack()

drop_label = Label(image_frame, text="Drag and drop an image file here", relief="ridge", width=40, height=10)
drop_label.pack(pady=30)

# Right: Centered text output
text_frame = Frame(main_frame)
text_frame.pack(side=RIGHT, fill=Y, expand=True)

# Use pack() instead of place() for better layout handling
text_inner_frame = Frame(text_frame)
text_inner_frame.pack(expand=True)

text_box = Text(
    text_inner_frame,
    width=25,
    height=10,
    font=("Courier", 15),
    state=DISABLED,
)


# Buttons
stop_button = None
back_button = None
dropped_image_path = None

def drop(event):
    global stop_button, back_button, dropped_image_path
    filepath = event.data.strip('{}')

    try:
        image = Image.open(filepath)
        image.thumbnail((400, 300))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

        drop_label.pack_forget()
        dropped_image_path = filepath

        if not stop_button:
            stop_button = Button(image_frame, text='Process Puzzle', width=25, command=process_image)
            stop_button.pack(pady=5)

        if not back_button:
            back_button = Button(image_frame, text='Back', width=25, command=reset_ui)
            back_button.pack(pady=5)

    except Exception as e:
        image_label.config(text=f"Error: {e}")

def process_image():
    if not dropped_image_path:
        print("❌ No image path available!")
        return

    print(f"📷 Processing: {dropped_image_path}")

    detector = ColorGridDetector(grid_size=(5, 5))
    color_positions = detector.detect_colors(dropped_image_path)

    solver = FlowFreeSolver(5, color_positions)

    output = io.StringIO()
    sys.stdout = output  # Redirect print

    if solver.solve():
        print("✅ Solution found:")
        solver.print_grid()
    else:
        print("❌ No solution found.")

    sys.stdout = sys.__stdout__  # Restore

    text_box.config(state=NORMAL)
    text_box.delete("1.0", END)
    text_box.insert(END, output.getvalue())
    text_box.config(state=DISABLED)
    # Show the text box if it's not already packed
    if not text_box.winfo_ismapped():
        text_box.pack(pady=20)

def reset_ui():
    global stop_button, back_button, dropped_image_path

    image_label.config(image='', text='')
    image_label.image = None
    dropped_image_path = None

    text_box.config(state=NORMAL)
    text_box.delete("1.0", END)
    text_box.config(state=DISABLED)

    if stop_button:
        stop_button.destroy()
        stop_button = None
    if back_button:
        back_button.destroy()
        back_button = None

    drop_label.pack(pady=30)

# Bind drag-and-drop
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind('<<Drop>>', drop)

root.mainloop()