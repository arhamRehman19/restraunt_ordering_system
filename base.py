import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog
import json, os
p

MENU_FILE = "menu.json"


def load_menu():
    if not os.path.exists(MENU_FILE):
        return {"Burger":8.5, "Pizza":12.0, "Pasta":10.0,
                "Fries":4.0, "Soda":2.5, "Ice Cream":3.0}
    with open(MENU_FILE,"r") as f:
        return json.load(f)


def save_menu(menu):
    with open(MENU_FILE,"w") as f:
        json.dump(menu, f, indent=4)


class KitchenWindow(tk.Toplevel):
    def __init__(self, master, order_queue):
        super().__init__(master)
        self.order_queue = order_queue
        self.title("Chef’s Kitchen")


        tk.Label(self, text="Pending Orders", font=("Arial",14,"bold")).pack(pady=10)
        self.listbox = tk.Listbox(self, width=40, height=10, selectmode=tk.MULTIPLE)
        self.listbox.pack(padx=10, pady=5)
        tk.Button(self, text="Order Made", command=self.remove_order).pack(pady=5)
        self.refresh_list()


    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for tbl, items, total in self.order_queue:
            self.listbox.insert(tk.END, f"Table {tbl}: {', '.join(items)} → ${total:.2f}")


    def remove_order(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        for idx in reversed(sel):
            del self.order_queue[idx]
        self.refresh_list()


class RestaurantOrderingSystem:
    def __init__(self, root, menu_data):
        self.root = root
        root.title("Customer Ordering")
        self.menu_data = menu_data
        self.order_queue = []
        self.kitchen = KitchenWindow(root, self.order_queue)


        tk.Label(root, text="Select Your Order", font=("Arial",16,"bold")).pack(pady=10)
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()
        self.build_menu()


        tk.Button(root, text="Submit Order", command=self.submit_order,
                  font=("Arial",12,"bold")).pack(pady=15)
        tk.Button(root, text="Edit Menu", command=self.open_menu_editor,
                  font=("Arial",10)).pack()


    def build_menu(self):
        for w in self.menu_frame.winfo_children():
            w.destroy()
        self.check_vars = {}
        for item, price in self.menu_data.items():
            var = tk.IntVar()
            chk = tk.Checkbutton(self.menu_frame,
                                 text=f"{item} – ${price:.2f}",
                                 variable=var, font=("Arial",12))
            chk.pack(anchor='w')
            self.check_vars[item] = var


    def submit_order(self):
        tbl = simpledialog.askinteger("Table Number",
                                      "Enter your table number:",
                                      parent=self.root, minvalue=1)
        if tbl is None:
            messagebox.showinfo("Cancelled", "No table number entered.")
            return
        selected = {item: price for item, price in self.menu_data.items()
                    if self.check_vars.get(item, tk.IntVar()).get()}
        if not selected:
            messagebox.showwarning("No Selection","Please select at least one item!")
            return
        items = list(selected.keys())
        total = sum(selected.values())
        self.order_queue.append((tbl, items, total))
        messagebox.showinfo("Order Placed", f"Table {tbl} order sent!")
        self.show_order_summary(items, total, tbl)
        self.kitchen.refresh_list()
        self.reset_selection()


    def show_order_summary(self, items, total, tbl):
        win = Toplevel(self.root)
        win.title("Your Order")
        tk.Label(win, text=f"Order Summary (Table {tbl})",
                 font=("Arial",16,"bold")).pack(pady=10)
        for itm in items:
            tk.Label(win, text=f"{itm} – ${self.menu_data[itm]:.2f}",
                     font=("Arial",12)).pack(anchor='w', padx=20)
        tk.Label(win, text=f"\nTotal: ${total:.2f}",
                 font=("Arial",14,"bold")).pack(pady=10)


    def reset_selection(self):
        for var in self.check_vars.values():
            var.set(0)


    def open_menu_editor(self):
        MenuEditor(self)


class MenuEditor:
    def __init__(self, main_app):
        self.main_app = main_app
        self.menu_data = main_app.menu_data
        self.win = Toplevel()
        self.win.title("Edit Menu")
        tk.Label(self.win, text="Menu Items", font=("Arial",14,"bold")).pack(pady=10)
        self.listbox = tk.Listbox(self.win, width=30)
        self.listbox.pack()
        self.update_list()
        tk.Button(self.win, text="Add Item", command=self.add_item).pack(pady=5)
        tk.Button(self.win, text="Remove Selected", command=self.remove_item).pack(pady=5)
        tk.Button(self.win, text="Save and Refresh", command=self.save_refresh).pack(pady=10)


    def update_list(self):
        self.listbox.delete(0,tk.END)
        for i, p in self.menu_data.items():
            self.listbox.insert(tk.END, f"{i} – ${p:.2f}")


    def add_item(self):
        name = simpledialog.askstring("New Item","Enter item name:", parent=self.win)
        if not name:
            return
        try:
            price = float(simpledialog.askstring("Item Price", f"Enter price for {name}:", parent=self.win))
        except (TypeError, ValueError):
            messagebox.showerror("Invalid Input","Please enter a valid number.")
            return
        self.menu_data[name] = price
        self.update_list()


    def remove_item(self):
        sel = self.listbox.curselection()
        if sel:
            name = self.listbox.get(sel[0]).split(" – $")[0]
            del self.menu_data[name]
            self.update_list()


    def save_refresh(self):
        save_menu(self.menu_data)
        self.main_app.build_menu()
        self.win.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    menu = load_menu()
    app = RestaurantOrderingSystem(root, menu)
    root.mainloop()
