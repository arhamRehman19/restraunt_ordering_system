import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk  # You need Pillow installed

def create_home_content(parent, switch_to_tab_callback, upload_image_callback):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text="Welcome to the Home Page!")
    label.pack(pady=20)

    # Upload image button
    upload_btn = ttk.Button(frame, text="Upload Image", command=upload_image_callback)
    upload_btn.pack(pady=10)

    # Navigation buttons inside Home tab
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=10)

    btn1 = ttk.Button(btn_frame, text="Go to Tab 1", command=lambda: switch_to_tab_callback(1))
    btn1.pack(side='left', padx=5)

    btn2 = ttk.Button(btn_frame, text="Go to Tab 2", command=lambda: switch_to_tab_callback(2))
    btn2.pack(side='left', padx=5)

    btn3 = ttk.Button(btn_frame, text="Go to Tab 3", command=lambda: switch_to_tab_callback(3))
    btn3.pack(side='left', padx=5)

    return frame

def create_tab_content(parent, tab_name, go_home_callback):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text=f"Content for {tab_name}")
    label.pack(pady=20)
    btn_home = ttk.Button(frame, text="Go Home", command=go_home_callback)
    btn_home.pack(pady=10)
    return frame

def switch_to_tab(tab_index):
    notebook.select(tab_index)

def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if file_path:
        # Load and display the image on Tab 1
        load_and_show_image(file_path)

def load_and_show_image(path):
    # Open the image using PIL
    img = Image.open(path)
    img.thumbnail((400, 400))  # Resize to fit nicely
    
    # Convert to ImageTk for tkinter
    img_tk = ImageTk.PhotoImage(img)
    
    # If there's already an image label, update it, else create it
    global image_label, loaded_image
    loaded_image = img_tk  # Keep a reference to avoid garbage collection
    
    if not hasattr(tab1_content, "image_label"):
        tab1_content.image_label = ttk.Label(tab1_content)
        tab1_content.image_label.pack(pady=10)
    tab1_content.image_label.config(image=img_tk)
    
    # Automatically switch to Tab 1 to show the image
    switch_to_tab(1)

# --- Main Window Setup ---

root = tk.Tk()
root.title("Button-Driven Tabs with Image Upload")

style = ttk.Style()
style.layout("TNotebook.Tab", [])  # Hide the tabs

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Home tab (index 0) with upload button and navigation
home_content = create_home_content(
    notebook,
    switch_to_tab_callback=switch_to_tab,
    upload_image_callback=upload_image
)
notebook.add(home_content, text="Home")

# Other tabs
tab1_content = create_tab_content(notebook, "Tab 1", lambda: switch_to_tab(0))
notebook.add(tab1_content, text="Tab 1")

tab2_content = create_tab_content(notebook, "Tab 2", lambda: switch_to_tab(0))
notebook.add(tab2_content, text="Tab 2")

tab3_content = create_tab_content(notebook, "Tab 3", lambda: switch_to_tab(0))
notebook.add(tab3_content, text="Tab 3")

root.mainloop()
