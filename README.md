# 🚀 Pencarian Jalur Terpendek Kampus UNIB (Floyd-Warshall + Tkinter GUI)

Aplikasi desktop sederhana berbasis Python yang digunakan untuk mencari jalur terpendek antar titik atau gedung di Universitas Bengkulu menggunakan algoritma **Floyd-Warshall**. Hasil pencarian jalur juga dilengkapi dengan estimasi **jarak tempuh** dan **biaya transportasi**, serta ditampilkan melalui antarmuka pengguna (GUI) berbasis Tkinter.

## 🧠 Fitur Utama
- Input asal dan tujuan gedung di kampus UNIB melalui dropdown.
- Perhitungan jalur terpendek antar gedung menggunakan algoritma **Floyd-Warshall**.
- Estimasi total **jarak tempuh** (dalam meter).
- Estimasi total **biaya transportasi** (dalam Rupiah).
- Tampilan GUI yang sederhana dan mudah digunakan.

## 📌 Struktur Graph
Graph direpresentasikan dalam bentuk **adjacency list** berupa dictionary Python. Setiap simpul (gedung atau gerbang) menyimpan daftar tetangganya beserta jaraknya dalam meter.

Contoh:
```python
"Pintu Gerbang Depan": [("Pasca Hukum", 200)],
"Pasca Hukum": [("Pintu Gerbang Depan", 200), ("MAKSI (Ged C)", 400)],
Algoritma Floyd-Warshall
Digunakan untuk menghitung semua pasangan jarak terpendek antar simpul (all-pairs shortest path). Implementasi mencakup:

Matriks jarak (dist)

Matriks node berikutnya (next_node) untuk rekontruksi jalur

🖼️ Tampilan Aplikasi
GUI dibuat menggunakan tkinter. Terdapat dua dropdown untuk memilih gedung asal dan tujuan, tombol untuk mencari jalur, dan area hasil untuk menampilkan rute, jarak, serta estimasi biaya.
