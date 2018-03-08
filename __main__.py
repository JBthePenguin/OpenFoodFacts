#! /usr/bin/env python3
# coding: utf-8

""" imports all necessary modules and play application : main() """

# import from local modules
from off_class import category, product
from off_function import off_function


def main():
    """ main function display:
    - welcome message
    - choice A : select a product or a favorite
    - choice B : select category
    -  user select a product -> display description and found substitute"""
    appli_on = True
    while appli_on is True:
        # Welcome message
        off_function.display_welcome_msg()
        # Choice A
        off_function.display_choice_a()
        user_choice = off_function.save_input_user(
            "Taper 1 ou 2 puis entrée: ", 2
        )
        if user_choice == "q":
            appli_on = False
        elif user_choice == 1:
            # Build  the main category Category() : application
            cat_id = "M"
            level = 0
            name = "OpenFoodFactsApp"
            main_category = category.Category(cat_id, level, name)
            main_category.found_products_id()
            down_categories = main_category.found_down_categories()
            return_main_menu = False
            while return_main_menu is False:
                # Display  main category or new main and down categories
                off_function.display_category(main_category, down_categories)
                # User select a categorie
                user_choice = off_function.save_input_user(
                    "\nChoisir une catégorie en saisissant son numéro: ",
                    len(down_categories)
                )
                new_main_category = down_categories[user_choice - 1]
                products_id_available = new_main_category.products_id
                # Display the selected category and down categories
                new_down_categories = new_main_category.found_down_categories()
                for new_down_category in new_down_categories:
                    new_down_category.update_products_id(products_id_available)
                off_function.display_category(new_main_category, new_down_categories)
                # Display a list of products
                off_function.display_products_list(new_main_category, products_id_available)
                # Choice B
                if new_down_categories != []:
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
                    off_function.display_products_list(new_main_category, products_id_available)
                    user_choice = off_function.save_input_user(
                        "\nChoisir un produit en saisissant son numéro: ",
                        len(new_main_category.products_id)
                    )
                    selected_product_id = new_main_category.products_id[user_choice - 1]
                    selected_product = product.Product(selected_product_id)
                    off_function.display_product(selected_product)
                    print("".join([
                        "##################################\n",
                        " found substitute comming soon\n",
                        "##################################\n"
                    ]))
                    return_main_menu = True
                    appli_on = False
                if user_choice == 2:
                    # user choose to return to main menu
                    return_main_menu = True
                elif user_choice == 3:
                    # user want to select a down categorie
                    main_category = new_main_category
                    down_categories = new_down_categories
                else:
                    # user quit
                    return_main_menu = True
                    appli_on = False
        else:
            print("Favori non disponible")
    off_function.display_end_msg()


if __name__ == "__main__":
    main()
