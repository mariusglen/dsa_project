import matplotlib.pyplot as plt
import networkx as nx
from b1 import nodes, ungerichtet_gewichtet, ungerichtet_ungewichtet, gerichtet_gewichtet, gerichtet_ungewichtet

matrix = gerichtet_gewichtet
def visualize_graph(nodes, matrix):
    G = nx.DiGraph()
    
    for i, node in enumerate(nodes):
        for j, weight in enumerate(matrix[i]):
            if weight != 0:
                G.add_edge(node, nodes[j], weight=weight)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Directed Weighted Graph")
    plt.show()

if __name__ == "__main__":
    visualize_graph(nodes, matrix)
