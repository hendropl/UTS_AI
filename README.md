# Aplikasi Pencarian Jalur Kampus (Floyd-Warshall GUI)

Aplikasi ini dibuat menggunakan Python dan pustaka tkinter, yang berfungsi untuk mencari jalur terpendek antar titik di lingkungan kampus menggunakan *algoritma Floyd-Warshall*. Hasil pencarian mencakup jalur, jarak, biaya, dan estimasi waktu tempuh berdasarkan pilihan moda transportasi.

## 📌 Fitur

- Pencarian jalur terpendek dari titik awal ke tujuan
- Menampilkan hasil:
  - Rute/jalur
  - Total jarak (dalam meter)
  - Total biaya (Rp 1000 per 10 meter)
  - Waktu tempuh (untuk jalan kaki, motor, dan mobil)
- Antarmuka grafis (GUI) yang mudah digunakan

## 🧠 Algoritma yang Digunakan

*Floyd-Warshall*: Algoritma pencarian jalur terpendek untuk graf berbobot. Cocok digunakan untuk mencari semua jalur terpendek antara semua pasangan simpul.

## 🚀 Cara Menjalankan

### 1. Pastikan Python sudah terinstal
Jika belum, download dan install dari: https://www.python.org/downloads/

### 2. Jalankan aplikasi
Buka terminal/command prompt, lalu jalankan:
bash
python floyd_warshall_gui.py


Atau, jika menggunakan VSCode atau PyCharm, buka file floyd_warshall_gui.py lalu klik *Run*.

## 🛠️ Struktur GUI

- Dua dropdown: untuk memilih titik *awal* dan *tujuan*
- Tombol *"Cari Jalur"*: Menjalankan pencarian jalur menggunakan Floyd-Warshall
- Label hasil: Menampilkan hasil pencarian dalam format yang mudah dibaca

## 📊 Tabel Kecepatan Transportasi

| Moda Transportasi | Kecepatan     |
|-------------------|---------------|
| Jalan Kaki        | 4 km/jam (1.11 m/s) |
| Motor             | 60 km/jam (16.67 m/s) |
| Mobil             | 40 km/jam (11.11 m/s) |

## 📁 File Penting

- floyd_warshall_gui.py: File utama yang berisi seluruh logika dan GUI aplikasi
- README.md: Dokumentasi ini

## 📝 Catatan

- Pastikan semua nama titik pada graph sesuai dan tidak ada yang tertinggal.
- Aplikasi ini berbasis lokal dan tidak memerlukan koneksi internet.

## 📬 Kontak

Jika ada pertanyaan atau ingin mengembangkan lebih lanjut, silakan hubungi pembuat atau kirim pesan melalui GitHub Issues (jika diunggah ke GitHub).

---
