#! /usr/bin/env python3
# coding: utf-8

""" Modules with application's functions to displaying all differents msg"""
from colorama import init, Fore, Style

init(autoreset=True)


def display_welcome_msg():
    """ display the welcome message"""
    msg = "".join([
        "\n               ##############################################",
        "\n               ## !!! ", (Fore.RED + Style.BRIGHT + "OPENFOODFACTS"),
        (Fore.GREEN + Style.NORMAL + " "),
        "Python application !!! ##",
        "\n               ##    est là pour vous aider à trouver un   ##",
        "\n               ## produit plus sain  à déguster à la place ##",
        "\n               ##    de celui que vous voulez dévorer.     ##",
        "\n               ##############################################",
        "\n"
    ])
    print(Fore.GREEN + msg)


def display_choice_a():
    """ display the first choice -> A """
    msg = "".join([
        "\n",
        "##############################################\n",
        "   1. Sélectionner un produit à substituer\n",
        "   2. Mes Favoris\n",
        "   Q. Quitter\n",
        "##############################################",
        "\n"
    ])
    print(Fore.WHITE + msg)


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
        "   ", str(i + 1), ". Retourner à la catégorie supérieure\n"
        "   ", str(i + 2), ". Retourner au menu principal\n"
        "##############################################",
        "\n"
    ])
    print(Fore.WHITE + msg)


def display_choice_c():
    """ display the choice save or not in favorites -> C """
    msg = "".join([
        "\n",
        "##############################################\n",
        "   1. Ajouter aux Favoris\n",
        "   2. Retourner au menu principal\n",
        "   Q. Quitter\n",
        "##############################################",
        "\n"
    ])
    print(Fore.WHITE + msg)


def display_error_msg():
    """ display the error message
    when the input user is wrong """
    print(Fore.RED + Style.BRIGHT + "\n  !! mauvaise saisie !!\n")


def display_end_msg():
    """display msg when app is closed"""
    print(Fore.CYAN + Style.BRIGHT + "\n  !!! A bientôt et BON APPETIT !!!\n")


def display_category(category, down_categories):
    """ with:
    - main category -> Category()
    - down categories -> list(Category())
    display :
    - title -> name, link OFF and number of products for main category
    - a list of down categories with the number of products for each
    and the corresponding input number -> i"""
    msg = "".join([
        "\n",
        "               ########################################\n",
        "                     ", category.name, "\n"
        "                     ", str(len(category.products_id)), " produits", "\n",
        "               ########################################",
        "\n"
    ])
    print(Fore.RED + Style.BRIGHT + msg)
    i = 1
    for down_category in down_categories:
        msg = "".join([
            "\n",
            str(i), ". ", down_category[1], ": ",
            str(down_category[2]), " produits"
        ])
        print(Fore.GREEN + Style.NORMAL + msg)
        i += 1


def display_products_list(title, products):
    """ with:
    - products : list of products_brands
        display list of products with:
    - id for user input -> 1 2 3 ... - name - brand"""
    msg = "".join([
        "\n",
        "##############################################\n",
        "".join(["  ", title, "\n"]),
        "##############################################",
        "\n"
    ])
    print(Fore.RED + Style.BRIGHT + msg)
    i = 1
    for product in products:
        msg = "".join([
            str(i), ". ", product.name, "   Marque: ", product.brands
        ])
        print(Fore.GREEN + Style.NORMAL + msg)
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
    if product.nutrition_grade.capitalize() == "A":
        font_color = Fore.GREEN
    elif product.nutrition_grade.capitalize() == "B":
        font_color = Fore.YELLOW
    elif product.nutrition_grade.capitalize() == "C":
        font_color = Fore.WHITE
    elif product.nutrition_grade.capitalize() == "D":
        font_color = Fore.BLUE
    else:
        font_color = Fore.RED
    msg = "".join([
        "\n",
        "###################################################################\n",
        "    ", (font_color + product.name), (Fore.CYAN + "    Marque: "),
        (font_color + product.brands), (Fore.CYAN + "\n"),
        "###################################################################\n",
        "              Nutri-Score: ",
        (font_color + Style.BRIGHT + product.nutrition_grade.capitalize()),
        (Fore.CYAN + Style.NORMAL + "\n\n"),
        (Fore.GREEN + "  A -> Mmmm !!! :)"), (Fore.CYAN + " "), "     ...         ",
        (Fore.RED + "E -> Brrr !!! :("), (Fore.CYAN + "\n"),
        "###################################################################\n",
        " ", (font_color + product.description), (Fore.CYAN + "\n\n"),
        "###################################################################\n",
        "  lien OpenFoodFacts: ", (font_color + product.url_link), (Fore.CYAN + "\n"),
        "###################################################################\n",
        "  où m'acheter?: " + (font_color + product.stores), (Fore.CYAN + "\n"),
        "###################################################################",
        "\n"
    ])
    print(Fore.CYAN + msg)


def display_favorites_list(favorites):
    """ with favorites : list of favorite -> (prod, sub) """
    msg = "".join([
        "\n",
        "###################################################################\n",
        "                 FAVORIS\n", "#############################"
    ])
    i = 0
    for favorite in favorites:
        i += 1
        msg = "".join([
            (Fore.RED + Style.BRIGHT + msg), (Fore.GREEN + Style.NORMAL + "\n"),
            str(i), ". ", favorite[0].name, ", ",
            favorite[0].brands, ", ", favorite[0].nutrition_grade.capitalize(),
            "  -->  ", favorite[1].name, ", ",
            favorite[1].brands, ", ", favorite[1].nutrition_grade.capitalize()
        ])
    print(Fore.GREEN + msg)


def display_choice_favorite():
    """ display chooses if user select favorite """
    msg = "".join([
        "\n",
        "##############################################\n",
        "   1. Consulter un Favori\n",
        "   2. Supprimer un Favori\n",
        "   3. Retourner au menu principal\n",
        "##############################################",
        "\n"
    ])
    print(Fore.WHITE + msg)


def display_favorite(favorite):
    """ with a favorite -> (prod, sub) """
    if favorite[0].nutrition_grade.capitalize() == "A":
        font_color = Fore.GREEN
    elif favorite[0].nutrition_grade.capitalize() == "B":
        font_color = Fore.YELLOW
    elif favorite[0].nutrition_grade.capitalize() == "C":
        font_color = Fore.WHITE
    elif favorite[0].nutrition_grade.capitalize() == "D":
        font_color = Fore.BLUE
    else:
        font_color = Fore.RED
    msg = "".join([
        (Fore.RED + Style.BRIGHT + "\n"),
        "###################################################################\n",
        "                     Favori \n",
        "              ########################\n\n",
        (Fore.CYAN + Style.NORMAL + " Product : "),
        (font_color + favorite[0].name), (Fore.CYAN + "   Marque: "),
        (font_color + favorite[0].brands), (Fore.CYAN + "\n"),
        "##############\n",
        "          Nutri-Score: ",
        (font_color + Style.BRIGHT + favorite[0].nutrition_grade.capitalize()),
        (Fore.CYAN + Style.NORMAL + "\n"),
        "#########################\n",
        "  lien OpenFoodFacts: ", (font_color + favorite[0].url_link), (Fore.CYAN + "\n"),
        "#########################\n",
        "  où m'acheter?: ", (font_color + favorite[0].stores), (Fore.CYAN + "\n"),
        "############################################\n\n"
        " Substitut : ", (Fore.GREEN + favorite[1].name), (Fore.CYAN + "   Marque: "),
        (Fore.GREEN + favorite[1].brands), (Fore.CYAN + "\n"),
        "##############\n",
        "          Nutri-Score: ",
        (Fore.GREEN + Style.BRIGHT + favorite[1].nutrition_grade.capitalize()),
        (Fore.CYAN + Style.NORMAL + "\n"),
        "#########################\n",
        "  lien OpenFoodFacts: ", (Fore.GREEN + favorite[1].url_link),
        (Fore.CYAN + "\n"),
        "#########################\n",
        "  où m'acheter?: ", (Fore.GREEN + favorite[1].stores), (Fore.CYAN + "\n"),
        "###################################################################\n"
    ])
    print(Fore.CYAN + msg)
