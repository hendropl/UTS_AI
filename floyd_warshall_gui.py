
import tkinter as tk
from tkinter import ttk, messagebox

INF = float('inf')  # Nilai tak hingga untuk inisialisasi jarak yang belum diketahui

# === Graph kampus ===
# Representasi dalam bentuk adjacency list: setiap node menyimpan daftar tuple (tetangga, jarak)
graph = {
    "Pintu Gerbang Depan": [("Pasca Hukum", 200)],
    "Pasca Hukum": [("Pintu Gerbang Depan", 200), ("MAKSI (Ged C)", 400), ("Gedung F", 500)],
    "MAKSI (Ged C)": [("Pasca Hukum", 400), ("Ged. B", 300)],
    "Ged. B": [("MAKSI (Ged C)", 300), ("Ged. A", 200)],
    "Ged. A": [("Ged. B", 200), ("Masjid UNIB", 100)],
    "Masjid UNIB": [("Ged. A", 100)],
    "Gedung F": [("Pasca Hukum", 500), ("Lab. Hukum", 300), ("Ged. I", 200), ("Ged. J", 200), ("Dekanat Pertanian", 200)],
    "Lab. Hukum": [("Gedung F", 300)],
    "Ged. I": [("Gedung F", 200), ("Ged. MM", 150)],
    "Ged. MM": [("Ged. I", 150), ("Ged. MPP", 200)],
    "Ged. MPP": [("Ged. MM", 200), ("Ged. UPT B. Inggris", 100)],
    "Ged. J": [("Gedung F", 200), ("Ged. UPT B. Inggris", 200)],
    "Ged. UPT B. Inggris": [("Ged. J", 200), ("Ged. MPP", 100), ("REKTORAT", 200)],
    "Dekanat Pertanian": [("Gedung F", 200), ("Ged. T", 200)],
    "Ged. T": [("Dekanat Pertanian", 200), ("Ged. V", 200)],
    "Ged. V": [("Ged. T", 200), ("Ged. Renper", 200), ("REKTORAT", 300)],
    "Ged. Renper": [("Ged. V", 200), ("Lab. Agro", 200)],
    "Lab. Agro": [("Ged. Renper", 200), ("Ged. Basic Sains", 200)],
    "Ged. Basic Sains": [("Lab. Agro", 200), ("GKB I", 200), ("Dekanat MIPA", 200)],
    "UPT Puskom": [("Ged. V", 200), ("GKB I", 200)],
    "REKTORAT": [("Ged. UPT B. Inggris", 200), ("Ged. V", 300), ("Dekanat FISIP", 200)],
    "Dekanat FISIP": [("REKTORAT", 200), ("Pintu Gerbang", 200), ("GKB II", 200)],
    "Pintu Gerbang": [("Dekanat FISIP", 200), ("Dekanat Teknik", 200)],
    "Dekanat Teknik": [("Pintu Gerbang", 200), ("Gedung Serba Guna (GSG)", 200)],
    "Gedung Serba Guna (GSG)": [("Dekanat Teknik", 200), ("Stadion Olahraga", 200), ("GKB III", 200), ("Dekanat FKIP", 200)],
    "GKB I": [("UPT Puskom", 200), ("GKB II", 200), ("Ged. Basic Sains", 200)],
    "GKB II": [("GKB I", 200), ("Dekanat FKIP", 200), ("Dekanat FISIP", 200)],
    "Dekanat FKIP": [("GKB II", 200), ("Gedung Serba Guna (GSG)", 200)],
    "GKB V": [("PKM", 200), ("PSPD", 200)],
    "Stadion Olahraga": [("Gedung Serba Guna (GSG)", 200), ("PSPD", 200)],
    "PKM": [("GKB V", 200)],
    "PSPD": [("GKB V", 200), ("Stadion Olahraga", 200)],
    "GKB III": [("Gedung Serba Guna (GSG)", 200)],
    "Dekanat MIPA": [("Ged. Basic Sains", 200)],
}

nodes = list(graph.keys())  # Ambil semua simpul (nama titik di kampus)

# === Floyd-Warshall Algorithm ===
def floyd_warshall(graph):
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}
    next_node = {u: {v: None for v in nodes} for u in nodes}

    for u in nodes:
        dist[u][u] = 0
        for v, w in graph[u]:
            dist[u][v] = w
            next_node[u][v] = v

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node

def reconstruct_path(u, v, next_node):
    if next_node[u][v] is None:
        return []
    path = [u]
    while u != v:
        u = next_node[u][v]
        path.append(u)
    return path

def calculate_cost(distance):
    return (distance // 10) * 1000 if distance < float('inf') else 0

def find_floyd_path():
    start = start_combobox.get()
    goal = goal_combobox.get()

    if start not in nodes or goal not in nodes:
        messagebox.showerror("Error", "Titik tidak valid.")
        return

    dist_matrix, next_matrix = floyd_warshall(graph)
    distance = dist_matrix[start][goal]
    path = reconstruct_path(start, goal, next_matrix)

    if not path:
        result_label.config(text="Tidak ada jalur yang tersedia.")
    else:
        price = calculate_cost(distance)
        result_label.config(text=f"Jalur: {' -> '.join(path)}\nTotal Jarak: {distance} meter\nTotal Biaya: {price} Rp")

# === GUI ===
root = tk.Tk()
root.title("Pencarian Jalur Kampus - Floyd-Warshall")

start_combobox = ttk.Combobox(root, values=nodes, width=50)
goal_combobox = ttk.Combobox(root, values=nodes, width=50)
start_combobox.pack(pady=5)
goal_combobox.pack(pady=5)

tk.Button(root, text="Cari Jalur Terpendek (Floyd-Warshall)", command=find_floyd_path).pack(pady=5)

result_label = tk.Label(root, text="", justify="left")
result_label.pack(pady=10)

root.mainloop()
