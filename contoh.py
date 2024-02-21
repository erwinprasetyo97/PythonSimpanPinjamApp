import tkinter as tk
from tkinter import ttk

def notebook_event(event):
    current_tab = notebook.index(notebook.select())
    if current_tab == 1:
        select_based_loans()
    elif current_tab == 2:
        select_based_credit_risk()
    elif current_tab == 3:
        select_based_profit_sharing()
    elif current_tab == 4:
        select_based_pokok()

root = tk.Tk()
root.title("Aplikasi Simpan Pinjam")
root.geometry("1060x650")
root.resizable(False, False)

# Baris pertama: Notebook untuk menampilkan data
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

# ... (frame1, frame2, frame3, frame4, frame5)

# Add Frames to notebook display data
notebook.add(frame1, text='Semua')
notebook.add(frame2, text='Per Jumlah Pinjaman')
notebook.add(frame3, text='Per Resiko Kredit')
notebook.add(frame4, text='Per Bagi Hasil')
notebook.add(frame5, text='Per Sisa Pokok')

notebook.bind("<<NotebookTabChanged>>", lambda event: notebook_event(event))

# Baris kedua: Notebook untuk pencarian
search_notebook = ttk.Notebook(root)
search_notebook.grid(row=1, column=0, sticky="nsew")

search_frame1 = ttk.Frame(search_notebook, width=400, height=280)
search_frame2 = ttk.Frame(search_notebook, width=400, height=280)
# ... (tambahkan frame pencarian lainnya)

search_notebook.add(search_frame1, text='Pencarian 1')
search_notebook.add(search_frame2, text='Pencarian 2')
# ... (tambahkan tab pencarian lainnya)

# Baris ketiga: Notebook untuk inputan
input_notebook = ttk.Notebook(root)
input_notebook.grid(row=2, column=0, sticky="nsew")

input_frame1 = ttk.Frame(input_notebook, width=400, height=280)
input_frame2 = ttk.Frame(input_notebook, width=400, height=280)
# ... (tambahkan frame input lainnya)

input_notebook.add(input_frame1, text='Input Data Peminjam')
input_notebook.add(input_frame2, text='Input Data Setoran')
# ... (tambahkan tab input lainnya)

# ...

root.mainloop()
