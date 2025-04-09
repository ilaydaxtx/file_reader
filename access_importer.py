import os
import sqlite3

def veritabani_olustur():
    conn = sqlite3.connect("access_kayitlari.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih_saat TEXT,
            ip_adresi TEXT,
            port_no TEXT,
            mac_adresi TEXT,
            seri_no TEXT,
            firma_adi TEXT,
            bilgisayar_adi TEXT
        )
    """)
    conn.commit()
    conn.close()

def veritabani_kaydet(veriler):
    conn = sqlite3.connect("access_kayitlari.db")
    cursor = conn.cursor()
    for veri in veriler:
        if len(veri) == 7:
            cursor.execute("""
                INSERT INTO access_log (tarih_saat, ip_adresi, port_no, mac_adresi, seri_no, firma_adi, bilgisayar_adi)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, veri)
    conn.commit()
    conn.close()

def access_dosyalari_oku(klasor):
    veriler = []
    for dosya_adi in os.listdir(klasor):
        if dosya_adi.endswith("access.txt"):
            dosya_yolu = os.path.join(klasor, dosya_adi)
            with open(dosya_yolu, "r", encoding="utf-8") as dosya:
                for satir in dosya:
                    parcala = [parca.strip() for parca in satir.strip().split("&")]
                    veriler.append(parcala)
    return veriler

def main():
    klasor = "access_files"  #KLASOR ADI BU ONEMLI, DEGISMEMESI LAZIM
    if not os.path.exists(klasor):
        print(f"{klasor} klasörü bulunamadı.")
        return
    veritabani_olustur()
    veriler = access_dosyalari_oku(klasor)
    veritabani_kaydet(veriler)
    print("Veri başarıyla veritabanına kaydedildi.")

if __name__ == "__main__":
    main()
