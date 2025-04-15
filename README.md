##🏫 Aplikasi Pencarian Jalur Kampus UNIB (Floyd-Warshall + OSMnx)
Aplikasi ini merupakan alat bantu pencarian rute terpendek antar gedung di kampus Universitas Bengkulu (UNIB). Dibuat menggunakan Python, algoritma Floyd-Warshall, dan pustaka visualisasi seperti Folium dan OSMnx, aplikasi ini memperhitungkan aturan akses gerbang berdasarkan waktu serta menampilkan jalur nyata sesuai peta jalan (real-road path).

##📌 Fitur
Pencarian jalur terpendek berdasarkan algoritma Floyd-Warshall

Visualisasi peta UNIB menggunakan Folium

Rute jalan nyata berdasarkan data OpenStreetMap (via OSMnx)

Estimasi waktu tempuh berdasarkan kecepatan rata-rata jalan kaki

Aturan akses gerbang berdasarkan waktu dan hari

Petunjuk arah berdasarkan kompas (utara, timur laut, dll.)

Antarmuka terminal dan output HTML interaktif

##🧠 Algoritma yang Digunakan
Floyd-Warshall: Menentukan semua pasangan jalur terpendek dalam graf berarah berbobot.

OSMnx + NetworkX: Untuk menyesuaikan jalur yang realistis berdasarkan bentuk jalan di peta sebenarnya.

## 🛑 Aturan Akses Gerbang

| Gerbang                   | Hari & Jam                   | Akses                            |
|---------------------------|------------------------------|----------------------------------|
| Gerbang Masuk Belakang    | Senin–Jumat 07:00–18:00      | Masuk (jalur kiri & kanan)      |
|                           | Sabtu–Minggu atau di luar jam tersebut | Hanya jalur kiri bisa masuk     |
| Gerbang Keluar Belakang   | Senin–Jumat 06:00–18:00      | Keluar                           |
|                           | Di luar waktu tersebut       | Tertutup                         |
| Gerbang Masuk Rektorat    | Setiap saat                  | Hanya masuk ke arah kiri        |


# 📊 Tabel Kecepatan Transportasi

| Moda Transportasi | Kecepatan     |
|-------------------|---------------|
| Jalan Kaki        | 4 km/jam (1.11 m/s) |
| Motor             | 60 km/jam (16.67 m/s) |
| Mobil             | 40 km/jam (11.11 m/s) |

##🚀 Cara Menjalankan
1. Instalasi Python
Pastikan Python 3 sudah terpasang. Jika belum: 📥 https://www.python.org/downloads/

2. Instalasi pustaka yang dibutuhkan
Buka terminal dan jalankan:

bash
Salin
Edit
pip install folium osmnx geopy pytz
3. Jalankan aplikasi
bash
Salin
Edit
python shortest_path_unib_modified.py
🛠️ Antarmuka Aplikasi
Terminal CLI untuk memilih gedung awal & tujuan

Input waktu untuk menentukan akses gerbang

Visualisasi hasil berupa:

Jalur terpendek berdasarkan Floyd-Warshall

Jalur realistis berdasarkan OSMnx

Estimasi jarak dan waktu

Petunjuk arah berdasarkan arah mata angin

File HTML (unib_path.html) untuk melihat rute di browser

##📊 Kecepatan Jalan Kaki

Moda	Kecepatan
Jalan Kaki	5 km/jam (1.4 m/s)

##📁 Struktur File Penting
File	Fungsi
shortest_path_unib_modified.py	File utama berisi logika algoritma, akses gerbang, dan visualisasi
unib_path.html	Output visualisasi peta interaktif
README.md	Dokumentasi aplikasi
📝 Catatan
Jika tidak bisa menghasilkan rute jalan realistis (karena keterbatasan data), aplikasi akan membuat jalur garis lurus sebagai alternatif.

Aplikasi ini berjalan offline dan tidak membutuhkan koneksi internet, kecuali saat mengakses data peta OSM untuk pertama kali.
