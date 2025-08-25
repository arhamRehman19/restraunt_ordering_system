import tkinter as tk
from tkinter import ttk

def create_tab_content(parent, tab_name):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text=f"Content for {tab_name}")
    label.pack(pady=20)
    return frame

root = tk.Tk()
root.title("Button-Driven Tabs")

style = ttk.Style()
style.layout("TNotebook.Tab", [])  # This removes the tab from the notebook

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create tabs and add content
tab1_content = create_tab_content(notebook, "Tab 1")
notebook.add(tab1_content)

tab2_content = create_tab_content(notebook, "Tab 2")
notebook.add(tab2_content)

tab3_content = create_tab_content(notebook, "Tab 3")
notebook.add(tab3_content)

# You can also use separate buttons to switch tabs programmatically
def switch_to_tab(tab_index):
    notebook.select(tab_index)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

btn1 = ttk.Button(button_frame, text="Show Tab 1", command=lambda: switch_to_tab(0))
btn1.pack(side='left', padx=5)

btn2 = ttk.Button(button_frame, text="Show Tab 2", command=lambda: switch_to_tab(1))
btn2.pack(side='left', padx=5)

btn3 = ttk.Button(button_frame, text="Show Tab 3", command=lambda: switch_to_tab(2))
btn3.pack(side='left', padx=5)

root.mainloop()