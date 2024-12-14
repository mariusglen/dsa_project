
nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def read_adjacency_matrix(file_path):
    with open(file_path, 'r') as file:
        matrix = []
        next(file)  # Skip the first line with labels
        for line in file:
            row = list(map(int, line.strip().split()[1:]))  # Skip the first element in each row
            matrix.append(row)
    return matrix


file_paths = [
    'data/graph_ungerichtet_gewichtet.txt',
    'data/graph_ungerichtet_ungewichtet.txt',
    'data/graph_gerichtet_gewichtet.txt',
    'data/graph_gerichtet_ungewichtet.txt'
]

ungerichtet_gewichtet = read_adjacency_matrix(file_paths[0])
ungerichtet_ungewichtet = read_adjacency_matrix(file_paths[1])
gerichtet_gewichtet = read_adjacency_matrix(file_paths[2])
gerichtet_ungewichtet = read_adjacency_matrix(file_paths[3])

def print_matrix(matrix, nodes):
    print("  " + " ".join(nodes))
    for i, row in enumerate(matrix):
        print(nodes[i] + " " + " ".join(map(str, row)))


