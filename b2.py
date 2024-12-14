#B2: Stadtplan modifizieren
import os 
import b1
from b1 import print_matrix, nodes, ungerichtet_gewichtet, ungerichtet_ungewichtet, gerichtet_gewichtet, gerichtet_ungewichtet
#print(ungerichtet_gewichtet)
#funtion to add a new node to ungerichtet_gewichtet
def add_node(node,node_name):
    #add the new node to the list of nodes
    nodes.append(str(node_name))
    for i in range(len(ungerichtet_gewichtet)):
        ungerichtet_gewichtet[i].append(0)
    ungerichtet_gewichtet.append([0] * (len(ungerichtet_gewichtet) + 1))
    ungerichtet_gewichtet[-1][-1] = 0
    return ungerichtet_gewichtet

#function to add a new edge to ungerichtet_gewichtet
def add_edge(node1, node2, weight):
    ungerichtet_gewichtet[node1][node2] = weight
    ungerichtet_gewichtet[node2][node1] = weight
    return

#function to remove a node from ungerichtet_gewichtet
def remove_node(node):
    #remove the node from the list of nodes
    nodes.pop(node)
    #remove the node from the matrix
    ungerichtet_gewichtet.pop(node)
    for i in range(len(ungerichtet_gewichtet)):
        ungerichtet_gewichtet[i].pop(node)
    return ungerichtet_gewichtet


def test():
    os.system('clear')
    while True:
        
        print()
        print("====================================================")

        print("Was möchtst du an den Stadtplan(un_ge) modifizieren?")
        print("0. print the stadtplan")
        print("1. Kreuzungspunkt hinzufügen")
        print("2. Strasse hinzufügen")
        print("3. Kreuzungspunkt entfernen")
        
        print()

        print("s. sava the stadtplan to the file")
        print("x. back to menu")
        print("====================================================")

        choise_b2 = input("Modiefiezierung auswahlen: ")
        if choise_b2 == "0":
            os.system('clear')
            print_matrix(ungerichtet_gewichtet, nodes)

        elif choise_b2 == "1":
            print("Kreuzungspunkt hinzufügen")
            node_name = input("Input the Namen des Kreuzungspunkt: ")
            add_node(len(nodes), node_name)
        elif choise_b2 == "2":
            print("Strasse hinzufügen")
            node1 = int(input("Von welche Kreuzungspunkt: "))
            node2 = int(input("Bin welche Kreuzungspunkt: "))
            weight = int(input("Wie lange soll die Strasse sein: "))
            add_edge(node1, node2, weight)
        elif choise_b2 == "3":
            print("Knoten entfernen")
            node = int(input("Input the node to remove: "))
            remove_node(node)
        elif choise_b2 == "x":
            print("back to main...")
            break
        else:
            print("Invalid choice. Please try again.")
