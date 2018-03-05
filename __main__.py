#! /usr/bin/env python3
# coding: utf-8

""" imports all necessary modules and play application : main() """


# import from standard modules
from os.path import dirname as path_dirname
# import from third party modules
import mysql.connector
# import from local modules
from off_class import category, product
from off_function import off_function


MAIN_DIR = path_dirname(__file__)
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
# to SELECT Product.name and Product.brands with id
QUERY_PRODUCT_1 = ("SELECT name, brands FROM Product "
                 "WHERE id = %s")
# to SELECT Product.* with id
QUERY_PRODUCT_2 = (
    "SELECT name, brands, nutrition_grade, url_link, description, stores   FROM Product "
    "WHERE id = %s")


def main():
    """ main function display:
    - welcome message
    - choice A : select a product or a favorite
    - choice B : select category
    -  user select a product -> display description and found substitute"""
    # Welcome message
    off_function.display_welcome_msg()
    # Choice A
    off_function.display_choice_a()
    user_choice = off_function.save_input_user(
        "Taper 1 ou 2 (puis entrée): ", 2
    )
    if user_choice == 1:
        # Found and display categories level 1
        categories = []
        CURSOR.execute(QUERY_CATEGORY_1, (1,))
        for (cat_id, cat_level, cat_name) in CURSOR:
            selected_category = category.Category(cat_id, cat_level, cat_name)
            categories.append(selected_category)
        product_founded = False
        while product_founded is False:
            off_function.display_categories_list(
                "CATEGORIES", categories, CURSOR, QUERY_CATEGORY_PRODUCT_1)
            # User select a categorie
            user_choice = off_function.save_input_user(
                "\nChoisir une catégorie en saisissant son numéro: ", (
                    len(categories)  #+ 1
                )
            )
            selected_category = categories[user_choice - 1]
            return_main_categories = False
            while return_main_categories is False:
                # found and display down categories and products
                print("\n" + selected_category.name + "\n")
                products = selected_category.found_products_id(
                    CURSOR, QUERY_CATEGORY_PRODUCT_1
                )
                down_categories = selected_category.found_down_categories(
                    products, CURSOR, QUERY_CATEGORY_1, QUERY_CATEGORY_PRODUCT_2
                )
                if down_categories != []:
                    off_function.display_categories_list(
                        "SOUS CATEGORIES", down_categories, CURSOR, QUERY_CATEGORY_PRODUCT_1)
                off_function.display_products_list(products, CURSOR, QUERY_PRODUCT_1)
                # Choice B
                if down_categories != []:
                    off_function.display_choice_b(True)
                    user_choice = off_function.save_input_user(
                        "Taper 1, 2 ou 3 (puis entrée): ", 3
                    )
                else:
                    off_function.display_choice_b(False)
                    user_choice = off_function.save_input_user(
                        "Taper 1 ou 2 (puis entrée): ", 2
                    )
                if user_choice == 1:
                    # user select a product
                    off_function.display_products_list(products, CURSOR, QUERY_PRODUCT_1)
                    user_choice = off_function.save_input_user(
                        "\nChoisir un produit en saisissant son numéro: ", (
                            len(products)
                        )
                    )
                    selected_product_id = products[user_choice - 1]
                    # display all description of the product ---> coming soon
                    CURSOR.execute(QUERY_PRODUCT_2, (selected_product_id,))
                    for (name, brands, nutrition_grade, url_link, description, stores) in CURSOR:
                        selected_product = product.Product(
                            selected_product_id, name, brands,
                            nutrition_grade, url_link, description, stores)
                    off_function.display_product(selected_product)
                    product_founded = True
                    return_main_categories = True
                elif user_choice == 2:
                    # user select return to main category
                    return_main_categories = True
                else:
                    # user choose a down category
                    user_choice = off_function.save_input_user(
                        "\nChoisir une catégorie en saisissant son numéro: ", (
                            len(down_categories)
                        )
                    )
                    selected_category = down_categories[user_choice - 1]
    else:
        print("Favori non disponible")
if __name__ == "__main__":
    main()
