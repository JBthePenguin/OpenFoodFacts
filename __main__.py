#! /usr/bin/env python3
# coding: utf-8

""" imports all necessary modules and play application : main() """


# import from standard modules
from os.path import dirname as path_dirname
# import from third party module
# import from local modules
from substitute import substitute
from favorite import favorite


MAIN_DIR = path_dirname(__file__)


def main():
    """ main function display:
    - welcome message
    - choice A : choose a product or a favorite"""
    # Welcome message
    print(("##############################################"), (
           "\n## !!! OPENFOODFACTS Python application !!! ##"), (
           "\n##############################################\n")
    )
    # Choice A
    print(("##############################################"), (
           "\n  1. Sélectionner un produit à substituer"), (
           "\n  2. Mes Favoris"), (
           "\n##############################################\n")
    )
    input_error = True
    while input_error == True:
        choice_a = ""
        while choice_a == "":
            choice_a = input("Taper 1 ou 2 (puis entrée): ")
            print("\n")
        if choice_a in ["1", "2"]:
            input_error = False
            if choice_a == "1":
                substitute.found()
            else:
                favorite.found()
        else:
            print("  !! mauvaise saisie !!\n")


if __name__ == "__main__":
    main()
