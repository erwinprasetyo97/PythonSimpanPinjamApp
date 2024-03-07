import tkinter as tk
from tkinter import ttk

# Membuat jendela utama
root = tk.Tk()

# Membuat Treeview dengan kolom
treeview = ttk.Treeview(root, columns=("ID", "Nama", "Puskesmas"), show="headings")

# Menambahkan judul kolom
treeview.heading("ID", text="ID")
treeview.heading("Nama", text="Nama")
treeview.heading("Puskesmas", text="Puskesmas")

# Memasukkan data ke dalam Treeview (ganti ini dengan logika pemasukan data sebenarnya)
treeview.insert("", tk.END, values=("1", "John Doe", "Puskesmas A"))
treeview.insert("", tk.END, values=("2", "Jane Doe", "Puskesmas B"))

# Mempasang Treeview ke dalam jendela
treeview.pack()

# Menjalankan loop utama
root.mainloop()
