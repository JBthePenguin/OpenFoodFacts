#! /usr/bin/env python3
# coding: utf-8

""" Module substitute with function found"""
# import from third party modules
import mysql.connector
# import from local modules
from . import category


###
# DATABASE
###
## Connexion
# to DataBase
CNX = mysql.connector.connect(
    user="OpenFoodFactsApp", password='BonAppetit', host="127.0.0.1", database="db_openfoodfacts")
CURSOR = CNX.cursor()
## Models
# to SELECT Category.* with level
QUERY_CATEGORY_1 = ("SELECT id, level, name FROM Category "
                  "WHERE level = %s")
# to SELECT Category.* with id
QUERY_CATEGORY_2 = ("SELECT id, level, name FROM Category "
                  "WHERE id = %s")
# to SELECT CategoryProduct.product_id with category_id
QUERY_CATEGORY_PRODUCT_1 = ("SELECT product_id FROM CategoryProduct "
                            "WHERE category_id = %s")
# to SELECT CategoryProduct.category_id with product_id
QUERY_CATEGORY_PRODUCT_2 = ("SELECT category_id FROM CategoryProduct "
                            "WHERE product_id = %s")
# to SELECT Product.name with id
QUERY_PRODUCT = ("SELECT name, brands FROM Product "
                 "WHERE id = %s")


def found():
    """found function display:
    - categories level 1
    - down categories and products
    - choice C
    - search input
    - substitute founded"""
    # Categories level 1
    print(("#########################"),(
           "\n CATEGORIES"),(
           "\n#########################")
    )
    categories = []
    CURSOR.execute(QUERY_CATEGORY_1, (1,))
    for (cat_id, cat_level, cat_name) in CURSOR:
        collected_category = category.Category(cat_id, cat_level, cat_name)
        categories.append(collected_category)
    i = 1
    for collected_category in categories:
        nbre_products = len(collected_category.found_products(
            CURSOR, QUERY_CATEGORY_PRODUCT_1))
        print(str(i) + ". " + collected_category.name + ": " + str(
            nbre_products) + " produits")
        i += 1
    # User's Select category in categories
    input_error = True
    while input_error == True:
        user_choice = ""
        while user_choice == "":
            user_choice = input(
                "\nChoisir une catégorie en saisissant son numéro: ")
        try:
            user_choice = int(user_choice)
        except ValueError:
            print("  !! mauvaise saisie !!")
        else:
            if user_choice in range (1, i):
                input_error = False
                selected_category = categories[user_choice - 1]
            else:
                print("\n  !! mauvaise saisie !!")
    print("\n" + selected_category.name + "\n")
    # down categories and products
    products = selected_category.found_products(
        CURSOR, QUERY_CATEGORY_PRODUCT_1)
    down_categories = selected_category.found_down_categories(
        products, CURSOR, QUERY_CATEGORY_1, QUERY_CATEGORY_PRODUCT_2)
    print(("#########################"),(
           "\n SOUS CATEGORIES"),(
           "\n#########################\n")
    )
    i = 1
    for category_id in down_categories:
        CURSOR.execute(QUERY_CATEGORY_2, (category_id,))
        for (cat_id, cat_level, cat_name) in CURSOR:
            print("-- " + str(i) + ". " + cat_name)
            i += 1
    print(("#########################"),(
           "\n PRODUITS"),(
           "\n#########################\n")
    )
    for product_id in products:
        CURSOR.execute(QUERY_PRODUCT, (product_id,))
        for (name, brands) in CURSOR:
            print(name, "  ", brands)
