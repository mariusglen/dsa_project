import os
from queue import PriorityQueue
from collections import defaultdict

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
            if kapazitaet_strassen[i][j] == 0: # Markiere Straßen als unpassierbar wenn Kapazität == 0
                matrix_unpass_strassen[i][j] = float('inf')
            else:
                matrix_unpass_strassen[i][j] = matrix[i][j]
    
    return matrix_unpass_strassen


matrix_unpass_strassen = create_matrix_unpass_strassen(matrix, kapazitaet_strassen)

def print_matrix(matrix, nodes):
    print("  " + " ".join(nodes))
    for i, row in enumerate(matrix):
        print(nodes[i] + " " + " ".join(map(lambda x: str(x) if x != float('inf') else 'inf', row)))

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
def dijkstra(nodes, matrix, start, end):
    num_nodes = len(nodes)
    distances = {node: float('inf') for node in range(num_nodes)}
    previous = {node: None for node in range(num_nodes)}

    distances[nodes.index(start)] = 0
    pq = PriorityQueue()
    pq.put((0, nodes.index(start)))

    while not pq.empty():
        current_distance, current_node = pq.get()

        # Skip processing if this is not the shortest path to the node
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor in range(num_nodes):
            weight = matrix[current_node][neighbor]
            if weight < float('inf'):  # There is a connection, and it's not unpassable
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

    if distances[nodes.index(end)] == float('inf'):
         return None, float('inf')  # No path found
    
    return list(reversed(path)), total_weight


# calculate the shortest path from personen_sammelpunkte to notlager
def sammelpunkte_to_notlager(sammelpunkte, notlager):
    shortest_paths = {}
    for sammelpunkt in sammelpunkte:
        for lager in notlager:
            path, weight = dijkstra(nodes, matrix_unpass_strassen, sammelpunkt, lager)
            if path:
              shortest_paths[(sammelpunkt, lager)] = (path, weight)
    return shortest_paths

shortest_paths = sammelpunkte_to_notlager(sammelpunkte, notlager)

# Funktion zum Zuordnen von Personen zu Routen
def assign_people_to_routes(personen_sammelpunkte, shortest_paths, kapazitaet_strassen, busse, kapazitaet_bus, kapazitaet_notlager):
  
    route_assignments = defaultdict(lambda: {"personen": 0, "busse": 0}) # Track assigned people per route
    notlager_assignments = defaultdict(lambda: 0) # Track assigned people per Notlager
    remaining_people = personen_sammelpunkte.copy() # Remaining people to assign

    total_bus_capacity = busse * kapazitaet_bus

    # Zuerst versuche, die Personen den Routen zuzuweisen, wenn es eine Route gibt
    for sammelpunkt, personen in personen_sammelpunkte.items():
        assigned_personen = 0
        for (start, end), (path, weight) in shortest_paths.items():
          if start == sammelpunkt:
            if remaining_people[sammelpunkt] == 0:
                break
            
            route_key = (start,end)
            route_capacity = float('inf')
            
            # Berechne die Minimale Kapazität der Strasse auf diesem Weg
            for i in range(len(path) - 1):
              u = nodes.index(path[i])
              v = nodes.index(path[i+1])
              route_capacity = min(route_capacity,kapazitaet_strassen[u][v])
            
            # Falls die Kapazität des Weges grösser 0, wird geprüft ob es noch Busse oder Personen gibt.
            if route_capacity > 0:
                  
                  # berechne die Anzahl benötigter Busse für die Route
                  busses_required = min((personen - assigned_personen + kapazitaet_bus - 1) // kapazitaet_bus,busse - route_assignments[route_key]["busse"]) if remaining_people[sammelpunkt] != 0 else 0
                  
                  # zuweisen der Personen und Busse
                  assigned_people_for_route = min(personen - assigned_personen ,busses_required * kapazitaet_bus,route_capacity )
                  route_assignments[route_key]["personen"] += assigned_people_for_route
                  route_assignments[route_key]["busse"] += busses_required
                  assigned_personen += assigned_people_for_route
                  remaining_people[sammelpunkt] -= assigned_people_for_route
                  
                  print(f"Assigning {assigned_people_for_route} persons to route {start} -> {end} with {busses_required} busses.")
                  if remaining_people[sammelpunkt] == 0:
                    break
    
    # Falls nicht alle Personen auf Routen zugeteilt werden konnten, gebe die Rest personen aus.
    unassigned_people = sum(remaining_people.values())
    
    
    # Verteile die Personen die auf den Routen zu den Notlagern gelangen
    for (start, end), route_info in route_assignments.items():
       # Verteile die Personen zu den Notlagern
      if route_info["personen"] > 0:
          
          # zuordnen der Personen auf die Notlager
          notlager_capacity = kapazitaet_notlager[end] - notlager_assignments[end]
          assigned_people_to_notlager = min(notlager_capacity, route_info["personen"])
          notlager_assignments[end] += assigned_people_to_notlager

          route_info["personen"] -= assigned_people_to_notlager

          print(f"Assigned {assigned_people_to_notlager} from Route {start} to Notlager {end}")
    
    unassigned_to_notlager = 0
    # nicht zugeordnete Personen auf den Routen werden angezeigt
    for route, info in route_assignments.items():
      if info["personen"] > 0:
        unassigned_to_notlager += info["personen"]
        print(f"Route {route} has unassigned persons {info['personen']}")
    
    return route_assignments, notlager_assignments, unassigned_people, unassigned_to_notlager



route_assignments, notlager_assignments, unassigned_people, unassigned_to_notlager = assign_people_to_routes(personen_sammelpunkte, shortest_paths, kapazitaet_strassen, busse, kapazitaet_bus, kapazitaet_notlager)

os.system('clear')

# Output results from personen_sammelpunkte to notlager as print, checks which calculation is the shortest

# Output the shortest path from each personen_sammelpunkte to notlager
print("Shortest path from each Sammelpunkt to Notlager:")
for (sammelpunkt, lager), (path, weight) in shortest_paths.items():
    print(f"From {sammelpunkt} to {lager}:")
    print(f"Path: {' -> '.join(path)}")
    print(f"Total weight: {weight}")
    print()

# Output the results of the calculations
print("Results:")
print(f"Total unassigned people: {unassigned_people}")
print(f"Total unassigned people to Notlager: {unassigned_to_notlager}")
print(f"People assigned per route: {route_assignments}")
print(f"People assigned per notlager: {notlager_assignments}")

# Output the new matrix
print("Matrix with unpassable roads:")
print_matrix(matrix_unpass_strassen, nodes)