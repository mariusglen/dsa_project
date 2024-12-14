import os
from queue import PriorityQueue

nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

matrix = [
    [5, 1, 0, 1, 1, 0, 5, 25, 0, 17],
    [15, 8, 4, 0, 1, 10, 0, 0, 0, 34],
    [15, 0, 5, 1, 7, 0, 9, 1, 0, 0],
    [6, 4, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 9, 0, 0, 10, 0, 0, 0, 0],
    [0, 3, 0, 0, 5, 0, 0, 0, 0, 12],
    [2, 3, 9, 0, 0, 0, 0, 7, 10, 0],
    [8, 6, 15, 2, 2, 0, 0, 0, 0, 0],
    [0, 13, 0, 0, 0, 0, 17, 34, 3, 0],
    [9, 0, 3, 0, 0, 0, 0, 0, 23, 0]
]

kapazitaet_strassen = [
    [0, 90, 0, 0, 80, 0, 80, 76, 0, 61],
    [71, 89, 0, 0, 76, 124, 0, 0, 0, 105],
    [122, 0, 116, 95, 54, 0, 63, 142, 0, 0],
    [59, 79, 130, 0, 60, 0, 0, 0, 0, 0],
    [0, 95, 52, 0, 0, 74, 0, 0, 0, 0],
    [0, 127, 0, 0, 75, 0, 0, 0, 0, 111],
    [78, 0, 0, 0, 0, 0, 0, 82, 144, 0],
    [61, 115, 0, 150, 87, 0, 0, 0, 0, 0],
    [0, 148, 0, 0, 0, 0, 52, 102, 107, 0],
    [84, 0, 131, 0, 0, 0, 0, 0, 84, 0],
]

def create_matrix_unpass_strassen(matrix, kapazitaet_strassen):
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    matrix_unpass_strassen = [[0] * num_cols for _ in range(num_rows)]
    
    for i in range(num_rows):
        for j in range(num_cols):
            if kapazitaet_strassen[i][j] != 0:
                matrix_unpass_strassen[i][j] = matrix[i][j]
    
    return matrix_unpass_strassen

matrix_unpass_strassen = create_matrix_unpass_strassen(matrix, kapazitaet_strassen)

def print_matrix(matrix, nodes):
    print("  " + " ".join(nodes))
    for i, row in enumerate(matrix):
        print(nodes[i] + " " + " ".join(map(str, row)))

# folgende Knoten sind Sammelpunkte:
sammelpunkte = ["D", "F"]

# folgende Knoten sind Notlager:
notlager = ["I", "J"]

busse = 10
kapazitaet_bus = 50

population_to_evacuate = 1000

personen_sammelpunkte = {
    "D": 100,
    "F": 400
}

kapazitaet_notlager = {
    "I": 200,
    "J": 300
}

# Dijkstra Algorithmus zur Berechnung des kürzesten Weges zwischen zwei Knoten , return Pfad aller knoten und die gewichte addiren
# Modified Dijkstra's Algorithm to include all visited nodes
def dijkstra_with_visited(nodes, matrix, start, end):
    num_nodes = len(nodes)
    distances = {node: float('inf') for node in range(num_nodes)}
    previous = {node: None for node in range(num_nodes)}
    visited_nodes = []

    distances[nodes.index(start)] = 0
    pq = PriorityQueue()
    pq.put((0, nodes.index(start)))

    while not pq.empty():
        current_distance, current_node = pq.get()

        if current_node not in visited_nodes:
            visited_nodes.append(nodes[current_node])

        # Skip processing if this is not the shortest path to the node
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor in range(num_nodes):
            weight = matrix[current_node][neighbor]
            if weight > 0:  # There is a connection
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    pq.put((distance, neighbor))

    # Reconstruct the path
    path = []
    current = nodes.index(end)
    total_weight = 0
    while current is not None:
        path.append(nodes[current])
        next_node = previous[current]
        if next_node is not None:
            total_weight += matrix[next_node][current]
        current = next_node

    return list(reversed(path)), total_weight, visited_nodes

# calculate the shortest path from personen_sammelpunkte to notlager
def sammelpunkte_to_notlager(sammelpunkte, notlager):
    shortest_paths = {}
    for sammelpunkt in sammelpunkte:
        for lager in notlager:
            path, weight, visited = dijkstra_with_visited(nodes, matrix_unpass_strassen, sammelpunkt, lager)
            shortest_paths[(sammelpunkt, lager)] = (path, weight, visited)
    return shortest_paths

shortest_paths = sammelpunkte_to_notlager(sammelpunkte, notlager)

os.system('clear')

# Output results from personen_sammelpunkte to notlager as print, checks which calculation is the shortest

# Output the shortest path from each personen_sammelpunkte to notlager
print("Shortest path from each Sammelpunkt to Notlager:")
for (sammelpunkt, lager), (path, weight, visited) in shortest_paths.items():
    print(f"From {sammelpunkt} to {lager}:")
    print(f"Path: {' -> '.join(path)}")
    print(f"Total weight: {weight}")
    print()

# berechnen ob die kapazitat der busse ausreicht um alle personen zu evakuieren
def calculate_bus_capacity(busse, kapazitaet_bus, personen_sammelpunkte):
    total_capacity = busse * kapazitaet_bus
    total_personen = sum(personen_sammelpunkte.values())
    return total_capacity >= total_personen

# berechenen ob die Kapazität der Notlager ausreicht um alle Personen aufzunehmen
def calculate_notlager_capacity(kapazitaet_notlager, personen_sammelpunkte):
    total_personen = sum(personen_sammelpunkte.values())
    total_capacity = sum(kapazitaet_notlager.values())
    return total_capacity >= total_personen


# Output the results of the calculations
print("Results:")
print(f"Bus capacity is sufficient: {calculate_bus_capacity(busse, kapazitaet_bus, personen_sammelpunkte)}")
print(f"Notlager capacity is sufficient: {calculate_notlager_capacity(kapazitaet_notlager, personen_sammelpunkte)}")

# Output the new matrix
print("Matrix with unpassable roads:")
print_matrix(matrix_unpass_strassen, nodes)


