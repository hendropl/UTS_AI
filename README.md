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

## 🔍 Analisis Algoritma dan Arsitektur

### 1. Fungsi `get_gate_access`
Fungsi ini mengecek aksesibilitas gerbang kampus berdasarkan hari dan jam saat ini.

**Implementasi:**
- Menggunakan `datetime` dan `pytz` untuk menentukan waktu lokal (`Asia/Jakarta`).
- **Aturan gerbang belakang:**
  - 🕒 **Senin–Jumat, 07.00–18.00:** semua gerbang aktif.
  - 🕙 **Di luar waktu tersebut:** hanya gerbang masuk belakang **kiri** yang aktif.

⚙️ **Kompleksitas Waktu:** `O(1)` (hanya pengecekan kondisi logika)

---

### 2. Kelas `GateController`
Mengatur akses gerbang secara fleksibel melalui beberapa metode:

- `check_back_gate_access()`: akses masuk belakang saat hari dan jam tertentu.
- `check_back_exit_access()`: akses keluar belakang dalam jam kerja.
- `check_side_gates_access()`: menentukan arah masuk/keluar berdasarkan waktu.

⚙️ **Kompleksitas Waktu:** `O(1)` per metode

---

### 3. Struktur Data `unib_buildings`
Gedung-gedung Universitas Bengkulu disimpan dalam `OrderedDict`, kemudian dikonversi menjadi dictionary berindeks numerik:

```python
{
  0: {"name": "Rektorat", "lon": ..., "lat": ...},
  1: {"name": "Perpustakaan", "lon": ..., "lat": ...},
  ...
}
```

📍 **Total lokasi:** 47

Ini mempermudah pemetaan node dalam algoritma graf.

---

### 4. 🚀 Algoritma Floyd-Warshall
Digunakan untuk menghitung **jalur terpendek antar semua pasangan node** dalam graf berarah berbobot (gedung-gedung di UNIB).

✨ **Langkah-langkah Utama:**
1. Inisialisasi matriks `dist` dan `next_node` berdasarkan jarak antar node.
2. Terapkan algoritma Floyd-Warshall:
   ```python
   for k in range(n):
       for i in range(n):
           for j in range(n):
               if dist[i][j] > dist[i][k] + dist[k][j]:
                   dist[i][j] = dist[i][k] + dist[k][j]
                   next_node[i][j] = next_node[i][k]
   ```
3. Perbarui jalur saat ditemukan rute yang lebih pendek.

📈 **Kompleksitas:**
- **Waktu:** `O(n³)`
- **Memori:** `O(n²)`

📌 **Cocok untuk graf berukuran kecil–menengah (≤ 100 node).**

🧭 **Catatan:**
- Cocok untuk sistem navigasi peta kampus.
- Didukung dengan data lokasi nyata (latitude & longitude).

---

### 5. Fungsi `reconstruct_path`
Membangun kembali rute terpendek dari node asal ke tujuan berdasarkan matriks `next_node`.

⚙️ **Kompleksitas Waktu:** `O(n)` (kasus terburuk)

---

### 6. 📍 Visualisasi Peta dengan Folium
- Pusat peta: Gedung **Rektorat**
- Menampilkan:
  - Marker tiap gedung
  - Jalur/rute antar node hasil algoritma

📷 **Contoh Visualisasi:**

![Image](https://github.com/user-attachments/assets/6adae20c-1ab9-4971-ac1d-858381b92f20)

---

### 💡 Catatan Tambahan
- Akses ke node (gerbang) **dibatasi secara dinamis berdasarkan waktu nyata**.
- Visualisasi mendukung pengguna mencari **rute tercepat antar gedung** di kampus.
- Cocok untuk pengembangan fitur **navigasi kampus dan simulasi waktu nyata**.

