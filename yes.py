import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# --- Globals ---
order_list = []

def create_home_content(parent, switch_to_tab_callback, upload_image_callback):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text="Welcome to the Home Page!")
    label.pack(pady=20)

    upload_btn = ttk.Button(frame, text="Upload Image", command=upload_image_callback)
    upload_btn.pack(pady=10)

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=10)

    btn1 = ttk.Button(btn_frame, text="Go to Tab 1", command=lambda: switch_to_tab_callback(1))
    btn1.pack(side='left', padx=5)

    btn2 = ttk.Button(btn_frame, text="Go to Tab 2", command=lambda: switch_to_tab_callback(2))
    btn2.pack(side='left', padx=5)

    btn3 = ttk.Button(btn_frame, text="Go to Tab 3", command=lambda: switch_to_tab_callback(3))
    btn3.pack(side='left', padx=5)

    return frame

def create_tab1_content(parent, go_home_callback):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text="Content for Tab 1")
    label.pack(pady=20)
    btn_home = ttk.Button(frame, text="Go Home", command=go_home_callback)
    btn_home.pack(pady=10)
    return frame

def create_tab2_content(parent, go_home_callback):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text="Select items to add to your order:")
    label.pack(pady=10)

    items = ["Apple", "Banana", "Carrot", "Doughnut", "Eggplant"]

    def add_to_order(item):
        order_list.append(item)
        update_order_listbox()
        print(f"Added {item} to order.")

    # List items with buttons
    for item in items:
        item_frame = ttk.Frame(frame)
        item_frame.pack(fill='x', pady=2, padx=10)

        item_label = ttk.Label(item_frame, text=item)
        item_label.pack(side='left')

        add_btn = ttk.Button(item_frame, text="Add to Order", command=lambda i=item: add_to_order(i))
        add_btn.pack(side='right')

    btn_home = ttk.Button(frame, text="Go Home", command=go_home_callback)
    btn_home.pack(pady=10)

    return frame

def create_tab3_content(parent, go_home_callback):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text="Your Order:")
    label.pack(pady=10)

    global order_listbox
    order_listbox = tk.Listbox(frame, height=10)
    order_listbox.pack(padx=10, pady=5, fill='x')

    def remove_selected():
        selected = order_listbox.curselection()
        if selected:
            index = selected[0]
            removed_item = order_list.pop(index)
            update_order_listbox()
            print(f"Removed {removed_item} from order.")

    remove_btn = ttk.Button(frame, text="Remove Selected Item", command=remove_selected)
    remove_btn.pack(pady=5)

    btn_home = ttk.Button(frame, text="Go Home", command=go_home_callback)
    btn_home.pack(pady=10)

    return frame

def update_order_listbox():
    if order_listbox:
        order_listbox.delete(0, tk.END)
        for item in order_list:
            order_listbox.insert(tk.END, item)

def switch_to_tab(tab_index):
    notebook.select(tab_index)

def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if file_path:
        load_and_show_image(file_path)

def load_and_show_image(path):
    img = Image.open(path)
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    global image_label, loaded_image
    loaded_image = img_tk
    if not hasattr(tab1_content, "image_label"):
        tab1_content.image_label = ttk.Label(tab1_content)
        tab1_content.image_label.pack(pady=10)
    tab1_content.image_label.config(image=img_tk)
    switch_to_tab(1)

# --- Main Window Setup ---

root = tk.Tk()
root.title("Button-Driven Tabs with Image Upload and Ordering")

style = ttk.Style()
style.layout("TNotebook.Tab", [])  # Hide the tabs

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create tabs
home_content = create_home_content(
    parent=notebook,
    switch_to_tab_callback=switch_to_tab,
    upload_image_callback=upload_image
)
notebook.add(home_content, text="Home")

tab1_content = create_tab1_content(notebook, go_home_callback=lambda: switch_to_tab(0))
notebook.add(tab1_content, text="Tab 1")

tab2_content = create_tab2_content(notebook, go_home_callback=lambda: switch_to_tab(0))
notebook.add(tab2_content, text="Tab 2")

tab3_content = create_tab3_content(notebook, go_home_callback=lambda: switch_to_tab(0))
notebook.add(tab3_content, text="Tab 3")

# Global references
order_listbox = None
image_label = None
loaded_image = None

root.mainloop()
