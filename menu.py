import os
import b1
from b1 import print_matrix, nodes, ungerichtet_gewichtet, ungerichtet_ungewichtet, gerichtet_gewichtet, gerichtet_ungewichtet
import b2
import f1


os.system('clear')
while True:
    print()
    print("===========================================")
    print("Planungstool fur das Katastrophenmanagement")
    print("===========================================")
    print("b1. B1: Stadtplan einlesen und ausgeben")
    print("b2. B2: Stadtplan modifizieren")
    print("f1. F1: Kommunikationsinfrastruktur wiederaufbauen")
    print("x. EXIT")
    print("===========================================")
    choice = input("Enter your choice: ")
    if choice == "b1":
        print("Choose which graph to show:")
        print("1. Ungerichtet Gewichtet")
        print("2. ungerichtet_ungewichtet")
        print("3. gerichtet_gewichtet")
        print("4. gerichtet_ungewichtet")
        choice_graph = input("Enter your choice: ")
        if choice_graph == "1":
            print("Adjacency matrix for Ungerichtet Gewichtet:")
            print_matrix(ungerichtet_gewichtet, nodes)
        elif choice_graph == "2":
            print("Adjacency matrix for ungerichtet_ungewichtet:")
            print_matrix(ungerichtet_ungewichtet, nodes)
        elif choice_graph == "3":
            print("Adjacency matrix for gerichtet_gewichtet:")
            print_matrix(gerichtet_gewichtet, nodes)
        elif choice_graph == "4":
            print("Adjacency matrix for gerichtet_ungewichtet:")
            print_matrix(gerichtet_ungewichtet, nodes)
        else:
            print("Invalid choice. Please try again.")
            print()
    elif choice == "b2":
        b2.test()
    elif choice == "f1":
        print("Adjacency matrix for Ungerichtet Gewichtet:")
        print_matrix(ungerichtet_gewichtet, nodes)
        print("\n1. MST anwenden ")
        print("2. MST visualisieren")
        choise_f1 = input("Enter your choice: ")
        if choise_f1 == "1":
            f1.calculate_and_print()
        elif choise_f1 == "2":
            f1.visualize()
        elif choise_f1 == "x":
            print("Exiting program...")
            break

    elif choice == "x":
        print("Exiting program...")
        break
    else:
        print("Invalid choice. Please try again.")

