import numpy as np
import itertools

# Definition der Knoten und der Distanzmatrix
nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
matrix = np.array([
    [0, 1, 1, 1, 0, 0, 1, 0, 0, 1],  # A
    [1, 0, 0, 0, 6, 2, 8, 0, 0, 0],  # B
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # C
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0],  # D
    [0, 6, 0, 0, 0, 1, 0, 13, 0, 0], # E
    [0, 2, 0, 0, 1, 0, 0, 0, 0, 0],  # F
    [1, 8, 1, 0, 0, 0, 0, 0, 2, 0],  # G
    [0, 0, 0, 1, 13, 0, 0, 0, 9, 0], # H
    [0, 0, 0, 0, 0, 0, 2, 9, 0, 2],  # I
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 0]   # J
])

# Einsatzstellen und Versorgungspunkte
einsatzstellen = {"D", "F", "I", "J"}
versorgungspunkte = {"A", "H"}

# Berechne die kürzesten Wege zwischen allen Knoten mit dem Floyd-Warshall-Algorithmus
def floyd_warshall(matrix):
    dist = np.copy(matrix)
    n = len(matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i, k] > 0 and dist[k, j] > 0:
                    if dist[i, j] == 0 or dist[i, j] > dist[i, k] + dist[k, j]:
                        dist[i, j] = dist[i, k] + dist[k, j]
    return dist

dist_matrix = floyd_warshall(matrix)

# Funktion zur Berechnung der durchschnittlichen Entfernung zu den Versorgungspunkten
def avg_distance_to_supply_points(einsatzstellen, versorgungspunkte, nodes, dist_matrix):
    total_distance = 0
    for einsatzstelle in einsatzstellen:
        min_distance = float('inf')
        for versorgungspunkt in versorgungspunkte:
            i = nodes.index(einsatzstelle)
            j = nodes.index(versorgungspunkt)
            if dist_matrix[i, j] > 0 and dist_matrix[i, j] < min_distance:
                min_distance = dist_matrix[i, j]
        total_distance += min_distance
    return total_distance / len(einsatzstellen)

# Funktionsaufruf mit gegebener Einsatzstellen und Versorgungspunkte
avg_dist = avg_distance_to_supply_points(einsatzstellen, versorgungspunkte, nodes, dist_matrix)
print(f"Durchschnittliche Entfernung zu den Versorgungspunkten: {avg_dist:.2f}")

# Optional: Bestimmen Sie die optimalen zusätzlichen Versorgungspunkte
def find_optimal_supply_points(einsatzstellen, versorgungspunkte, nodes, dist_matrix, k):
    best_supply_points = None
    best_avg_distance = float('inf')
    potential_points = set(nodes) - einsatzstellen - versorgungspunkte
    for new_supply_points in itertools.combinations(potential_points, k):
        current_supply_points = versorgungspunkte.union(new_supply_points)
        avg_distance = avg_distance_to_supply_points(einsatzstellen, current_supply_points, nodes, dist_matrix)
        if avg_distance < best_avg_distance:
            best_avg_distance = avg_distance
            best_supply_points = current_supply_points
    return best_supply_points, best_avg_distance

# Beispiel: Finde 2 zusätzliche Versorgungspunkte
additional_points = 2
optimal_supply_points, optimal_avg_distance = find_optimal_supply_points(einsatzstellen, versorgungspunkte, nodes, dist_matrix, additional_points)
print(f"Optimale Versorgungspunkte: {optimal_supply_points}")
print(f"Optimale durchschnittliche Entfernung: {optimal_avg_distance:.2f}")