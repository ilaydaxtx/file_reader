import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

DB_PATH = "access_kayitlari.db"

def veritabani_baglanti():
    return sqlite3.connect(DB_PATH)

def verileri_getir(ip=None, tarih1=None, tarih2=None, port=None, firma_adi=None):
    conn = veritabani_baglanti()
    cursor = conn.cursor()

    sorgu = "SELECT * FROM access_log"
    kosullar = []
    parametreler = []

    if ip:
        kosullar.append("ip_adresi = ?")
        parametreler.append(ip)
    if tarih1 and tarih2:
        kosullar.append("tarih_saat BETWEEN ? AND ?")
        parametreler.extend([tarih1, tarih2])
    if port:
        kosullar.append("port_no = ?")
        parametreler.append(port)
    if firma_adi:
        kosullar.append("firma_adi = ?")
        parametreler.append(firma_adi)

    if kosullar:
        sorgu += " WHERE " + " AND ".join(kosullar)

    cursor.execute(sorgu, tuple(parametreler))
    veriler = cursor.fetchall()
    conn.close()
    return veriler

def tabloyu_guncelle(veriler):
    for i in tree.get_children():
        tree.delete(i)
    for veri in veriler:
        tree.insert("", tk.END, values=veri)

def filtrele():
    ip = ip_entry.get().strip()
    tarih1 = tarih1_entry.get().strip()
    tarih2 = tarih2_entry.get().strip()
    port = port_entry.get().strip()
    firma_adi = firma_adi_entry.get().strip()

    veriler = verileri_getir(ip if ip else None, tarih1 if tarih1 else None, 
                              tarih2 if tarih2 else None, port if port else None, 
                              firma_adi if firma_adi else None)
    tabloyu_guncelle(veriler)
    
def secili_kaydi_sil():
    secili = tree.selection()
    if not secili:
        messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz kaydı seçin.")
        return
    onay = messagebox.askyesno("Onay", "Seçilen kayıt(lar) silinsin mi?")
    if not onay:
        return

    conn = veritabani_baglanti()
    cursor = conn.cursor()
    for item in secili:
        kayit = tree.item(item)["values"]
        cursor.execute("DELETE FROM access_log WHERE id = ?", (kayit[0],))
    conn.commit()
    conn.close()
    yenile()
    messagebox.showinfo("Başarılı", "Kayıt(lar) silindi.")


def yenile():
    ip_entry.delete(0, tk.END)
    tarih1_entry.delete(0, tk.END)
    tarih2_entry.delete(0, tk.END)
    port_entry.delete(0, tk.END)
    firma_adi_entry.delete(0, tk.END)
    tabloyu_guncelle(verileri_getir())

def csv_aktar():
    veriler = verileri_getir()
    if not veriler:
        messagebox.showinfo("Bilgi", "Aktarılacak veri yok.")
        return

    dosya_yolu = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV dosyası", "*.csv")])
    if not dosya_yolu:
        return

    with open(dosya_yolu, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Tarih Saat", "IP Adresi", "Port", "MAC", "Seri No", "Firma", "Bilgisayar"])
        writer.writerows(veriler)

    messagebox.showinfo("Başarılı", f"Veriler '{dosya_yolu}' dosyasına aktarıldı.")


pencere = tk.Tk()
pencere.title("Access Log Görüntüleyici")
pencere.geometry("1100x500")


aramalar_frame = tk.Frame(pencere)
aramalar_frame.pack(pady=10)

tk.Label(aramalar_frame, text="IP Adresi:").grid(row=0, column=0, padx=3)
ip_entry = tk.Entry(aramalar_frame)
ip_entry.grid(row=0, column=1, padx=3)

tk.Label(aramalar_frame, text="Tarih 1 (gg.aa.yyyy ss:dd:sn):").grid(row=0, column=2, padx=3)
tarih1_entry = tk.Entry(aramalar_frame, width=20)
tarih1_entry.grid(row=0, column=3, padx=3)

tk.Label(aramalar_frame, text="Tarih 2:").grid(row=0, column=4, padx=3)
tarih2_entry = tk.Entry(aramalar_frame, width=20)
tarih2_entry.grid(row=0, column=5, padx=3)

tk.Label(aramalar_frame, text="Port Numarası:").grid(row=0, column=6, padx=3)
port_entry = tk.Entry(aramalar_frame)
port_entry.grid(row=0, column=7, padx=3)

tk.Label(aramalar_frame, text="Firma Adı:").grid(row=0, column=8, padx=3)
firma_adi_entry = tk.Entry(aramalar_frame)
firma_adi_entry.grid(row=0, column=9, padx=3)

tk.Button(aramalar_frame, text="Filtrele", command=filtrele).grid(row=0, column=10, padx=3)
tk.Button(aramalar_frame, text="Yenile", command=yenile).grid(row=0, column=11, padx=3)
tk.Button(aramalar_frame, text="CSV'ye Aktar", command=csv_aktar).grid(row=0, column=12, padx=3)
tk.Button(aramalar_frame, text="Seçili Kaydı Sil", command=secili_kaydi_sil).grid(row=0, column=13, padx=3)



sutunlar = ["ID", "Tarih Saat", "IP Adresi", "Port", "MAC", "Seri No", "Firma", "Bilgisayar"]
tree = ttk.Treeview(pencere, columns=sutunlar, show="headings")
for s in sutunlar:
    tree.heading(s, text=s)
    tree.column(s, width=120)
tree.pack(expand=True, fill="both")

tabloyu_guncelle(verileri_getir())

pencere.mainloop()
