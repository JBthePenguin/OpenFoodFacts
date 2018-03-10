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
        "##    de celui que vous voulez dévorer.     ##\n",
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
        "   Q. Quitter\n",
        "##############################################",
        "\n"
    ]))


def display_choice_b(category_name, with_down_categories, with_prods_id_no_cat):
    """ display the choice B with 2 or 3 options
    depends if there down categories or not"""
    i = 1
    msg = "".join([
        "\n",
        "##############################################\n"
    ])
    if with_down_categories is True:
        msg = "".join([msg, "   ", str(i), ". Choisir une sous-categorie\n"])
        i += 1
    if with_prods_id_no_cat is True:
        msg = "".join([msg, "   ", str(i), ". Choisir un produit sans sous-catégorie\n"])
        i += 1
    msg = "".join([
        msg,
        "   ", str(i), ". Choisir dans tous les produits de la catégorie ", category_name, "\n"
        "   ", str(i + 1), ". Retourner au menu principal\n"
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
        "########################################",
        "\n"
    ]))
    i = 1
    for down_category in down_categories:
        print("".join([
            "\n",
            str(i), ". ", down_category[1], ": ",
            str(down_category[2]), " produits"
        ]))
        i += 1


def display_products_list(title, products_id):
    """ with:
    - products : list of products_brands
        display list of products with:
    - id for user input -> 1 2 3 ... - name - brand"""
    print("".join([
        "\n",
        "##############################################\n",
        "".join(["  ", title, "\n"]),
        "##############################################",
        "\n"
    ]))
    i = 1
    for product_id in products_id:
        print("".join([
            str(i), ". id: ", str(product_id)
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
        "    ", product.name, "    Marque: ", product.brands, "\n",
        "###################################################################\n",
        "              Nutri-Score: ", product.nutrition_grade.capitalize(), "\n\n",
        "  A -> Mmmm !!! :)      ...         E -> Brrr !!! :(", "\n",
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
def save_input_user(input_msg, nbre_choice, with_quit):
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
                if (with_quit is True) and (choice == "q"):
                    return choice
                else:
                    display_error_msg()
        else:
            for i in range(1, (nbre_choice + 1)):
                if choice == i:
                    return choice
            display_error_msg()
