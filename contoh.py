import tkinter as tk
from tkinter import ttk

def submit():
    # Fungsi ini dapat digunakan untuk mengambil nilai dari setiap input dan melakukan sesuatu dengannya
    nama = entry_nama.get()
    nip = entry_nip.get()
    puskesmas = entry_puskesmas.get()
    alamat_rumah = entry_alamat_rumah.get()
    tanggal_lahir = entry_tanggal_lahir.get()
    jumlah_pinjaman = entry_jumlah_pinjaman.get()
    jangka_waktu = entry_jangka_waktu.get()

    # Contoh: Menampilkan data yang diambil
    print("Nama:", nama)
    print("NIP:", nip)
    print("Puskesmas:", puskesmas)
    print("Alamat Rumah:", alamat_rumah)
    print("Tanggal Lahir:", tanggal_lahir)
    print("Jumlah Pinjaman:", jumlah_pinjaman)
    print("Jangka Waktu:", jangka_waktu)

# Membuat window
window = tk.Tk()
window.title("Form Peminjaman")

# Membuat ttk.Notebook
notebook = ttk.Notebook(window)

# Membuat frame untuk setiap tab
frame_tab1 = ttk.Frame(notebook)
frame_tab2 = ttk.Frame(notebook)

# Menambahkan tab ke notebook
notebook.add(frame_tab1, text='Tab 1')
notebook.add(frame_tab2, text='Tab 2')

# Membuat label dan input untuk setiap data di setiap tab
label_nama = ttk.Label(frame_tab1, text="Nama:")
entry_nama = ttk.Entry(frame_tab1)

label_nip = ttk.Label(frame_tab1, text="NIP:")
entry_nip = ttk.Entry(frame_tab1)

# ... (lanjutkan untuk elemen lainnya)

# Menempatkan label dan input ke dalam grid di setiap tab
label_nama.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

label_nip.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_nip.grid(row=1, column=1, padx=5, pady=5)

# ... (lanjutkan untuk elemen lainnya)

# Membuat tombol submit di setiap tab
button_submit_tab1 = ttk.Button(frame_tab1, text="Submit", command=submit)
button_submit_tab2 = ttk.Button(frame_tab2, text="Submit", command=submit)

# Menempatkan tombol submit di setiap tab
button_submit_tab1.grid(row=7, column=0, columnspan=2, pady=10)
button_submit_tab2.grid(row=7, column=0, columnspan=2, pady=10)

# Menjalankan aplikasi
notebook.pack(expand=1, fill="both")
window.mainloop()
