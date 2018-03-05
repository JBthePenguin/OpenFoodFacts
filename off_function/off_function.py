#! /usr/bin/env python3
# coding: utf-8

""" Module with application's functions"""

# DISPLAY
def display_welcome_msg():
    """ display the welcome message"""
    print(("##############################################"), (
           "\n## !!! OPENFOODFACTS Python application !!! ##"), (
           "\n##############################################\n")
    )

def display_choice_a():
    """ display the first choice -> A """
    print(("##############################################"), (
           "\n  1. Sélectionner un produit à substituer"), (
           "\n  2. Mes Favoris"), (
           "\n##############################################\n")
    )


def display_choice_b(down_categories):
    """ display the choice B with 2 or 3 options
    depends if there down categories or not"""
    msg = ("##############################################") +(
        "\n  1. Choisir un produit") +(
            "\n  2. Retourner aux catégories principales")
    if down_categories is True:
        msg += "\n  3. Choisir une sous catégorie"
    msg += "\n##############################################\n"
    print(msg)


def display_error_msg():
    """ display the error message
    when the input user is wrong """
    print("\n  !! mauvaise saisie !!\n")


def display_categories_list(title, categories, cursor, query_category_product):
    """ display the name of category with
    his number of products and id for user input -> 1 2 3 ..."""
    print(("#########################"), (
           "\n " + title), (
           "\n#########################")
    )
    i = 1
    for selected_category in categories:
        print(str(i) + ". " + selected_category.name + ": " + str(
            selected_category.found_nbre_products(
                cursor, query_category_product)) + " produits")
        i += 1


def display_products_list(products, cursor, query_product):
    print(("#########################"), (
           "\n PRODUITS"), (
           "\n#########################\n")
    )
    i = 1
    for product_id in products:
        cursor.execute(query_product, (product_id,))
        for (name, brands) in cursor:
            print(str(i) + ". " + name + "    Marque: " + brands)
            i += 1


# INPUT
def save_input_user(input_msg, nbre_choice):
    """ valid the input user before return it"""
    valid_input = False
    while valid_input is False:
        choice = input(input_msg)
        if choice == "":
            continue
        try:
            choice = int(choice)
        except ValueError:
            display_error_msg()
        else:
            for i in range(1, (nbre_choice + 1)):
                if choice == i:
                    return choice
            display_error_msg()

