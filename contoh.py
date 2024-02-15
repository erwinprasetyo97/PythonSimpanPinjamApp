import tkinter as tk
from tkinter import ttk

Myblue = "#DCF0F2"
Myyellow = "#F2C84B"

def on_treeview_click(event):
    item = treeview.identify_row(event.y)
    column = treeview.identify_column(event.x)
    
    # Change background color when a specific column is clicked
    if column == "#0":  # Replace "#0" with the actual identifier of the desired column
        treeview.tag_configure("clicked", background=Myyellow)
        treeview.item(item, tags=("clicked",))

# Create a Tkinter window
root = tk.Tk()
root.geometry("500x300")

# Create a Treeview widget
treeview = ttk.Treeview(root)
treeview["columns"] = ("Name", "Age", "Gender")

# Configure column headings
treeview.heading("#0", text="ID")
treeview.heading("Name", text="Name")
treeview.heading("Age", text="Age")
treeview.heading("Gender", text="Gender")

# Add sample data to the Treeview
for i in range(1, 11):
    treeview.insert("", "end", values=(f"Item {i}", f"{20 + i}", "Male"))

# Bind the click event to the Treeview
treeview.bind("<ButtonRelease-1>", on_treeview_click)

# Apply style to Treeview
style = ttk.Style()
style.configure("Treeview", background=Myblue)

# Run the Tkinter event loop
root.mainloop()
