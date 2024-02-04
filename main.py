from tkinter import *
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from datetime import datetime
import pandas as pd
from tkinter import filedialog


root = Tk()

conn = sqlite3.connect("pinjamanpuskesmas.db")
cursor = conn.cursor()


def create_table():
    # Menonaktifkan pengecekan kunci asing
    cursor.execute("PRAGMA foreign_keys=off")
    cursor.execute("DROP TABLE IF EXISTS LOANS")
    query = """
    CREATE TABLE LOANS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAMA TEXT NOT NULL,
        NIP INTEGER NOT NULL,
        INSTANSI TEXT NOT NULL,
        TANGGAL_LAHIR TEXT NOT NULL,
        ALAMAT TEXT NOT NULL,
        JUMLAH_PINJAMAN INTEGER NOT NULL,
        JANGKA_WAKTU INTEGER NOT NULL,
        RESIKO_KREDIT INT,
        BAGI_HASIL INT,
        POKOK INT,
        TERIMA_BERSIH INT,
        URAIAN TEXT
    )
    """
    cursor.execute(query)
    cursor.execute("PRAGMA foreign_keys=on")
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


def select_all():
    query = "SELECT ID, NAMA, NIP, INSTANSI, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH, URAIAN FROM LOANS"
    cursor.execute(query)
    rows = cursor.fetchall()
    update_trv(rows)


def update_trv(rows):
    trv.delete(*trv.get_children())
    for idx, i in enumerate(rows, start=1):
        trv.insert('', 'end', values=(i[0], idx, *i[1:]))


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

            query = """ 
                UPDATE LOANS
                SET NAMA=?, NIP=?, INSTANSI=?, ALAMAT=?, TANGGAL_LAHIR=?, JUMLAH_PINJAMAN=?, JANGKA_WAKTU=?, URAIAN=? WHERE ID=?
            """
            params = (
                v_nama.get(),
                v_nip.get(),
                v_instansi.get(),
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

            # show success message
            messagebox.showinfo("Info", "Data berhasil diperbarui.")
        else:
            return True
    except Exception as e:
        print("Error", e)
        messagebox.showerror("Error", "Pastikan format data yang diupdate sudah benar")


def add_new():
    try:
        # Ambil nilai dari setiap field
        nama_value = v_nama.get()
        nip_value = v_nip.get()
        instansi_value = v_instansi.get()
        tanggal_lahir_value = v_tanggal_lahir.get()
        alamat_value = v_alamat_rumah.get()
        jumlah_pinjaman_value = v_jumlah_pinjaman.get()
        jangka_waktu_value = v_jangka_waktu.get()
        uraian_value = v_uraian.get()

        if not nama_value or not nip_value or not tanggal_lahir_value or not jumlah_pinjaman_value or not jangka_waktu_value:
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        if not str(jumlah_pinjaman_value or not nip_value or not jangka_waktu_value).isdecimal():
            messagebox.showerror(
                "Error", "Jumlah pinjaman harus berupa bilangan bulat positif")
            return

        # Memanggil fungsi validasi tanggal lahir
        if not is_valid_date(tanggal_lahir_value):
            messagebox.showerror(
                "Kesalahan", "Format tanggal lahir tidak valid")
            return

        jumlah_pinjaman_int = int(jumlah_pinjaman_value)

        query = """
            INSERT INTO LOANS
            (NAMA, NIP, INSTANSI, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH, URAIAN)
            values (:NAMA, :NIP, :INSTANSI, :TANGGAL_LAHIR, :ALAMAT, :JUMLAH_PINJAMAN, :JANGKA_WAKTU, :RESIKO_KREDIT, :BAGI_HASIL, :POKOK, :TERIMA_BERSIH, :URAIAN)
            """
        params = {
            "NAMA": nama_value,
            "NIP": nip_value,
            "INSTANSI": instansi_value,
            "ALAMAT": alamat_value,
            "TANGGAL_LAHIR": tanggal_lahir_value,
            "JUMLAH_PINJAMAN": jumlah_pinjaman_value,
            "JANGKA_WAKTU": jangka_waktu_value,
            "RESIKO_KREDIT": 1.5 * jumlah_pinjaman_value,
            "BAGI_HASIL": 0.01 * jumlah_pinjaman_value,
            "POKOK": jumlah_pinjaman_value / jangka_waktu_value,
            "TERIMA_BERSIH": jumlah_pinjaman_value - (1.5 * jumlah_pinjaman_value),
            "URAIAN": uraian_value
        }
        cursor.execute(query, params)
        conn.commit()
        print("Data added Succesfully.")
        select_all()
        clear_field()
    except Exception as e:
        print("Error :", e)
        messagebox.showerror("Error", "Pastikan format data yang diupdate sudah benar")


def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(rowid)

    if 'values' in item and len(item['values']) >= 14:
        v_id.set(item['values'][0])
        v_nama.set(item['values'][2])
        v_nip.set(item['values'][3])
        v_instansi.set(item['values'][4])
        v_tanggal_lahir.set(item['values'][5])
        v_alamat_rumah.set(item['values'][6])
        v_jumlah_pinjaman.set(item['values'][7])
        v_jangka_waktu.set(item['values'][8])
        v_uraian.set(item['values'][13])
    else:
        print("Error: Insufficient values in the 'values atribute.")


def clear_field():
    entry_nama.delete(0, 'end')
    entry_nip.delete(0, 'end')
    entry_instansi.delete(0, 'end')
    dob_entry.delete(0, 'end')
    address_entry.delete(0, 'end')
    jumlahpinjaman_entry.delete(0, 'end')
    jangkawaktu_entry.delete(0, 'end')
    uraian_entry.delete(0, 'end')


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
        else:
            return True
    except Exception as e:
        print("Error :", e)

def export_data():
    try:
        # Menampilkan dialog untuk memilih lokasi penyimpanan file Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if file_path:
            # Mengambil data dari database
            query = "SELECT * FROM LOANS"
            cursor.execute(query)
            rows = cursor.fetchall()

        # Membuat DataFrame dari data
        df = pd.DataFrame(rows, columns=[
            'ID', 'NAMA', 'NIP', 'INSTANSI', 'TANGGAL_LAHIR', 'ALAMAT', 'JUMLAH_PINJAMAN', 'JANGKA_WAKTU','RESIKO_KREDIT', 'BAGI_HASIL', 'POKOK', 'TERIMA_BERSIH', 'URAIAN'
        ])

        # Menyimpan DataFrame ke file Excel
        df.to_excel(file_path, index=False)
        
        # Menampilkan pesan sukses
        messagebox.showinfo("Info", f"Data berhasil diekspor ke {file_path}")
    except Exception as e:
        print("Error :", e)
        messagebox.showerror("Error", "Terjadi kesalahan saat mengekspor data.")


def search():
    q2 = q.get()
    query = """
    SELECT ID, NAMA, NIP, INSTANSI, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH, URAIAN FROM LOANS WHERE NAMA LIKE {} OR NIP LIKE {}
    """.format("'%"+q2+"%'", "'%"+q2+"%'")
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    update_trv(rows)


def clear():
    ent.delete(0, 'end')
    clear_field()
    select_all()


# Wrapper
wrapper1 = LabelFrame(root, text="Daftar Peminjam")
wrapper2 = LabelFrame(root, text="Pencarian")
wrapper3 = LabelFrame(root, text="Data Peminjam")

# Posisi Wrapper
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", padx=20, pady=10)
wrapper3.pack(fill="both", padx=20, pady=10)

# Form variable
v_id = IntVar()
v_nama = StringVar()
v_nip = IntVar()
v_instansi = StringVar()
v_tanggal_lahir = StringVar()
v_alamat_rumah = StringVar()
v_jumlah_pinjaman = IntVar()
v_jangka_waktu = IntVar()
v_uraian = StringVar()

# Frame untuk Form di Wrapper 3
form_frame = ttk.Frame(wrapper3, padding="5")
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

# Label dan Entry untuk Instansi
label_instansi = ttk.Label(form_frame, text="Instansi")
label_instansi.grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_instansi = ttk.Entry(form_frame, textvariable=v_instansi)
entry_instansi.grid(row=2, column=1, padx=5, pady=5)

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
label_jangkawaktu = ttk.Label(form_frame, text="Jangka Waktu")
label_jangkawaktu.grid(row=2, column=2, sticky="w", padx=5, pady=5)
jangkawaktu_entry = ttk.Entry(form_frame, textvariable=v_jangka_waktu)
jangkawaktu_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)

# Label dan Entry untuk Uraian
label_uraian = ttk.Label(form_frame, text="Uraian")
label_uraian.grid(row=3, column=2, sticky="w", padx=5, pady=5)
uraian_entry = ttk.Entry(form_frame, textvariable=v_uraian)
uraian_entry.grid(row=3, column=3, sticky="w", padx=5, pady=5)

# Frame button add, update, delete
frame_btn = Frame(wrapper3)
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
lbl = Label(wrapper2, text="Search")
lbl.pack(side=LEFT, padx=10, pady=15)
ent = Entry(wrapper2, textvariable=q)
ent.pack(side=LEFT, padx=6, pady=15)
btn = Button(wrapper2, text="Search", command=search)
btn.pack(side=LEFT, padx=6, pady=15)
cbtn = Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=LEFT, padx=6)

# Wrapper 1 - Tabel dari data simpan pinjam
trv = ttk.Treeview(wrapper1, column=(0, 1, 2, 3, 4, 5, 6, 7,
                   8, 9, 10, 11, 12, 13), show="headings", height=13)
style = ttk.Style()
# ["aqua", "step", "clam", "alt", "default", "classic"]
style.theme_use("clam")
trv.pack(side=RIGHT)
trv.place(x=0, y=0)

trv.heading(0, text="Id")
trv.heading(1, text="No")
trv.heading(2, text="Nama")
trv.heading(3, text="NIP")
trv.heading(4, text="Instansi")
trv.heading(5, text="Tanggal Lahir")
trv.heading(6, text="Alamat Rumah")
trv.heading(7, text="Jumlah Pinjaman")
trv.heading(8, text="Jangka Waktu")
trv.heading(9, text="Resiko Kredit")
trv.heading(10, text="Bagi Hasil")
trv.heading(11, text="Pokok")
trv.heading(12, text="Terima Bersih")
trv.heading(13, text="Uraian")

trv.column(0, stretch=NO, width=0)
trv.column(1, width=5, minwidth=70, anchor=CENTER)
trv.column(2, width=86, minwidth=120, anchor=CENTER)
trv.column(3, width=82, minwidth=120, anchor=CENTER)
trv.column(4, width=82, minwidth=120, anchor=CENTER)
trv.column(5, width=78, minwidth=120, anchor=CENTER)
trv.column(6, width=84, minwidth=120, anchor=CENTER)
trv.column(7, width=106, minwidth=120, anchor=CENTER)
trv.column(8, width=76, minwidth=120, anchor=CENTER)
trv.column(9, width=85, minwidth=120, anchor=CENTER)
trv.column(10, width=85, minwidth=120, anchor=CENTER)
trv.column(11, width=60, minwidth=120, anchor=CENTER)
trv.column(12, width=80, minwidth=120, anchor=CENTER)
trv.column(13, width=86, minwidth=120, anchor=CENTER)

# fungsi untuk user klik 2x di trv
trv.bind('<Double 1>', getrow)

# Membuat scroll bar untuk tabel
yscrollbar = Scrollbar(wrapper1, orient="vertical", command=trv.yview)
yscrollbar.pack(side=RIGHT, fill="y")

xscrollbar = Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
xscrollbar.pack(side=BOTTOM, fill="x")

trv.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

if __name__ == '__main__':
    root.title("Aplikasi Simpan Pinjam")
    root.geometry("1060x650")
    root.resizable(FALSE, FALSE)
    if (isFirst("LOANS")):
        create_table()
    else:
        select_all()
    root.mainloop()