import tkinter as tk
from tkinter import ttk, messagebox
import math

# Kecepatan dalam meter per detik
SPEEDS = {
    'jalan_kaki': 1.11,  # 4 km/jam
    'motor': 16.67,      # 60 km/jam
    'mobil': 11.11       # 40 km/jam
}

# Data graf berbentuk adjacency list dengan jarak (dalam meter)
graph = {
    "Pintu Gerbang Depan": [("Pasca Hukum", 200)],
    "Pasca Hukum": [("Pintu Gerbang Depan", 200), ("MAKSI (Ged C)", 400), ("Gedung F", 500)],
    "MAKSI (Ged C)": [("Pasca Hukum", 400), ("Ged. B", 300)],
    "Ged. B": [("MAKSI (Ged C)", 300), ("Ged. A", 200)],
    "Ged. A": [("Ged. B", 200), ("Masjid UNIB", 100)],
    "Masjid UNIB": [("Ged. A", 100)],
    "Gedung F": [("Pasca Hukum", 500), ("Lab. Hukum", 300), ("Ged. I", 200), ("Ged. J", 200), ("Dekanat Pertanian", 200)],
    "Lab. Hukum": [("Gedung F", 100)],
    "Ged. I": [("Gedung F", 200), ("Ged. MM", 150)],
    "Ged. MM": [("Ged. I", 200), ("Ged. MPP", 200)],
    "Ged. MPP": [("Ged. MM", 100), ("Ged. UPT B. Inggris", 100)],
    "Ged. J": [("Gedung F", 200), ("Ged. UPT B. Inggris", 100)],
    "Ged. UPT B. Inggris": [("Ged. J", 100), ("REKTORAT", 150)],
    "Dekanat Pertanian": [("Gedung F", 200), ("Ged. T", 150)],
    "Ged. T": [("Dekanat Pertanian", 150), ("Ged. V", 150)],
    "Ged. V": [("Ged. T", 150), ("Ged. Renper", 100), ("REKTORAT", 150)],
    "Ged. Renper": [("Ged. V", 100), ("Lab. Agro", 100)],
    "Lab. Agro": [("Ged. Renper", 100), ("Ged. Basic Sains", 200)],
    "Ged. Basic Sains": [("Lab. Agro", 200), ("GKB I", 150), ("Dekanat MIPA", 100)],
    "Dekanat MIPA": [("Ged. Basic Sains", 100)],
    "UPT Puskom": [("Ged. V", 150), ("GKB I", 100)],
    "REKTORAT": [("Ged. UPT B. Inggris", 150), ("Ged. V", 150), ("Dekanat FISIP", 150)],
    "Dekanat FISIP": [("REKTORAT", 150), ("Pintu Gerbang", 200), ("GKB II", 100)],
    "Pintu Gerbang": [("Dekanat FISIP", 200), ("Dekanat Teknik", 300)],
    "Dekanat Teknik": [("Pintu Gerbang", 300), ("Gedung Serba Guna (GSG)", 200)],
    "Gedung Serba Guna (GSG)": [("Dekanat Teknik", 200), ("Stadion Olahraga", 200), ("GKB III", 200), ("Dekanat FKIP", 100)],
    "GKB I": [("UPT Puskom", 100), ("GKB II", 100), ("Ged. Basic Sains", 150)],
    "GKB II": [("GKB I", 100), ("Dekanat FKIP", 100), ("Dekanat FISIP", 100)],
    "Dekanat FKIP": [("GKB II", 100), ("Gedung Serba Guna (GSG)", 100)],
    "GKB III": [("Gedung Serba Guna (GSG)", 200)],
    "PSPD": [("GKB V", 200), ("Stadion Olahraga", 150)],
    "PKM": [("GKB V", 200)],
    "GKB V": [("PKM", 200), ("PSPD", 200)],
    "Stadion Olahraga": [("GKB III", 200), ("PSPD", 150)]
}

# Inisialisasi list node
nodes = list(graph.keys())
n = len(nodes)
index = {node: i for i, node in enumerate(nodes)}

# Matriks jarak awal
dist = [[math.inf] * n for _ in range(n)]
next_node = [[None] * n for _ in range(n)]

for u in nodes:
    for v, w in graph[u]:
        i, j = index[u], index[v]
        dist[i][j] = w
        next_node[i][j] = v
    dist[index[u]][index[u]] = 0

# Floyd-Warshall
for k in range(n):
    for i in range(n):
        for j in range(n):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                next_node[i][j] = next_node[i][k]

# Fungsi untuk membentuk jalur dari node i ke j

def construct_path(i, j):
    if next_node[i][j] is None:
        return None
    path = [nodes[i]]
    while i != j:
        i = index[next_node[i][j]]
        path.append(nodes[i])
    return path

# GUI
root = tk.Tk()
root.title("Pencarian Jalur - Floyd Warshall")

start_combobox = ttk.Combobox(root, values=nodes)
goal_combobox = ttk.Combobox(root, values=nodes)
mode_combobox = ttk.Combobox(root, values=list(SPEEDS.keys()))

start_combobox.pack(padx=10, pady=5)
goal_combobox.pack(padx=10, pady=5)
mode_combobox.pack(padx=10, pady=5)

result_label = tk.Label(root, text="", justify="left")
result_label.pack(padx=10, pady=10)


def find_floyd_path():
    start = start_combobox.get()
    goal = goal_combobox.get()
    mode = mode_combobox.get()

    if start not in index or goal not in index or mode not in SPEEDS:
        messagebox.showerror("Error", "Pastikan semua pilihan telah diisi dengan benar.")
        return

    i, j = index[start], index[goal]
    path = construct_path(i, j)
    if not path:
        result_label.config(text="Tidak ada jalur yang tersedia.")
        return

    distance = dist[i][j]  # dalam meter
    speed = SPEEDS[mode]  # dalam m/s
    time = distance / speed  # dalam detik

    menit = int(time // 60)
    detik = int(time % 60)

    result_label.config(
        text=f"Jalur: {' -> '.join(path)}\nTotal Jarak: {distance} meter\nEstimasi Waktu ({mode}): {menit} menit {detik} detik"
    )

search_button = tk.Button(root, text="Cari Jalur", command=find_floyd_path)
search_button.pack(pady=10)

root.mainloop()
