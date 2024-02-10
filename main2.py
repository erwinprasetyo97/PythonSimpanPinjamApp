from tkinter import *
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from datetime import datetime
import pandas as pd
from tkinter import filedialog
from datetime import datetime, timezone


root = Tk()

conn = sqlite3.connect("pinjamanpuskesmas.db")
cursor = conn.cursor()

# Create a notebook
notebook = ttk.Notebook(root)
notebook.pack(fill="both", padx=20, pady=10)


def create_table():
    # Menonaktifkan pengecekan kunci asing
    cursor.execute("PRAGMA foreign_keys=off")
    cursor.execute("PRAGMA timezone = 'Asia/Jakarta'")
    cursor.execute("DROP TABLE IF EXISTS LOANS")
    query = """
    CREATE TABLE LOANS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAMA TEXT NOT NULL,
        NIP INTEGER NOT NULL,
        PUSKESMAS TEXT NOT NULL,
        TANGGAL_LAHIR TEXT NOT NULL,
        ALAMAT TEXT NOT NULL,
        JUMLAH_PINJAMAN INTEGER NOT NULL,
        JANGKA_WAKTU INTEGER NOT NULL,
        RESIKO_KREDIT INT,
        BAGI_HASIL INT,
        POKOK INT,
        TERIMA_BERSIH INT,
        TIMESTAMP TIMESTAMP DEFAULT (datetime('now', 'localtime'))
    )
    """
    cursor.execute(query)
    cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("PRAGMA timezone = DEFAULT")
    conn.commit()


def isFirst(table_name):
    query = '''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}' '''.format(
        table_name)
    cursor.execute(query)
    conn.commit()
    if cursor.fetchone()[0] == 1:
        return False
    else:
        return True


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return FALSE


# query for display all data
def select_all():
    query = "SELECT ID, NAMA, NIP, PUSKESMAS, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH FROM LOANS"
    cursor.execute(query)
    rows = cursor.fetchall()
    update_trv(rows)


# query for display data based "jumlah_pinjaman"
def select_based_loans(event=None):
    try:
        # Menentukan kolom yang ingin ditampilkan
        columns_to_select = ['ID', 'NAMA', 'PUSKESMAS', 'TIMESTAMP', 'JUMLAH_PINJAMAN']

        # Membuat pernyataan SQL SELECT
        query = f"SELECT {', '.join(columns_to_select)} FROM LOANS;"
        cursor.execute(query)
        rows = cursor.fetchall()

        update_trv2(rows)
    except Exception as e:
        print("Error fetching data:", e)

# query for display data based "Resiko Kredit"
def select_based_credit_risk(event=None):
    try :
        # Menentukan kolom yang ingin ditampilkan
        columns_to_select = ['ID', 'NAMA', 'PUSKESMAS', 'RESIKO_KREDIT']

        # Membuat pernyataan SQL SELECT
        query = f"SELECT {', '.join(columns_to_select)} FROM LOANS;"
        cursor.execute(query)
        rows = cursor.fetchall()

        # print("Data Credit Risk : ", rows)
        update_trv3(rows)
    
    except Exception as e:
        print("Error fetching data:", e)


# function untuk update treeview pada semua data
def update_trv(rows):
    trv.delete(*trv.get_children())
    for idx, i in enumerate(rows, start=1):
        trv.insert('', 'end', values=(i[0], idx, *i[1:]))

# function untuk update treeview pada 
def update_trv2(data):
    # Membersihkan isi treeviw sebelum memasukkan data baru
    for row in trv2.get_children():
        trv2.delete(row)

    # Memasukkan data baru ke dalam treeview
    for i, row in enumerate(data, start=1):
        trv2.insert("", "end", values=[i] + list(row))

# function untuk update treeview pada 
def update_trv3(data):
    # Membersihkan isi treeviw sebelum memasukkan data baru
    for row in trv3.get_children():
        trv3.delete(row)

    # Memasukkan data baru ke dalam treeview
    for row in data:
        trv3.insert("", "end", values=row)

def add_new():
    try:
        # Ambil nilai dari setiap field
        nama_value = v_nama.get()
        nip_value = v_nip.get()
        puskesmas_value = v_puskesmas.get()
        tanggal_lahir_value = v_tanggal_lahir.get()
        alamat_value = v_alamat_rumah.get()
        jumlah_pinjaman_value = v_jumlah_pinjaman.get()
        jangka_waktu_value = v_jangka_waktu.get()
        resiko_kredit_value = 1.5/100 * jumlah_pinjaman_value
        bagi_hasil_value = 0.01 * jumlah_pinjaman_value
        pokok_value = jumlah_pinjaman_value / jangka_waktu_value

        if not nama_value or not nip_value or not tanggal_lahir_value or not jumlah_pinjaman_value or not jangka_waktu_value:
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        if not str(jumlah_pinjaman_value or not nip_value or not jangka_waktu_value).isdecimal():
            messagebox.showerror(
                "Error", "Jumlah pinjaman harus berupa bilangan bulat positif")
            return

        if (jangka_waktu_value > 48):
            messagebox.showerror(
                "Error", "Jangka Waktu tidak boleh dari 48 Bulan")
            return

        # Memanggil fungsi validasi tanggal lahir
        if not is_valid_date(tanggal_lahir_value):
            messagebox.showerror(
                "Kesalahan", "Format tanggal lahir tidak valid")
            return

        confirm = messagebox.askquestion(
            "Konfirmasi", "Apakah data sudah benar ?")

        if confirm == 'yes':
            # Jika user menekan Yes, Simpan data ke database
            query = """
                INSERT INTO LOANS
                (NAMA, NIP, PUSKESMAS, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH, TIMESTAMP)
                values (:NAMA, :NIP, :PUSKESMAS, :TANGGAL_LAHIR, :ALAMAT, :JUMLAH_PINJAMAN, :JANGKA_WAKTU, :RESIKO_KREDIT, :BAGI_HASIL, :POKOK, :TERIMA_BERSIH, CURRENT_TIMESTAMP)
                """
            params = {
                "NAMA": nama_value,
                "NIP": nip_value,
                "PUSKESMAS": puskesmas_value,
                "ALAMAT": alamat_value,
                "TANGGAL_LAHIR": tanggal_lahir_value,
                "JUMLAH_PINJAMAN": jumlah_pinjaman_value,
                "JANGKA_WAKTU": jangka_waktu_value,
                "RESIKO_KREDIT": resiko_kredit_value,
                "BAGI_HASIL": bagi_hasil_value,
                "POKOK": round(pokok_value / 100) * 100,
                "TERIMA_BERSIH": jumlah_pinjaman_value - resiko_kredit_value
            }
            cursor.execute(query, params)
            conn.commit()
            messagebox.showinfo("Info", "Data Berhasil ditambahkan !")
            print("Data added Succesfully.")
            select_all()
            select_based_loans()
            select_based_credit_risk()
            clear_field()

    except Exception as e:
        print("Error :", e)
        messagebox.showerror(
            "Error", "Pastikan format data yang diupdate sudah benar")


def update_data():
    try:
        if messagebox.askyesno("Harap konfirmasi", "Apakah anda yakin ingin memperbarui data ini ?"):
            # validasi format tanggal lahir
            if not is_valid_date(v_tanggal_lahir.get()):
                messagebox.showerror(
                    "Kesalahan", "Format tanggal lahir tidak valid.")
                return

            jumlah_pinjaman_value = v_jumlah_pinjaman.get()
            nip_value = v_nip.get()
            jangka_waktu_value = v_jangka_waktu.get()

            if not str(jumlah_pinjaman_value or not nip_value or not jangka_waktu_value).isdecimal():
                messagebox.showerror(
                    "Error", "Jumlah pinjaman harus berupa bilangan bulat positif")
                return

            if (jangka_waktu_value > 48):
                messagebox.showerror(
                    "Error", "Jangka Waktu tidak boleh dari 48 Bulan")
                return

            query = """ 
                UPDATE LOANS
                SET NAMA=?, NIP=?, PUSKESMAS=?, ALAMAT=?, TANGGAL_LAHIR=?, JUMLAH_PINJAMAN=?, JANGKA_WAKTU=?, URAIAN=? WHERE ID=?
            """
            params = (
                v_nama.get(),
                v_nip.get(),
                v_puskesmas.get(),
                v_alamat_rumah.get(),
                v_tanggal_lahir.get(),
                v_jumlah_pinjaman.get(),
                v_jangka_waktu.get(),
                v_uraian.get(),
                v_id.get()
            )
            cursor.execute(query, params)
            conn.commit()
            clear_field()
            select_all()
            select_based_loans()
            select_based_credit_risk()

            # show success message
            messagebox.showinfo("Info", "Data berhasil diperbarui.")
        else:
            return True
    except Exception as e:
        print("Error", e)
        messagebox.showerror(
            "Error", "Pastikan format data yang diupdate sudah benar")


def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(rowid)

    if 'values' in item and len(item['values']) >= 13:
        v_id.set(item['values'][0])
        v_nama.set(item['values'][2])
        v_nip.set(item['values'][3])
        v_puskesmas.set(item['values'][4])
        v_tanggal_lahir.set(item['values'][5])
        v_alamat_rumah.set(item['values'][6])
        v_jumlah_pinjaman.set(item['values'][7])
        v_jangka_waktu.set(item['values'][8])
    else:
        print("Error: Insufficient values in the 'values atribute.")


def clear_field():
    entry_nama.delete(0, 'end')
    entry_nip.delete(0, 'end')
    entry_puskesmas.delete(0, 'end')
    dob_entry.delete(0, 'end')
    address_entry.delete(0, 'end')
    jumlahpinjaman_entry.delete(0, 'end')
    jangkawaktu_entry.delete(0, 'end')


def delete_data():
    try:
        id = v_id.get()
        if (messagebox.askyesno("Konfirmasi Hapus?", "Apakah yakin ingin menghapus data ini ?")):
            query = "DELETE FROM LOANS WHERE ID = {}".format(id)
            cursor.execute(query)
            conn.commit()
            print("Success delete data")
            clear_field()
            select_all()
            select_based_loans()
            select_based_credit_risk()
        else:
            return True
    except Exception as e:
        print("Error :", e)


# untuk export data to excel
def export_data():
    try:
        # Menampilkan dialog untuk memilih lokasi penyimpanan file Excel
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if file_path:
            # Mengambil data dari database
            query = "SELECT * FROM LOANS"
            cursor.execute(query)
            rows = cursor.fetchall()

        # Membuat DataFrame dari data
        df = pd.DataFrame(rows, columns=[
            'ID', 'NAMA', 'NIP', 'PUSKESMAS', 'TANGGAL_LAHIR', 'ALAMAT', 'JUMLAH_PINJAMAN', 'JANGKA_WAKTU', 'RESIKO_KREDIT', 'BAGI_HASIL', 'POKOK', 'TERIMA_BERSIH', 'URAIAN'
        ])

        # Menyimpan DataFrame ke file Excel
        df.to_excel(file_path, index=False)

        # Menampilkan pesan sukses
        messagebox.showinfo("Info", f"Data berhasil diekspor ke {file_path}")
    except Exception as e:
        print("Error :", e)
        messagebox.showerror(
            "Error", "Terjadi kesalahan saat mengekspor data.")


def search():
    q2 = q.get()
    query = """
    SELECT ID, NAMA, NIP, PUSKESMAS, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH FROM LOANS WHERE NAMA LIKE {} OR NIP LIKE {}
    """.format("'%"+q2+"%'", "'%"+q2+"%'")
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    update_trv(rows)
    update_trv2(rows)
    update_trv3(rows)


def clear():
    ent.delete(0, 'end')
    clear_field()
    select_all()
    select_based_loans()
    select_based_credit_risk()

# untuk mengecek notebook yang aktif
def notebook_event(event):
    current_tab = notebook.index(notebook.select())
    if current_tab == 1:
        select_based_loans()
    elif current_tab == 2:
        select_based_credit_risk()


# Wrapper
wrapperPencarian = LabelFrame(root, text="Pencarian")
wrapperDataPeminjam = LabelFrame(root, text="Data Peminjam")

# For tab (notebook)
frame1 = ttk.Frame(notebook, width=400, height=280)
frame2 = ttk.Frame(notebook, width=400, height=280)
frame3 = ttk.Frame(notebook, width=400, height=280)
frame4 = ttk.Frame(notebook, width=400, height=280)
frame5 = ttk.Frame(notebook, width=400, height=280)

frame1.grid(row=0, column=0, sticky="nsew")  # Use grid instead of pack
frame2.grid(row=0, column=0, sticky="nsew")
frame3.grid(row=0, column=0, sticky="nsew")
frame4.grid(row=0, column=0, sticky="nsew")
frame5.grid(row=0, column=0, sticky="nsew")

# Add Frames to notebook
notebook.add(frame1, text='Semua')
notebook.add(frame2, text='Per Jumlah Pinjaman')
notebook.add(frame3, text='Per Resiko Kredit')
notebook.add(frame4, text='Per Bagi Hasil')
notebook.add(frame5, text='Per Sisa Pokok')

notebook.bind("<<NotebookTabChanged>>", lambda event: notebook_event(event))
# Posisi Wrapper
wrapperPencarian.pack(fill="both", padx=20, pady=10)
wrapperDataPeminjam.pack(fill="both", padx=20, pady=10)

# Form variable
v_id = IntVar()
v_nama = StringVar()
v_nip = IntVar()
v_puskesmas = StringVar()
v_tanggal_lahir = StringVar()
v_alamat_rumah = StringVar()
v_jumlah_pinjaman = IntVar()
v_jangka_waktu = IntVar()
v_uraian = StringVar()

# Frame untuk Form di Wrapper 3
form_frame = ttk.Frame(wrapperDataPeminjam, padding="5")
form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label dan Entry untuk Nama
label_nama = ttk.Label(form_frame, text="Nama")
label_nama.grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nama = ttk.Entry(form_frame, textvariable=v_nama)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

# Label dan Entry untuk NIP
label_nip = ttk.Label(form_frame, text="NIP")
label_nip.grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_nip = ttk.Entry(form_frame, textvariable=v_nip)
entry_nip.grid(row=1, column=1, padx=5, pady=5)

# Label dan Entry untuk Puskesmas
label_puskesmas = ttk.Label(form_frame, text="Puskesmas")
label_puskesmas.grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_puskesmas = ttk.Entry(form_frame, textvariable=v_puskesmas)
entry_puskesmas.grid(row=2, column=1, padx=5, pady=5)

# Label dan Entry untuk alamat Rumah
label_address = ttk.Label(form_frame, text="Alamat Rumah")
label_address.grid(row=3, column=0, sticky="w", padx=5, pady=5)
address_entry = ttk.Entry(form_frame, textvariable=v_alamat_rumah)
address_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

# Label dan Entry untuk Tanggal Lahir
dob_label = ttk.Label(form_frame, text="Tanggal Lahir")
dob_label.grid(row=0, column=2, sticky="w", padx=5, pady=5)
dob_entry = DateEntry(form_frame, selectmode='day',
                      textvariable=v_tanggal_lahir, date_pattern="dd/mm/y")
dob_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
dob_entry.insert(0, "dd/mm/yyyy")


# Label dan Entry untuk Jumlah pinjaman
label_jumlahpinjaman = ttk.Label(form_frame, text="Jumlah Pinjaman")
label_jumlahpinjaman.grid(row=1, column=2, sticky="w", padx=5, pady=5)
jumlahpinjaman_entry = ttk.Entry(form_frame, textvariable=v_jumlah_pinjaman)
jumlahpinjaman_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)

# Label dan Entry untuk Jangka waktu
label_jangkawaktu = ttk.Label(form_frame, text="Jangka Waktu (bulan)")
label_jangkawaktu.grid(row=2, column=2, sticky="w", padx=5, pady=5)
jangkawaktu_entry = ttk.Entry(form_frame, textvariable=v_jangka_waktu)
jangkawaktu_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)


# Frame button add, update, delete
frame_btn = Frame(wrapperDataPeminjam)
update_btn = Button(frame_btn, text="Update", command=update_data)
add_btn = Button(frame_btn, text="Tambah Data", command=add_new)
delete_btn = Button(frame_btn, text="Hapus", command=delete_data)
export_btn = Button(frame_btn, text="Export ke Excel", command=export_data)

frame_btn.grid(row=4, column=0, columnspan=5, sticky="w", pady=10)
add_btn.pack(side=LEFT, padx=5)
update_btn.pack(side=LEFT, padx=5)
delete_btn.pack(side=LEFT, padx=5)
export_btn.pack(side=LEFT, padx=5)

# Wrapper 2 - Pencarian
q = StringVar()
lbl = Label(wrapperPencarian, text="Search")
lbl.pack(side=LEFT, padx=10, pady=15)
ent = Entry(wrapperPencarian, textvariable=q)
ent.pack(side=LEFT, padx=6, pady=15)
btn = Button(wrapperPencarian, text="Search", command=search)
btn.pack(side=LEFT, padx=6, pady=15)
cbtn = Button(wrapperPencarian, text="Clear", command=clear)
cbtn.pack(side=LEFT, padx=6)

# Function untuk create treeview
def create_treview(frame, columns, headers, widths, bind_function=None):
    trv = ttk.Treeview(frame, column=columns, show="headings", height=12)

    style = ttk.Style()
    style.theme_use("clam")

    trv.grid(row=0, column=0, sticky="nsew")
    # trv.pack(side=RIGHT, fill=BOTH, expand=True)
    # trv.pack(side=RIGHT)
    # trv.place(x=0, y=0)

    for i, header in enumerate(headers):
        trv.heading(columns[i], text=header)

    for i, width in enumerate(widths):
        trv.column(columns[i], width=width, minwidth=width, anchor=CENTER)
    
    if bind_function:
        trv.bind('<Double 1>', bind_function)

    # Exclude the first column from being displayed
    trv["displaycolumns"] = columns[1:]

    scrollbar_y = Scrollbar(frame, orient="vertical", command=trv.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    trv.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = Scrollbar(frame, orient="horizontal", command=trv.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    trv.configure(xscrollcommand=scrollbar_x.set)

    return trv

# penerapan untuk tampilkan data semua
columns_trv = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
headers_trv = ("Id", "No", "Nama", "NIP", "Puskesmas", "Tanggal Lahir", "Alamat Rumah", "Jumlah Pinjaman", "Jangka Waktu", "Resiko Kredit", "Bagi Hasil", "Pokok", "Terima Bersih")
widths_trv = (0, 70, 120, 120, 120, 100, 120, 100, 120, 120, 100, 100)

trv = create_treview(frame1, columns_trv, headers_trv, widths_trv, bind_function=getrow)

# penerapan untuk tampilkan data per Jumlah Pinjaman
column_trv2 = (0, 1, 2, 3, 4, 5)
headers_trv2 = ("Id", "No", "Nama", "Puskesmas", "Tanggal Realisasi", "Jumlah Pinjaman")
widths_trv2 = (0, 70, 120, 120, 120, 120)

trv2 = create_treview(frame2, column_trv2, headers_trv2, widths_trv2, bind_function=getrow)


# Frame 3 - Tampilkan per resiko kredit
trv3 = ttk.Treeview(frame3, column=(0, 1, 2, 3), show="headings", height=12)

trv3.pack(side=RIGHT)
trv3.place(x=0, y=0)

column_headers3 = ["No", "Nama", "Puskesmas", "Resiko Kredit"]
column_widths3 = [70, 120, 120, 200]

# memastikan jumlah kolom susuai dengan panjang column_headers dan column_widths
assert len(column_headers3) == len(trv3["column"])

for i, header in enumerate(column_headers3):
    trv3.heading(i, text=header)

for i, width in enumerate(column_widths3):
    # Memastikan indeks kolom tidak melebihi jumlah kolom yang telah didefinisikan
    if i < len(trv3["column"]):
        trv3.column(i, width=width, anchor=CENTER)


# fungsi untuk user klik 2x di trv
# trv.bind('<Double 1>', getrow)
# trv2.bind('<Double 1>', getrow)
trv3.bind('<Double 1>', getrow)


if __name__ == '__main__':
    root.title("Aplikasi Simpan Pinjam")
    root.geometry("1060x650")
    root.resizable(FALSE, FALSE)
    if (isFirst("LOANS")):
        create_table()
    else:
        select_all()
    root.mainloop()
    conn.close()