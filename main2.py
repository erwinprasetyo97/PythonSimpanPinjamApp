from tkinter import *
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from datetime import datetime
import pandas as pd
from tkinter import filedialog
from datetime import datetime
from tkinter.ttk import Notebook, Style
import logging


root = Tk()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

conn = sqlite3.connect("pinjamanpuskesmas.db")
# conn.set_trace_callback(print)
cursor = conn.cursor()

# Atur level logging seeuai kebutuhan
logging.basicConfig(level=logging.DEBUG)

# Create a notebook baris pertama
notebook = ttk.Notebook(root)
notebook2 = ttk.Notebook(root)

# notebook.pack(fill="both", padx=20, pady=10)
notebook.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="w")
notebook2.grid(row=2, column=0, padx=(20, 20), pady=10, sticky="nsew")
# membuat tabel borrow


def create_borrow_table():
    # Menonaktifkan pengecekan kunci asing
    cursor.execute("PRAGMA foreign_keys=off")
    cursor.execute("PRAGMA timezone = 'Asia/Jakarta'")
    cursor.execute("DROP TABLE IF EXISTS BORROW")
    query = """
    CREATE TABLE BORROW(
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

# membuat table deposits


def create_deposits_table():
    cursor.execute("PRAGMA journal_mode = WAL")
    cursor.execute("PRAGMA foreign_keys=off")
    cursor.execute("PRAGMA timezone = 'Asia/Jakarta'")
    cursor.execute("DROP TABLE IF EXISTS DEPOSITS")
    query = """
    CREATE TABLE DEPOSITS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        JUMLAH_SETOR INTEGER NOT NULL,
        JUMLAH_ANGSURAN INTEGER,
        SELISIH INTEGER,
        GAGAL_POTONG INTEGER,
        SISA_POKOK INTEGER,
        TIMESTAMP TIMESTAMP DEFAULT (datetime('now', 'localtime')),
        BORROW_ID INTEGER,
        FOREIGN KEY(BORROW_ID) REFERENCES BORROW(ID)
    )
    """
    cursor.execute(query)

    cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("PRAGMA timezone = DEFAULT")
    conn.commit()


def isFirst(table_name):
    try:
        query = '''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}' '''.format(
            table_name)
        cursor.execute(query)
        result = cursor.fetchone()
        if result and result[0] == 1:
            return False  # Tabel sudah ada
        else:
            return True  # Tabel belum ada
    except Exception as e:
        print("Error:", e)
        return True  # Tabel belum ada karena ada kesalahan saat menjalankan query


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return FALSE

# query for display all data


def select_all_borrow():
    try:
        # Menentukan kolom yang ingin ditampilkan
        query = "SELECT ID, NAMA, NIP, PUSKESMAS, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH, TIMESTAMP FROM BORROW"
        cursor.execute(query)
        rows = cursor.fetchall()
        update_trv(rows)

    except Exception as e:
        print("Error fetching data:", e)

# query for display data based "jumlah_pinjaman"


def select_based_loans(event=None):
    try:
        # Menentukan kolom yang ingin ditampilkan
        columns_to_select = ['NAMA', 'PUSKESMAS',
                             'TIMESTAMP', 'JUMLAH_PINJAMAN']

        # Membuat pernyataan SQL SELECT
        query = f"SELECT {', '.join(columns_to_select)} FROM BORROW;"
        cursor.execute(query)
        rows = cursor.fetchall()

        update_trv2(rows)
    except Exception as e:
        print("Error fetching data:", e)

# query for display data based "Resiko Kredit"


def select_based_credit_risk(event=None):
    try:
        # Menentukan kolom yang ingin ditampilkan
        columns_to_select = ['NAMA', 'PUSKESMAS', 'RESIKO_KREDIT']

        # Membuat pernyataan SQL SELECT
        query = f"SELECT {', '.join(columns_to_select)} FROM BORROW;"
        cursor.execute(query)
        rows = cursor.fetchall()

        update_trv3(rows)

    except Exception as e:
        print("Error fetching data:", e)

# query for display data based "Bagi Hasil"


def select_based_profit_sharing(event=None):
    try:
        # Menentukan kolom yang ingin ditampilkan
        columns_to_select = ['NAMA', 'PUSKESMAS', 'BAGI_HASIL']

        # membuat pernyataan SQL SELECT
        query = f"SELECT {', '.join(columns_to_select)} FROM BORROW;"
        cursor.execute(query)
        rows = cursor.fetchall()

        update_trv4(rows)

    except Exception as e:
        print("Error fetching data:", e)

# query for display data based "Pokok"


def select_based_pokok(event=None):
    try:
        # Menentukan kolom yang ingin ditampilkan
        columns_to_select = ['NAMA', 'PUSKESMAS', 'POKOK']

        # membuat pernyataan SQL SELECT
        query = f"SELECT {', '.join(columns_to_select)} FROM BORROW;"
        cursor.execute(query)
        rows = cursor.fetchall()

        update_trv5(rows)

    except Exception as e:
        print("Error fetching data:", e)

# function untuk update treeview pada semua data


def update_trv(data):
    # Membersihkan isi treeviw sebelum memasukkan data baru
    for row in trv.get_children():
        trv.delete(row)

    # Memasukkan data baru ke dalam treeview
    for i, row in enumerate(data, start=1):
        # pastiknn urutan kolom di values sesuai dengan urutan kolom di ttk.treeview
        values = [i] + list(row)
        trv.insert("", "end", values=values)
        # print(values)

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
    for i, row in enumerate(data, start=1):
        trv3.insert("", "end", values=[i] + list(row))

# function untuk update treview berdasarkan bagi hasil


def update_trv4(data):
    # membersihkan isi treeview sebelum memasukkan data baru
    for row in trv4.get_children():
        trv4.delete(row)

    # memasukkan data baru ke dalam treeview
    for i, row in enumerate(data, start=1):
        trv4.insert("", "end", values=[i] + list(row))

# function untuk update treeview berdasarkan pokok


def update_trv5(data):
    # membersihkan isi treeview sebelum memasukkan data baru
    for row in trv5.get_children():
        trv5.delete(row)

    # memasukkan data baru ke dalam treeview
    for i, row in enumerate(data, start=1):
        trv5.insert("", "end", values=[i] + list(row))

# function untuk update treeview data setoran


def update_trv_deposit():
    # Hapus semua item di treeview
    for item in trv_display_deposits.get_children():
        trv_display_deposits.delete(item)

    # Query untuk mengambil data dari table DEPOSITS
    query_select_deposits = """
        SELECT ID, TIMESTAMP, BORROW_ID, JUMLAH_SETOR, SELISIH, GAGAL_POTONG
        FROM DEPOSITS
    """

    cursor.execute(query_select_deposits)
    rows = cursor.fetchall()
    print(rows)

    # Isi treeview dengan data
    for index, row in enumerate(rows, start=1):
        trv_display_deposits.insert("", "end", values=(index,) + row)

    # commit setelah update treeview
    # conn.commit()


# function untuk menambahkan data ke dalam table BORROW
def add_new_borrow():
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
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

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
                INSERT INTO BORROW
                (NAMA, NIP, PUSKESMAS, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH, TIMESTAMP)
                values (:NAMA, :NIP, :PUSKESMAS, :TANGGAL_LAHIR, :ALAMAT, :JUMLAH_PINJAMAN, :JANGKA_WAKTU, :RESIKO_KREDIT, :BAGI_HASIL, :POKOK, :TERIMA_BERSIH, :TIMESTAMP)
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
                "TERIMA_BERSIH": jumlah_pinjaman_value - resiko_kredit_value,
                "TIMESTAMP": timestamp
            }
            cursor.execute(query, params)
            conn.commit()
            messagebox.showinfo("Info", "Data Berhasil ditambahkan !")
            print("Data added Succesfully.")
            select_all_borrow()
            select_based_loans()
            select_based_credit_risk()
            select_based_profit_sharing()
            select_based_pokok()
            clear_field_borrow()

    except Exception as e:
        print("Error :", e)
        messagebox.showerror(
            "Error", "Pastikan format data yang diupdate sudah benar")

# function untuk tambah data setoran
def add_data_deposit():
    try:
        # ambil data dari filed
        jumlah_setoran = v_jumlah_setoran.get()
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if not jumlah_setoran:
            messagebox.showerror("Error", "Field Jumlah setoran harus diisi")
            return

        if not str(jumlah_setoran).isdecimal():
            messagebox.showerror(
                "Error", "Jumlah Setoran harus berupa bilangan bulat positif")
            return

        if not borrow_id:
            messagebox.showerror("Error", "Pilih data terlebih dahulu")
            return

        # mendapatkan nilai POKOK dan BAGI_HASIL dari table BORROW berdasarkan ID peminjaman
        query_borrow_data = """
            SELECT POKOK, BAGI_HASIL, JUMLAH_PINJAMAN
            FROM BORROW
            WHERE ID = :BORROW_ID
        """

        params_borrow_data = {
            "BORROW_ID": borrow_id
        }

        cursor.execute(query_borrow_data, params_borrow_data)
        borrow_data = cursor.fetchone()

        # menghitung nilai JUMLAH_ANGSURAN berdasarkan POKOK dan BAGI_HASIL
        if borrow_data:
            pokok_value = borrow_data[0]
            bagi_hasil_value = borrow_data[1]
            jumlah_angsuran_value = pokok_value + bagi_hasil_value
            jumlah_pinjaman = borrow_data[2]
        else:
            # Handle jika BORROW tidak ditemukan
            jumlah_angsuran_value = 0
            jumlah_pinjaman = 0

        # Mendapatkan nilai selisih
        selisih_value = jumlah_angsuran_value - int(jumlah_setoran)

        # Menghitung nilai GAGAL_POTONG berdasarkan SELISIH
        gagal_potong_sebelumnya_value = get_gagal_potong_sebelumnya(borrow_id)

        # Menghitung nilai GAGAL_POTONG berdasarkan SELISIH
        gagal_potong_value = selisih_value + gagal_potong_sebelumnya_value
        
        # Mendapatkan nilai sisa pokok sebelumnya
        sisa_pokok_sebelumnya_value = get_sisa_pokok_sebelumnya(borrow_id)

        # Menghitung nilai SISA_POKOK
        if gagal_potong_sebelumnya_value == 0:
            sisa_pokok_value = jumlah_pinjaman - pokok_value
        else:
            sisa_pokok_value = sisa_pokok_sebelumnya_value - pokok_value + gagal_potong_sebelumnya_value

        # # Menghitung sisa pokok setelah penyetoran
        # sisa_pokok_value = sisa_pokok_sebelumnya_value - pokok_value + max(gagal_potong_value, 0)

        # setelah mendapatkan nilai JUMLAH_ANGSURAN, Anda dapat menggunakannya dalam query untuk mengisi tabel DEPOSITS
        query_insert_deposit = """
            INSERT INTO DEPOSITS
            (JUMLAH_SETOR, JUMLAH_ANGSURAN, SELISIH, GAGAL_POTONG, SISA_POKOK, TIMESTAMP, BORROW_ID)
            VALUES (:JUMLAH_SETOR, :JUMLAH_ANGSURAN, :SELISIH, :GAGAL_POTONG, :SISA_POKOK, :TIMESTAMP, :BORROW_ID)
        """

        params_insert_deposit = {
            "JUMLAH_SETOR": jumlah_setoran,
            "JUMLAH_ANGSURAN": jumlah_angsuran_value,
            "SELISIH": selisih_value,
            "GAGAL_POTONG": 0,
            "SISA_POKOK": sisa_pokok_value,
            "TIMESTAMP": timestamp,
            "BORROW_ID": borrow_id

        }

        cursor.execute(query_insert_deposit, params_insert_deposit)
        conn.commit()
        messagebox.showinfo("Info", "Data berhasil ditambahkan ! ")
        print("Data added successfully")
        update_trv_deposit()
        logging.info("Data deposit berhasil ditambahkan")

    except Exception as e:
        logging.error(f"Erorr during add_data_deposit: {e}")
        conn.rollback()  # kembalikan perubahan jika terjadi kesalahan
        print("Error during commit : ", e)
        messagebox.showerror("Error", "Gagal menyimpan perubahan ke database")


def get_gagal_potong_sebelumnya(borrow_id):
    try:
        query = """
            SELECT GAGAL_POTONG
            FROM DEPOSITS
            WHERE BORROW_ID = :BORROW_ID
            ORDER BY TIMESTAMP DESC
            LIMIT 1
        """
        params = {
            "BORROW_ID": borrow_id
        }
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            return result[0]  # Mengembalikan nilai GAGAL_POsONG terakhir
        else:
            return 0  # Jika tidak ada data DEPOSITS terkait, mengembalikan 0

    except Exception as e:
        print("Error in get_gagal_potong_sebelumnya:", e)
        return 0  # Mengembalikan 0 jika terjadi kesalahan


def get_sisa_pokok_sebelumnya(borrow_id):
    try:
        query = """
            SELECT JUMLAH_PINJAMAN - POKOK + COALESCE(GAGAL_POTONG, 0)
            FROM DEPOSITS
            JOIN BORROW ON DEPOSITS.BORROW_ID = BORROW.ID
            WHERE BORROW_ID = :BORROW_ID
            ORDER BY TIMESTAMP DESC
            LIMIT 1
        """
        params = {
            "BORROW_ID": borrow_id
        }
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result is not None:
            # Mengembalikan nilai sisa pokok jika hasil tidak None
            return result[0]
        else:
            return 0  # Jika hasil query None, kembalikan nilai default 0

    except Exception as e:
        print("Error in get_sisa_pokok_sebelumnya:", e)
        return 0  # Jika terjadi kesalahan, kembalikan nilai default 0
    
# function untuk update data borrow

def update_data_borrow():
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
                UPDATE BORROW
                SET NAMA=?, NIP=?, PUSKESMAS=?, ALAMAT=?, TANGGAL_LAHIR=?, JUMLAH_PINJAMAN=?, JANGKA_WAKTU=? WHERE ID=?
            """
            params = (
                v_nama.get(),
                v_nip.get(),
                v_puskesmas.get(),
                v_alamat_rumah.get(),
                v_tanggal_lahir.get(),
                v_jumlah_pinjaman.get(),
                v_jangka_waktu.get(),
                v_id.get()
            )
            cursor.execute(query, params)
            conn.commit()
            clear_field_borrow()
            select_all_borrow()
            select_based_loans()
            select_based_credit_risk()
            select_based_profit_sharing()
            select_based_pokok()

            # show success message
            messagebox.showinfo("Info", "Data berhasil diperbarui.")
        else:
            return True
    except Exception as e:
        print("Error", e)
        messagebox.showerror(
            "Error", "Pastikan format data yang diupdate sudah benar")

# function untuk menampilkan data pinjaman dari database kedalam treeview


def getrow_borrow(event):
    global borrow_id

    rowid = trv.identify_row(event.y)
    item = trv.item(rowid)

    if 'values' in item and len(item['values']) >= 13:
        v_id.set(item['values'][1])
        v_nama.set(item['values'][2])
        v_nip.set(item['values'][3])
        v_puskesmas.set(item['values'][4])
        v_tanggal_lahir.set(item['values'][5])
        v_alamat_rumah.set(item['values'][6])
        v_jumlah_pinjaman.set(item['values'][7])
        v_jangka_waktu.set(item['values'][8])

        borrow_id = item['values'][1]
        print("ID BORROW : ", borrow_id)

    else:
        print("Error: Insufficient values in the 'valuesf atribute.")


def getrow_deposits(event):
    rowid = trv_display_deposits.identify_row(event.y)
    item = trv_display_deposits.item(rowid)

    if 'values' in item and len(item['values']) >= 9:
        v_id.set(item['values'][1])
        v_jumlah_setoran.set(item['values'][2])

    else:
        print("Error: Insufficient values in the 'values atribute.")


def clear_field_borrow():
    entry_nama.delete(0, 'end')
    entry_nip.delete(0, 'end')
    entry_puskesmas.delete(0, 'end')
    dob_entry.delete(0, 'end')
    address_entry.delete(0, 'end')
    jumlahpinjaman_entry.delete(0, 'end')
    jangkawaktu_entry.delete(0, 'end')
    entry_jumlah_setoran.delete(0, 'end')


def delete_data_borrow():
    try:
        id = v_id.get()
        if (messagebox.askyesno("Konfirmasi Hapus?", "Apakah yakin ingin menghapus data ini ?")):
            query = "DELETE FROM BORROW WHERE ID = {}".format(id)
            cursor.execute(query)
            conn.commit()
            print("Success delete data")
            clear_field_borrow()
            select_all_borrow()
            select_based_loans()
            select_based_credit_risk()
            select_based_profit_sharing()
            select_based_pokok()
        else:
            return True
    except Exception as e:
        print("Error :", e)

# untuk export data to excel


def export_data_borrow():
    try:
        # Menampilkan dialog untuk memilih lokasi penyimpanan file Excel
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if file_path:
            # Mengambil data dari database
            query = "SELECT * FROM BORROW"
            cursor.execute(query)
            rows = cursor.fetchall()

        # Membuat DataFrame dari data
        df = pd.DataFrame(rows, columns=[
            'ID', 'NAMA', 'NIP', 'PUSKESMAS', 'TANGGAL_LAHIR', 'ALAMAT', 'JUMLAH_PINJAMAN', 'JANGKA_WAKTU', 'RESIKO_KREDIT', 'BAGI_HASIL', 'POKOK', 'TERIMA_BERSIH', 'TIMESTAMP'
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
    try:
        q2 = q.get()
        query = """
        SELECT ID, NAMA, NIP, PUSKESMAS, TANGGAL_LAHIR, ALAMAT, JUMLAH_PINJAMAN, JANGKA_WAKTU, RESIKO_KREDIT, BAGI_HASIL, POKOK, TERIMA_BERSIH FROM BORROW WHERE NAMA LIKE ? OR NIP LIKE ?
        """
        cursor.execute(query, ('%' + q2 + '%', '%' + q2 + '%'))
        conn.commit()
        rows = cursor.fetchall()
        update_trv(rows)
        update_trv2(rows)
        update_trv3(rows)
        update_trv4(rows)
        update_trv5(rows)
    except Exception as e:
        print("Error :", e)
        messagebox.showerror(
            "Error", "Terjadi Kesalahan saat pencarian data"
        )


def clear():
    ent.delete(0, 'end')
    clear_field_borrow()
    select_all_borrow()
    select_based_loans()
    select_based_credit_risk()
    select_based_profit_sharing()
    select_based_pokok()

# untuk mengecek notebook yang aktif


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


# Wrapper

wrapperPencarian = LabelFrame(root, text="Pencarian")

# frame or tab (notebook)
frame1 = ttk.Frame(notebook, width=400, height=280)
frame2 = ttk.Frame(notebook, width=400, height=280)
frame3 = ttk.Frame(notebook, width=400, height=280)
frame4 = ttk.Frame(notebook, width=400, height=280)
frame5 = ttk.Frame(notebook, width=400, height=280)
frame_display_deposits = ttk.Frame(notebook, width=400, height=280)

# Frame untuk tab kedua
frameInputDataPeminjam = ttk.Frame(notebook2, width=400, height=200)
frameInputDataSetoran = ttk.Frame(notebook2, width=400, height=200)


# Frame configuration for frame1
frame1.grid_rowconfigure(0, weight=1, minsize=100)
frame1.grid_columnconfigure(0, weight=1, minsize=100)

# Frame configuration for frame2
frame2.grid_rowconfigure(0, weight=1, minsize=100)
frame2.grid_columnconfigure(0, weight=1, minsize=100)

# Frame configuration for frame 3
frame3.grid_rowconfigure(0, weight=1, minsize=100)
frame3.grid_columnconfigure(0, weight=1, minsize=100)

# Frame configuration for frame 4
frame4.grid_rowconfigure(0, weight=1, minsize=100)
frame4.grid_columnconfigure(0, weight=1, minsize=100)

# Frame configuration for frame 5
frame5.grid_rowconfigure(0, weight=1, minsize=100)
frame5.grid_columnconfigure(0, weight=1, minsize=100)

# Frame configuration for frame_display_deposits
frame_display_deposits.grid_rowconfigure(0, weight=1, minsize=100)
frame_display_deposits.grid_columnconfigure(0, weight=1, minsize=100)

# frame notbook untuk inputData Pinjaman
frame1.grid(row=0, column=0, sticky="nsew", padx=(10, 20), pady=10)
frame2.grid(row=0, column=0, sticky="nsew", padx=(10, 20), pady=10)
frame3.grid(row=0, column=0, sticky="nsew")
frame4.grid(row=0, column=0, sticky="nsew")
frame5.grid(row=0, column=0, sticky="nsew")
frame_display_deposits.grid(
    row=0, column=0, sticky="nsew", padx=(10.20), pady=10)


frameInputDataPeminjam.grid(row=0, column=0, sticky="nsew")
frameInputDataSetoran.grid(row=0, column=0, sticky="nsew")


# Add Frames to notebook display data
notebook.add(frame1, text='Semua')
notebook.add(frame2, text='Per Jumlah Pinjaman')
notebook.add(frame3, text='Per Resiko Kredit')
notebook.add(frame4, text='Per Bagi Hasil')
notebook.add(frame5, text='Per Sisa Pokok')
notebook.add(frame_display_deposits, text="Data Setoran")

notebook2.add(frameInputDataPeminjam, text='Input Data Peminjam')
notebook2.add(frameInputDataSetoran, text="Input Data Setoran")


notebook.bind("<<NotebookTabChanged>>", lambda event: notebook_event(event))

# Posisi Wrapper
# wrapperPencarian.pack(fill="both", padx=20, pady=10)
wrapperPencarian.grid(row=1, column=0, padx=(
    20, 20), pady=10, sticky="nsew", columnspan=2)

# Form variable
v_id = IntVar()
v_nama = StringVar()
v_nip = IntVar()
v_puskesmas = StringVar()
v_tanggal_lahir = StringVar()
v_alamat_rumah = StringVar()
v_jumlah_pinjaman = IntVar()
v_jangka_waktu = IntVar()
v_jumlah_setoran = IntVar()

# Frame untuk Form di Input Data Pinjaman
form_frame_borrow = ttk.Frame(frameInputDataPeminjam, padding="5")
form_frame_borrow.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label dan Entry untuk Nama
label_nama = ttk.Label(form_frame_borrow, text="Nama")
label_nama.grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nama = ttk.Entry(form_frame_borrow, textvariable=v_nama)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

# Label dan Entry untuk NIP
label_nip = ttk.Label(form_frame_borrow, text="NIP")
label_nip.grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_nip = ttk.Entry(form_frame_borrow, textvariable=v_nip)
entry_nip.grid(row=1, column=1, padx=5, pady=5)

# Label dan Entry untuk Puskesmas
label_puskesmas = ttk.Label(form_frame_borrow, text="Puskesmas")
label_puskesmas.grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_puskesmas = ttk.Entry(form_frame_borrow, textvariable=v_puskesmas)
entry_puskesmas.grid(row=2, column=1, padx=5, pady=5)

# Label dan Entry untuk alamat Rumah
label_address = ttk.Label(form_frame_borrow, text="Alamat Rumah")
label_address.grid(row=3, column=0, sticky="w", padx=5, pady=5)
address_entry = ttk.Entry(form_frame_borrow, textvariable=v_alamat_rumah)
address_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

# Label dan Entry untuk Tanggal Lahir
dob_label = ttk.Label(form_frame_borrow, text="Tanggal Lahir")
dob_label.grid(row=0, column=2, sticky="w", padx=5, pady=5)
dob_entry = DateEntry(form_frame_borrow, selectmode='day',
                      textvariable=v_tanggal_lahir, date_pattern="dd/mm/y")
dob_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
dob_entry.insert(0, "dd/mm/yyyy")


# Label dan Entry untuk Jumlah pinjaman
label_jumlahpinjaman = ttk.Label(form_frame_borrow, text="Jumlah Pinjaman")
label_jumlahpinjaman.grid(row=1, column=2, sticky="w", padx=5, pady=5)
jumlahpinjaman_entry = ttk.Entry(
    form_frame_borrow, textvariable=v_jumlah_pinjaman)
jumlahpinjaman_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)

# Label dan Entry untuk Jangka waktu
label_jangkawaktu = ttk.Label(form_frame_borrow, text="Jangka Waktu (bulan)")
label_jangkawaktu.grid(row=2, column=2, sticky="w", padx=5, pady=5)
jangkawaktu_entry = ttk.Entry(form_frame_borrow, textvariable=v_jangka_waktu)
jangkawaktu_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)

# Frame button add, update, delete pada InputDataPinjaman
frame_btn_borrow = Frame(frameInputDataPeminjam)
update_btn_borrow = Button(
    frame_btn_borrow, text="Update Data Pinjaman", command=update_data_borrow)
add_btn_borrow = Button(
    frame_btn_borrow, text="Tambah Data Pinjaman", command=add_new_borrow)
delete_btn_borrow = Button(
    frame_btn_borrow, text="Hapus Data Pinjaman", command=delete_data_borrow)
export_btn_borrow = Button(
    frame_btn_borrow, text="Export ke Excel", command=export_data_borrow)

frame_btn_borrow.grid(row=4, column=0, columnspan=5, sticky="w", pady=10)
add_btn_borrow.pack(side=LEFT, padx=5)
update_btn_borrow.pack(side=LEFT, padx=5)
delete_btn_borrow.pack(side=LEFT, padx=5)
export_btn_borrow.pack(side=LEFT, padx=5)

# Frame untuk di notebook Input Data Setoran
form_frame_deposits = ttk.Frame(frameInputDataSetoran, padding="5")
form_frame_deposits.grid(row=0, column=0, sticky="nsew")

# Label dan Entry untuk Nama di Input Setoran
label_nama_setoran = ttk.Label(form_frame_deposits, text="Nama")
label_nama_setoran.grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nama_setoran = ttk.Entry(
    form_frame_deposits, textvariable=v_nama, state="readonly")
entry_nama_setoran.grid(row=0, column=1, padx=5, pady=5)

# Label dan Entry untuk Nama di Input Setoran
label_puskesmas_setoran = ttk.Label(form_frame_deposits, text="Puskesmas")
label_puskesmas_setoran.grid(row=0, column=2, sticky="w", padx=5, pady=5)
entry_puskesmas_setoran = ttk.Entry(
    form_frame_deposits, textvariable=v_puskesmas, state="readonly")
entry_puskesmas_setoran.grid(row=0, column=3, padx=5, pady=5)

# Label dan Entry untuk Jumlah Setoran di Input Setoran
label_jumlah_setoran = ttk.Label(form_frame_deposits, text="Jumlah Setoran")
label_jumlah_setoran.grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_jumlah_setoran = ttk.Entry(
    form_frame_deposits, textvariable=v_jumlah_setoran)
entry_jumlah_setoran.grid(row=1, column=1, padx=5, pady=5)

# button untuk Input Data Setoran
frame_btn_deposit = Frame(frameInputDataSetoran)
update_btn_deposit = Button(
    frame_btn_deposit, text="Update Data Setoran", command=update_data_borrow)
add_btn_deposit = Button(
    frame_btn_deposit,
    text="Tambah Data Setoran",
    command=add_data_deposit
)
delete_btn_deposit = Button(
    frame_btn_deposit, text="Hapus Data Setoran", command=delete_data_borrow)
export_btn_deposit = Button(
    frame_btn_deposit, text="Export ke Setoran", command=export_data_borrow)

frame_btn_deposit.grid(row=4, column=0, columnspan=5, sticky="w", pady=10)
add_btn_deposit.pack(side=LEFT, padx=5)
update_btn_deposit.pack(side=LEFT, padx=5)
delete_btn_deposit.pack(side=LEFT, padx=5)
export_btn_deposit.pack(side=LEFT, padx=5)


# Wrapper 2 - Pencarian
q = StringVar()
lbl = Label(wrapperPencarian, text="Search")
lbl.pack(side=LEFT, padx=10, pady=15)
ent = Entry(wrapperPencarian, textvariable=q)
ent.pack(side=LEFT, padx=6, pady=15)
btn = Button(wrapperPencarian, text="Search", command=search)
btn.pack(side=LEFT, padx=6, pady=15)
cbtn = Button(wrapperPencarian, text="Clear", command=clear)
cbtn.pack(side=LEFT, padx=(6, 20))

# Function untuk create treeview


def create_treview(frame, columns, headers, widths, bind_function=None, Mysky=None):
    create_tab_notebook()
    trv = ttk.Treeview(frame, column=columns, show="headings", height=12)

    trv.tag_configure("header", background=Mysky)

    trv.grid(row=0, column=0, sticky="nsew")

    for i, header in enumerate(headers):
        trv.heading(columns[i], text=header)

    for i, width in enumerate(widths):
        trv.column(columns[i], width=width, minwidth=width, anchor=CENTER)

    if bind_function:
        trv.bind('<Double 1>', bind_function)

    # Exclude the first column from being displayed
    trv["displaycolumns"] = columns[0:]

    scrollbar_y = Scrollbar(frame, orient="vertical", command=trv.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    trv.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = Scrollbar(frame, orient="horizontal", command=trv.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    trv.configure(xscrollcommand=scrollbar_x.set)

    # frame.columnconfigure(0, weight=1)

    return trv


def create_tab_notebook():
    style = Style()
    style.theme_use("clam")


# penerapan untuk tampilkan data semua
columns_trv = ("No", "Id", "Nama", "NIP", "Puskesmas", "Tanggal Lahir", "Alamat Rumah",
               "Jumlah Pinjaman", "Jangka Waktu", "Resiko Kredit", "Bagi Hasil", "Pokok", "Terima Bersih", "Tanggal Pinjam")
headers_trv = ("No", "Id", "Nama", "NIP", "Puskesmas", "Tanggal Lahir", "Alamat Rumah",
               "Jumlah Pinjaman", "Jangka Waktu", "Resiko Kredit", "Bagi Hasil", "Pokok", "Terima Bersih", "Tanggal Pinjam")
widths_trv = (70, 0, 120, 120, 120, 100, 120,
              100, 120, 120, 100, 100, 100, 150)


trv = create_treview(frame1, columns_trv, headers_trv,
                     widths_trv, bind_function=getrow_borrow)

trv.column("#12", anchor=CENTER)
trv.column("#13", anchor=CENTER)

# penerapan untuk tampilkan data per Jumlah Pinjaman
column_trv2 = (0, 2, 3, 4, 5)
headers_trv2 = ("No", "Nama", "Puskesmas",
                "Tanggal Realisasi", "Jumlah Pinjaman")
widths_trv2 = (70, 120, 120, 120, 120)

trv2 = create_treview(frame2, column_trv2, headers_trv2,
                      widths_trv2, bind_function=getrow_borrow)

# penerapan untuk tampilkan data per resiko kredit
column_trv3 = (0, 2, 3, 4)
headers_trv3 = ("No", "Nama", "Puskesmas", "Resiko Kredit")
widths_trv3 = (70, 120, 120, 200)

trv3 = create_treview(frame3, column_trv3, headers_trv3,
                      widths_trv3, bind_function=getrow_borrow)

# penerapan untuk tampilkan data per bagi hasil
column_trv4 = (0, 2, 3, 4)
headers_trv4 = ("No", "Nama", "Puskesmas", "Bagi Hasil")
widths_trv4 = (70, 120, 120, 200)

trv4 = create_treview(frame4, column_trv4, headers_trv4,
                      widths_trv4, bind_function=getrow_borrow)

# penerapan untuk tampilkan data per Sisa Pokok
column_trv5 = (0, 2, 3, 4)
headers_trv5 = ("No", "Nama", "Puskesmas", "Pokok")
widths_trv5 = (70, 120, 120, 200)

trv5 = create_treview(frame5, column_trv5, headers_trv5,
                      widths_trv5, bind_function=getrow_borrow)

# penerapan untuk tampilkan data setoran
column_trv_display_deposits = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
headers_display_deposits = (
    "No", "Id", "Tanggal Setor", "Bulan", "Puskesmas", "Nama", "Jumlah Setor", "Selisih", "Gagal Potong", "Sisa Pokok")
width_trv_display_deposits = (70, 0, 120, 120, 120, 120, 120, 120, 120, 120)

trv_display_deposits = create_treview(frame_display_deposits, column_trv_display_deposits,
                                      headers_display_deposits, width_trv_display_deposits, bind_function=getrow_deposits)


if __name__ == '__main__':
    root.title("Aplikasi Simpan Pinjam")
    root.geometry("1060x650")
    root.resizable(TRUE, TRUE)

    try:

        # Membuat tabel DEPOSITS jika belum ada
        if (isFirst("DEPOSITS")):
            create_deposits_table()

        # Membuat tabel BORROW jika belum ada
        if (isFirst("BORROW")):
            create_borrow_table()
        else:
            # Memilih semua data dari tabel BORROW
            select_all_borrow()

        # Panggil fungsi untuk mengisi treeview saat aplikasi dibuka
        update_trv_deposit()

        root.mainloop()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # commit dan tutup koneksi di blok finally
        conn.commit()
        conn.close()
