import tkinter as tk
from tkinter import ttk

def create_home_content(parent, switch_to_tab_callback):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text="Welcome to the Home Page!")
    label.pack(pady=20)

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

root = tk.Tk()
root.title("Button-Driven Tabs")

style = ttk.Style()
style.layout("TNotebook.Tab", [])  # Hide the tabs

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

def switch_to_tab(tab_index):
    notebook.select(tab_index)

# Home tab (index 0) with navigation buttons
home_content = create_home_content(notebook, switch_to_tab)
notebook.add(home_content, text="Home")

# Other tabs with "Go Home" buttons
tab1_content = create_tab_content(notebook, "Tab 1", lambda: switch_to_tab(0))
notebook.add(tab1_content, text="Tab 1")

tab2_content = create_tab_content(notebook, "Tab 2", lambda: switch_to_tab(0))
notebook.add(tab2_content, text="Tab 2")

tab3_content = create_tab_content(notebook, "Tab 3", lambda: switch_to_tab(0))
notebook.add(tab3_content, text="Tab 3")

root.mainloop()
