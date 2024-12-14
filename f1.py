import heapq
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from b1 import ungerichtet_gewichtet, nodes
graph = ungerichtet_gewichtet


def prim(graph, important_nodes):
    """
    Berechnet den Minimal Spanning Tree (MST) nur für die markierten Knoten.
    Der Graph wird als Adjazenzmatrix dargestellt, und nur die Kanten der markierten Knoten werden berücksichtigt.
    """
    n = len(graph)
    mst = []  # Liste für die Kanten des MST
    visited = [False] * n  # Knoten, die bereits im MST enthalten sind
    min_heap = [(0, important_nodes[0])]  # Startknoten mit Gewicht 0
    total_weight = 0
    prev_node = -1  # Variable, um die vorherige Kante zu speichern

    while min_heap:
        weight, node = heapq.heappop(min_heap)
        if visited[node]:
            continue
        visited[node] = True
        total_weight += weight
        
        # Wenn der Knoten nicht der Startknoten ist, füge ihn zum MST hinzu
        if prev_node != -1:
            mst.append((prev_node, node, weight))
        
        # Füge benachbarte Knoten der wichtigen Knoten in den Heap ein
        for neighbor in important_nodes:
            if not visited[neighbor] and graph[node][neighbor] != 0:
                heapq.heappush(min_heap, (graph[node][neighbor], neighbor))
                prev_node = node
    
    return mst, total_weight


# Wichtige Knoten (Rettungsstationen, Krankenhäuser, Regierungsgebäude)
important_nodes = [0, 1, 2,3, 4, 5]  #A = 0, B = 1, C  = 2,  usw...
mst, total_weight = prim(graph, important_nodes)

 # Berechnung des MST für die markierten Knoten
def calculate_and_print():
    prim(graph, important_nodes)
    # Ausgabe des Minimal Spanning Trees (MST)
    print("Minimal Spanning Tree (MST):")
    for edge in mst:
        print(f"{chr(edge[0] + 65)} - {chr(edge[1] + 65)} mit Gewicht {edge[2]}")

    print(f"\nGesamtkosten des MST: {total_weight}")
    print()



# Visualisierung des Graphen mit NetworkX und Matplotlib
G = nx.Graph()

for node in nodes:
    G.add_node(node)

# Hinzufügen der Kanten (für alle Knoten, nicht nur die wichtigen)
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        if graph[i][j] != 0:
            G.add_edge(nodes[i], nodes[j], weight=graph[i][j])

# Zeichnen des gesamten Graphen
pos = nx.spring_layout(G)  # Layout für die Visualisierung

plt.figure(figsize=(8, 8))

# Farben für verschiedene Knotenarten
# A, B, C (Rettungsstationen) = grün
# D (Krankenhaus) = rot
# E (Rathaus) = gelb
node_colors = ['green' if i == 0 or i == 1 or i == 2 else 'red' if i == 3 else 'yellow' if i == 4 else 'lightblue' for i in range(len(nodes))]

# Zeichnen der Knoten
nx.draw(G, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=12, font_weight='bold')

# Kanten, die zum MST gehören, in rot zeichnen
edges = G.edges()
edge_colors = []
edge_labels = {}  # Für Kantenbeschriftungen

# Iteration durch die Kanten und ihre Farben
for u, v in edges:
    # Wenn die Kante im MST enthalten ist, färbe sie rot, andernfalls schwarz
    if (u, v) in [(nodes[edge[0]], nodes[edge[1]]) for edge in mst] or (v, u) in [(nodes[edge[0]], nodes[edge[1]]) for edge in mst]:
        edge_colors.append('red')
        edge_labels[(u, v)] = graph[nodes.index(u)][nodes.index(v)]  # Gewicht der Kante hinzufügen
    else:
        edge_colors.append('black')

# Kanten zeichnen
nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, width=2)

# Kantenbeschriftungen (Gewicht)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Legende erstellen

# Definiere die Legende mit den entsprechenden Farben
legend_elements = [
    mpatches.Patch(color='green', label='Rettungsstation'),
    mpatches.Patch(color='red', label='Krankenhaus'),
    mpatches.Patch(color='yellow', label='Rathaus')
]

def visualize():
    # Zeige den Plot
    plt.legend(handles=legend_elements, loc='upper right')
    plt.show()
