import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

# Load and resize image
img = Image.open("Z:\Images")
img = img.resize((100, 100))  # Resize if needed
img_tk = ImageTk.PhotoImage(img)

def on_click():
    print("Image button clicked!")

btn = tk.Button(root, image=img_tk, command=on_click)
btn.pack(pady=20)

# Keep reference to the image to prevent GC
btn.image = img_tk

root.mainloop()
