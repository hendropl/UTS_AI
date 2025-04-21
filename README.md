# 🏫 Aplikasi Pencarian Jalur Kampus UNIB (Floyd-Warshall + OSMnx)

Aplikasi ini merupakan alat bantu pencarian rute terpendek antar gedung di kampus Universitas Bengkulu (UNIB). Dibuat menggunakan Python, algoritma Floyd-Warshall, dan pustaka visualisasi seperti Folium dan OSMnx, aplikasi ini memperhitungkan aturan akses gerbang berdasarkan waktu serta menampilkan jalur nyata sesuai peta jalan (real-road path).

# 📌 Fitur

- Pencarian jalur terpendek berdasarkan algoritma Floyd-Warshall  
- Visualisasi peta UNIB menggunakan Folium  
- Rute jalan nyata berdasarkan data OpenStreetMap (via OSMnx)  
- Estimasi waktu tempuh berdasarkan kecepatan rata-rata jalan kaki  
- Aturan akses gerbang berdasarkan waktu dan hari  
- Petunjuk arah berdasarkan kompas (utara, timur laut, dll.)  
- Antarmuka terminal dan output HTML interaktif  

# 🧠 Algoritma yang Digunakan

- **Floyd-Warshall**: Menentukan semua pasangan jalur terpendek dalam graf berarah berbobot.  
- **OSMnx + NetworkX**: Untuk menyesuaikan jalur yang realistis berdasarkan bentuk jalan di peta sebenarnya.

# 🛑 Aturan Akses Gerbang

| Gerbang                   | Hari & Jam                             | Akses                            |
|---------------------------|----------------------------------------|----------------------------------|
| Gerbang Masuk Belakang    | Senin–Jumat 07:00–18:00                | Masuk (jalur kiri & kanan)      |
|                           | Sabtu–Minggu atau di luar jam tersebut| Hanya jalur kiri bisa masuk     |
| Gerbang Keluar Belakang   | Senin–Jumat 06:00–18:00                | Keluar                           |
|                           | Di luar waktu tersebut                 | Tertutup                         |
| Gerbang Masuk Rektorat    | Setiap saat                            | Hanya masuk ke arah kiri        |

# 📊 Tabel Kecepatan Transportasi

| Moda Transportasi | Kecepatan             |
|-------------------|-----------------------|
| Jalan Kaki        | 4 km/jam (1.11 m/s)   |
| Motor             | 60 km/jam (16.67 m/s) |
| Mobil             | 40 km/jam (11.11 m/s) |

# 🚀 Cara Menjalankan

1. **Instalasi Python**  
   Pastikan Python 3 sudah terpasang. Jika belum: 📥 https://www.python.org/downloads/

2. **Instalasi pustaka yang dibutuhkan**  
   Buka terminal dan jalankan:

   ```bash
   pip install folium osmnx geopy pytz
# 📊 Kecepatan Jalan Kaki
Moda | Kecepatan
Jalan Kaki | 5 km/jam (1.4 m/s)
