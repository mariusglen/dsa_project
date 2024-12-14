import numpy as np
import random
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


#Generierung einer Stadtplan mit Kapazitaten fur die einzelnen Wege
new_matrix = []
for row in matrix:
    new_row = []
    for value in row:
        if value > 0:  # If there's an edge
            new_value = random.choice([0] + [random.randint(50, 150) for _ in range(9)])
        else:  # No edge
            new_value = 0
        new_row.append(new_value)
    new_matrix.append(new_row)

new_matrix = np.array(new_matrix)

print(new_matrix)