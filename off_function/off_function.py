#! /usr/bin/env python3
# coding: utf-8

""" Modules with application's functions : display and input"""


# DISPLAY
def display_welcome_msg():
    """ display the welcome message"""
    print("".join([
        "\n",
        "##############################################\n",
        "## !!! OPENFOODFACTS Python application !!! ##\n",
        "##    est là pour vous aider à trouver un   ##\n",
        "## produit plus sain  à déguster à la place ##\n",
        "##  de celui que vous apprêtiez à dévorer.  ##\n",
        "##############################################",
        "\n"
    ]))


def display_choice_a():
    """ display the first choice -> A """
    print("".join([
        "\n",
        "##############################################\n",
        "   1. Sélectionner un produit à substituer\n",
        "   2. Mes Favoris\n",
        "   Q. Quitter\n"
        "##############################################",
        "\n"
    ]))


def display_choice_b(down_categories):
    """ display the choice B with 2 or 3 options
    depends if there down categories or not"""
    msg = "".join([
        "\n"
        "##############################################\n",
        "   1. Choisir un produit\n",
        "   2. Retourner au menu principal",
        "\n"
    ])
    if down_categories is True:
        msg = "".join([
            msg,
            "   3. Choisir une sous catégorie",
            "\n"
        ])
    msg = "".join([
        msg,
        "##############################################",
        "\n"
    ])
    print(msg)


def display_waiting_msg():
    pass


def display_error_msg():
    """ display the error message
    when the input user is wrong """
    print("\n  !! mauvaise saisie !!\n")


def display_end_msg():
    """display msg when app is closed"""
    print("\n  !!! A bientôt et BON APPETIT !!!\n")


def display_category(category, down_categories):
    """ with:
    - main category -> Category()
    - down categories -> list(Category())
    display :
    - title -> name, link OFF and number of products for main category
    - a list of down categories with the number of products for each
    and the corresponding input number -> i"""
    print("".join([
        "\n",
        "########################################\n",
        "  ", category.name, "\n"
        "  ", str(len(category.products_id)), " produits", "\n",
        "########################################"
        "\n"
    ]))
    i = 1
    for down_category in down_categories:
        print("".join([
            "\n",
            str(i), ". ", down_category.name, ": ",
            str(len(down_category.products_id)), " produits"
        ]))
        i += 1


def display_products_list(category, products_id_avalaible):
    """ with:
    - products : list of products_brands
        display list of products with:
    - id for user input -> 1 2 3 ... - name - brand"""
    print("".join([
        "\n"
        "#########################\n",
        "       PRODUITS\n",
        "#########################",
        "\n"
    ]))
    i = 1
    for key in category.products_brands:
        for product_id in products_id_avalaible:
            if key == product_id:
                print("".join([
                    str(i), ". ", category.products_brands[key],
                ]))
                i += 1


def display_product(product):
    """ with:
    - product : Product()
        display all information:
    - name      brand-
    - nutrition grade
    - description
    - store
    - url_link
    """
    print("".join([
        "\n",
        "###################################################################\n",
        "    ", product.name, "    Marque: ", product.brands, "\n"
        "###################################################################\n",
        "              Nutri-Score: ", product.nutrition_grade.capitalize(), "\n\n", 
        "  A -> Mmmm !!! :)      ...         E -> Brrr !!! :(", "\n" 
        "###################################################################\n",
        " ", product.description, "\n\n",
        "###################################################################\n",
        "  lien OpenFoodFacts: ", product.url_link, "\n",
        "###################################################################\n",
        "  où m'acheter?: " + product.stores, "\n",
        "###################################################################",
        "\n"
    ]))


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
            try:
                choice = choice.lower()
            except ValueError:  
                display_error_msg()
            else:
                if choice == "q":
                    return choice
                else:
                    display_error_msg()
        else:
            for i in range(1, (nbre_choice + 1)):
                if choice == i:
                    return choice
            display_error_msg()
