from datetime import datetime
import pytz

def get_gate_access(now=None):
    if now is None:
        now = datetime.now(pytz.timezone("Asia/Jakarta"))

    day = now.strftime("%A")
    hour = now.hour

    access = {
        "gate_in_behind_left": False,
        "gate_in_behind_right": False,
        "gate_out_behind": False,
        "gate_in_rektorat": True,
    }

    if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] and 7 <= hour < 18:
        access["gate_in_behind_left"] = True
        access["gate_in_behind_right"] = True
        access["gate_out_behind"] = True
    else:
        access["gate_in_behind_left"] = True
        access["gate_in_behind_right"] = False
        access["gate_out_behind"] = False

    return access


import folium
import numpy as np
import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
from collections import OrderedDict
from datetime import datetime, time
import pytz

# Constants
AVERAGE_WALKING_SPEED = 1.4  # meters per second (approx 5 km/h)

class GateController:
    def __init__(self):
        self.back_gate_open_hours = (time(7, 0), time(18, 0))
        self.back_exit_only_hours = (time(6, 0), time(18, 0))
        
    def is_weekday(self, weekday):
        return 0 <= weekday <= 4  # Monday-Friday
        
    def is_between(self, check_time, time_range):
        start, end = time_range
        return start <= check_time <= end
    
    def check_back_gate_access(self, current_time):
        if self.is_weekday(current_time.weekday()):
            return self.is_between(current_time.time(), self.back_gate_open_hours)
        return False
    
    def check_back_exit_access(self, current_time):
        return self.is_between(current_time.time(), self.back_exit_only_hours)
    
    def check_side_gates_access(self, current_time):
        current_time = current_time.time()
        if time(7, 0) <= current_time <= time(18, 0):
            return {
                'left_gate': {'entry': True, 'directions': ['rektorat', 'straight', 'right_turn'], 'exit': False},
                'right_gate': {'entry': True, 'directions': ['gsg'], 'straight': False, 'exit': False}
            }
        else:
            return {
                'left_gate': {'entry': True, 'directions': ['rektorat', 'straight', 'right_turn'], 'exit': False},
                'right_gate': {'entry': False, 'exit': True, 'directions': []}
            }

# Updated UNIB building locations
unib_buildings = OrderedDict([
    ("Rektorat", [102.27231460986346, -3.7590495172423495]),
    ("Masjid Baitul Hikmah", [102.27600666694858, -3.758945132312725]),
    ("Perpustakaan", [102.27485462111163, -3.756806076798016]),
    ("Gerbang Masuk Belakang", [102.27521569504947, -3.759614988399855]),
    ("Gerbang Masuk Depan", [102.26779832443637, -3.7597051616151904]),
    ("GB 1", [102.27372095056845, -3.7568032921655625]),
    ("GB 2", [102.274037554275, -3.7578575751002457]),
    ("GB 3 & 4", [102.27664495427499, -3.7560850630710587]),
    ("GB 5", [102.27650213893024, -3.7553463918453187]),
    ("LPTIK", [102.27501541748192, -3.7585034389347047]),
    ("GSG", [102.27655797563433, -3.757536160753844]),
    ("Dekanat Teknik", [102.27670099113969, -3.7584642603667104]),
    ("LAB Teknik", [102.27690975882886, -3.758891053967651]),
    ("LAB Terpadu Teknik", [102.27735016612473, -3.7585892834199925]),
    ("Stadion Unib", [102.27817155070424, -3.7576442412116946]),
    ("Gedung FKIP", [102.27746551161644, -3.756364599659421]),
    ("Fakultas Kedokteran", [102.27803206102215, -3.7551337561874982]),
    ("Sekretariat UKM", [102.2757012915378, -3.756636058655066]),
    ("Dekanat FMIPA", [102.2747136045303, -3.756028855847586]),
    ("Sekretariat BEM FMIPA", [102.27496036775979, -3.75578529907203]),
    ("Gedung Fisika", [102.27372386940291, -3.7562055013818023]),
    ("Ruang Baca Pertanian", [102.27283662942735, -3.7571162998364276]),
    ("LAB Agronomi", [102.27271362771398, -3.7570165757307543]),
    ("GLT", [102.27191958168342, -3.75809920273443]),
    ("Masjid Darul Ulum", [102.2675868394383, -3.757278224804399]),
    ("LAB Ilmu Tanah", [102.27012662561205, -3.7592326497010897]),
    ("Dekanat Pertanian", [102.26921964529129, -3.759336210212976]),
    ("Dekanat Hukum", [102.26844172291675, -3.760583199392584]),
    ("LAB Hukum", [102.26867339480454, -3.7602660084096446]),
    ("Fakultas FEB", [102.26862389169713, -3.7617198090691164]),
    ("Magister Ilmu Ekonomi", [102.2686381084575, -3.7624574876125974]),
    ("Jurusan Ekonomi Pembangunan", [102.26894613829127, -3.7617576387695197]),
    ("UPT Bing", [102.27036307553568, -3.7607740664372096]),
    ("Gedung J", [102.2697707104651, -3.76030119474263]),
    ("Gedung K", [102.26990813916206, -3.761142906184093]),
    ("Gedung C", [102.26791776641025, -3.7590706965117002]),
    ("Danau Unib", [102.27306446726114, -3.758445851629117]),
    ("Mushola Shelter", [102.27361705847183, -3.7576982064708235]),
    ("Dekanat FISIP", [102.27417328919393, -3.7590310709254973]),
    ("Dekanat FKIP", [102.27504444750583, -3.75753414150989]),
    ("Gerbang Keluar Depan", [102.26666968496903, -3.758831903679123]),
    ("Gerbang Keluar Belakang", [102.27618970824084, -3.7592446156990227]),
    ("Asrama PGSD", [102.27160069043919, -3.7617418863983096]),
    ("S2 Matematika", [102.27543890078353, -3.7580570001381477]),
    ("Klinik Pratama Unib", [102.2717675810424, -3.7614596037430554]),
    ("Sekretariat Teknik", [102.27733334828312, -3.7581980275566127]),
     ("Gerbang Masuk Rektorat", [102.27268704582688, -3.760605072804902])
])

# Convert to format: {index: {"name": name, "lon": lon, "lat": lat}}
unib_buildings = {idx: {"name": name, "lon": coords[0], "lat": coords[1]} 
                 for idx, (name, coords) in enumerate(unib_buildings.items())}

# Floyd-Warshall Algorithm
def floyd_warshall(graph):
    n = len(graph)
    dist = np.copy(graph)
    next_node = np.zeros((n, n), dtype=int)
    
    for i in range(n):
        for j in range(n):
            if i == j:
                next_node[i][j] = -1
            elif graph[i][j] != float('inf'):
                next_node[i][j] = j
            else:
                next_node[i][j] = -1
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
    
    return dist, next_node

def reconstruct_path(next_node, start, end):
    if next_node[start][end] == -1:
        return []
    
    path = [start]
    while start != end:
        start = next_node[start][end]
        path.append(start)
    
    return path

# Create adjacency matrix with distances
access = get_gate_access()

gate_names = {
    "Gerbang Masuk Belakang": None,
    "Gerbang Keluar Belakang": None,
    "Gerbang Masuk Rektorat": None
}

for idx, data in unib_buildings.items():
    if data['name'] in gate_names:
        gate_names[data['name']] = idx

n = len(unib_buildings)
graph = np.full((n, n), float('inf'))
np.fill_diagonal(graph, 0)

for i in range(n):
    for j in range(n):
        if i != j:
            name_i = unib_buildings[i]["name"]
            name_j = unib_buildings[j]["name"]

            if gate_names["Gerbang Masuk Belakang"] in [i, j]:
                if not (access["gate_in_behind_left"] or access["gate_in_behind_right"]):
                    continue
            if gate_names["Gerbang Keluar Belakang"] in [i, j]:
                if not access["gate_out_behind"]:
                    continue
            if gate_names["Gerbang Masuk Rektorat"] in [i, j]:
                if not access["gate_in_rektorat"]:
                    continue

            coord1 = (unib_buildings[i]["lat"], unib_buildings[i]["lon"])
            coord2 = (unib_buildings[j]["lat"], unib_buildings[j]["lon"])
            distance = geodesic(coord1, coord2).meters
            graph[i][j] = distance

# Calculate shortest paths
distances, next_node = floyd_warshall(graph)

# Enhanced Visualization with Folium
def visualize_unib_map(building_indices=None, path_coords=None, zoom_start=16):
    unib_center = [-3.7590495172423495, 102.27231460986346]  # Rektorat as center
    m = folium.Map(location=unib_center, zoom_start=zoom_start)
    
    gate_info = """
    <div style="position: fixed; bottom: 50px; left: 50px; width: 300px; height: 150px; 
                background-color: white; padding: 10px; z-index: 9999; border-radius: 5px;
                box-shadow: 0 0 5px rgba(0,0,0,0.5);">
        <h4>Gate Access Rules:</h4>
        <ul style="font-size: 12px; padding-left: 15px;">
            <li>Back Gate: Mon-Fri 07:00-18:00</li>
            <li>Back Exit: 06:00-18:00</li>
            <li>Side Gates: Different rules apply</li>
        </ul>
    </div>
    """
    m.get_root().html.add_child(folium.Element(gate_info))
    
    # Add all buildings as markers with custom icons
    for idx, building in unib_buildings.items():
        if "Gerbang" in building["name"]:
            icon_color = 'green'
            icon_type = 'sign'
        elif "LAB" in building["name"] or "Laboratorium" in building["name"]:
            icon_color = 'orange'
            icon_type = 'wrench'
        elif "Masjid" in building["name"] or "Mushola" in building["name"]:
            icon_color = 'black'
            icon_type = 'star'
        elif "Dekanat" in building["name"] or "Fakultas" in building["name"]:
            icon_color = 'blue'
            icon_type = 'university'
        else:
            icon_color = 'red'
            icon_type = 'home'
        
        is_in_path = building_indices and idx in building_indices
        icon_color = 'purple' if is_in_path else icon_color
        
        folium.Marker(
            location=[building["lat"], building["lon"]],
            popup=f"<b>{building['name']}</b>",
            tooltip=building["name"],
            icon=folium.Icon(color=icon_color, icon=icon_type, prefix='fa')
        ).add_to(m)
    
    # Add path if provided with improved styling
    if path_coords and len(path_coords) > 1:
        for i in range(len(path_coords)-1):
            folium.PolyLine(
                locations=[path_coords[i], path_coords[i+1]],
                color='red',
                weight=5,
                opacity=0.8,
                dash_array='10',
                popup=f"Segment {i+1}"
            ).add_to(m)
            
            mid_lat = (path_coords[i][0] + path_coords[i+1][0]) / 2
            mid_lon = (path_coords[i][1] + path_coords[i+1][1]) / 2
            
            folium.CircleMarker(
                location=[mid_lat, mid_lon],
                radius=3,
                color='darkred',
                fill=True,
                fill_opacity=1.0
            ).add_to(m)
        
        folium.Marker(
            location=path_coords[0],
            popup="<b>Start</b>",
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m)
        
        folium.Marker(
            location=path_coords[-1],
            popup="<b>Destination</b>",
            icon=folium.Icon(color='darkred', icon='stop', prefix='fa')
        ).add_to(m)
    
    folium.Circle(
        location=[-3.758, 102.272],
        radius=300,
        color='#3186cc',
        fill=True,
        fill_color='#3186cc',
        opacity=0.2,
        popup="UNIB Main Campus Area"
    ).add_to(m)
    
    return m

# Initialize gate controller
gate_controller = GateController()

# Enhanced OSMnx Integration
def get_realistic_path(start_coord, end_coord, current_time=None):
    try:
        if current_time is None:
            current_time = datetime.now()
            
        start_name = next((b['name'] for b in unib_buildings.values() 
                        if (b['lat'], b['lon']) == (start_coord[0], start_coord[1])), None)
        end_name = next((b['name'] for b in unib_buildings.values() 
                      if (b['lat'], b['lon']) == (end_coord[0], end_coord[1])), None)
        
        if "Gerbang Masuk Belakang" in [start_name, end_name]:
            if not gate_controller.check_back_gate_access(current_time):
                raise ValueError("Gerbang Belakang tutup (hanya buka Senin-Jumat 07:00-18:00)")
        
        if "Gerbang Keluar Belakang" in [start_name, end_name]:
            if not gate_controller.check_back_exit_access(current_time):
                raise ValueError("Gerbang Keluar Belakang tutup (hanya buka 06:00-18:00)")
        
        center_point = ((start_coord[0] + end_coord[0])/2, (start_coord[1] + end_coord[1])/2)
        dist = geodesic((start_coord[0], start_coord[1]), (end_coord[0], end_coord[1])).meters * 2
        dist = max(dist, 1500)
        
        G = ox.graph_from_point(center_point, network_type='walk', dist=dist)
        
        if len(G.nodes) < 20:
            print("Warning: Network has few nodes, downloading larger area")
            G = ox.graph_from_point(center_point, network_type='all', dist=dist*2)
        
        start_node = ox.distance.nearest_nodes(G, X=[start_coord[1]], Y=[start_coord[0]])[0]
        end_node = ox.distance.nearest_nodes(G, X=[end_coord[1]], Y=[end_coord[0]])[0]
        
        route = nx.shortest_path(G, start_node, end_node, weight='length')
        
        route_coords = []
        route_coords.append([start_coord[0], start_coord[1]])
        
        for node in route:
            point = G.nodes[node]
            route_coords.append([point['y'], point['x']])
        
        if route_coords[-1] != [end_coord[0], end_coord[1]]:
            route_coords.append([end_coord[0], end_coord[1]])
        
        return route_coords
    
    except nx.NetworkXNoPath:
        print("Tidak ada jalur yang ditemukan. Menggunakan jalur alternatif.")
        points = 10
        lat_step = (end_coord[0] - start_coord[0]) / points
        lon_step = (end_coord[1] - start_coord[1]) / points
        
        route_coords = []
        for i in range(points + 1):
            route_coords.append([start_coord[0] + i * lat_step, start_coord[1] + i * lon_step])
        
        return route_coords
    
    except Exception as e:
        print(f"OSMnx error: {e}")
        return [[start_coord[0], start_coord[1]], [end_coord[0], end_coord[1]]]

# Enhanced Route Instructions with time estimation
def get_route_instructions(route_coords):
    instructions = []
    if len(route_coords) < 2:
        return ["You have arrived at your destination"]
    
    total_distance = 0
    total_time = 0  # In seconds
    
    for i in range(1, len(route_coords)):
        prev = route_coords[i-1]
        curr = route_coords[i]
        
        segment_dist = geodesic(prev, curr).meters
        total_distance += segment_dist
        
        segment_time = segment_dist / AVERAGE_WALKING_SPEED
        total_time += segment_time
        
        lat1, lon1 = np.radians(prev[0]), np.radians(prev[1])
        lat2, lon2 = np.radians(curr[0]), np.radians(curr[1])
        
        dlon = lon2 - lon1
        x = np.sin(dlon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
        bearing = np.degrees(np.arctan2(x, y))
        bearing = (bearing + 360) % 360
        
        directions = [
            (0, 22.5, "north"),
            (22.5, 67.5, "northeast"),
            (67.5, 112.5, "east"),
            (112.5, 157.5, "southeast"),
            (157.5, 202.5, "south"),
            (202.5, 247.5, "southwest"),
            (247.5, 292.5, "west"),
            (292.5, 337.5, "northwest"),
            (337.5, 360, "north")
        ]
        
        direction = next((d for (start, end, d) in directions if start <= bearing < end), "north")
        
        instructions.append({
            'step': i,
            'direction': direction,
            'distance': segment_dist,
            'total_distance': total_distance,
            'time': segment_time,
            'total_time': total_time,
            'location': curr
        })
    
    return instructions

def print_instructions(instructions):
    print("\n📌 Route Instructions:")
    for i, inst in enumerate(instructions, 1):
        print(f"{i}. Head {inst['direction'].upper()} for {inst['distance']:.1f}m "
              f"(about {inst['time']/60:.1f} mins) - "
              f"Total: {inst['total_distance']:.1f}m")
    
    if instructions:
        total_time_minutes = instructions[-1]['total_time'] / 60
        print(f"\n🏁 Total distance: {instructions[-1]['total_distance']:.1f} meters")
        print(f"⏱️ Estimated  time: {total_time_minutes:.1f} minutes")

# Example Usage with User Interface
def main():
    print("🏫 UNIB Shortest Path Finder")
    print("===========================\n")
    
    print("Available Buildings:")
    for idx, building in unib_buildings.items():
        print(f"{idx:2d}. {building['name']}")
    
    try:
        start_idx = int(input("\nEnter starting building number: "))
        end_idx = int(input("Enter destination building number: "))
        
        while True:
            time_input = input("Enter time in HH:MM format (or press Enter for current time): ")
            if not time_input:
                current_time = datetime.now()
                break
            try:
                current_time = datetime.strptime(time_input, "%H:%M")
                current_time = current_time.replace(
                    year=datetime.now().year,
                    month=datetime.now().month,
                    day=datetime.now().day
                )
                break
            except ValueError:
                print("Invalid time format! Please use HH:MM or press Enter")
        
        if start_idx not in unib_buildings or end_idx not in unib_buildings:
            print("Invalid building numbers!")
            return
        
        start_building = unib_buildings[start_idx]
        end_building = unib_buildings[end_idx]
        
        print(f"\nCalculating path from {start_building['name']} to {end_building['name']} at {current_time.strftime('%H:%M')}...")
        
        abstract_path = reconstruct_path(next_node, start_idx, end_idx)
        
        if not abstract_path:
            print("No path exists between the selected buildings")
            return
        
        print("\nShortest path buildings:")
        for idx in abstract_path:
            print(f"- {unib_buildings[idx]['name']}")
        
        start_coord = (start_building["lat"], start_building["lon"])
        end_coord = (end_building["lat"], end_building["lon"])
        
        realistic_path = get_realistic_path(start_coord, end_coord, current_time)
        
        # Calculate total distance and time
        if realistic_path and len(realistic_path) > 1:
            total_distance = sum(geodesic(realistic_path[i], realistic_path[i+1]).meters 
                             for i in range(len(realistic_path)-1))
            estimated_time = total_distance / AVERAGE_WALKING_SPEED / 60  # In minutes
            
            print(f"\n📏 Total distance: {total_distance:.1f} meters")
            print(f"⏱️ Estimated  time: {estimated_time:.1f} minutes")
            
            instructions = get_route_instructions(realistic_path)
            print_instructions(instructions)
        else:
            print("\n⚠️ Could not generate detailed path instructions")
        
        m = visualize_unib_map(abstract_path, realistic_path)
        map_file = "unib_path.html"
        m.save(map_file)
        print(f"\n🗺️ Map saved to '{map_file}'. Open it in your browser to view the path.")
        
    except ValueError:
        print("Please enter valid numbers for building selection!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()