import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

def handle_paste(event):
    # Get the clipboard data
    clipboard_data = root.clipboard_get()

    # Check if the clipboard data is an image
    if clipboard_data and clipboard_data.startswith("P6\n") and b"\n255\n" in clipboard_data:
        # Save the clipboard data as an image file
        with open("pasted_image.ppm", "wb") as f:
            f.write(clipboard_data.encode())


def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Open the selected image file and display it on the canvas
        image = Image.open(file_path)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(event.x, event.y, image=photo)
        canvas.image = photo


root = tk.Tk()
root.title("Whiteboard")

canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Bind the paste event to the handle_paste function
root.bind("<Control-v>", handle_paste)
canvas.bind("<Button-1>", open_file)

root.mainloop()
