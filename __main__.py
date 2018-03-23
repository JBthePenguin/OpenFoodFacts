#! /usr/bin/env python3
# coding: utf-8

""" imports all necessary modules and play application : main() """
# import from local modules
from off_class import category, product, favorite
from off_function import display, input_user


def main():
    """ main function display:
    - welcome message
    - choice A : found a subsitute or chek favorites
    - found substitute
        - choice B : select category
        -  user select a product -> display description and found substitute
    - chek favorites
        - display favorites"""
    appli_on = True
    while appli_on is True:
        # Welcome message
        display.display_welcome_msg()
        # Choice A
        display.display_choice_a()
        user_choice = False
        while user_choice is False:
            user_choice = input_user.save_input_user(
                "Taper 1 ou 2 puis entrée: ", 2, True
            )
            if user_choice is False:
                display.display_error_msg()
        if user_choice == "q":
            appli_on = False
        elif user_choice == 1: # user want to found a substitute
            # Build  the main category Category() : application
            main_category = category.Category("M", 0, "OpenFoodFactsApp")
            down_categories = main_category.found_down_categories()
            up_categories = []
            up_categories.append(main_category)
            return_main_menu = False
            while return_main_menu is False:
                # Display  main category or new main and down categories
                display.display_category(main_category, down_categories)
                user_choice = False
                while user_choice is False: # User select a categorie
                    user_choice = input_user.save_input_user(
                        "\nChoisir une catégorie en saisissant son numéro: ",
                        len(down_categories),
                        False
                    )
                    if user_choice is False:
                        display.display_error_msg()
                cat_selected = down_categories[user_choice - 1]
                new_main_category = category.Category(
                    cat_selected[0],
                    main_category.level + 1,
                    cat_selected[1],
                    main_category.products_id
                )
                # create list of up categories
                up_categories.append(new_main_category)
                # Display the selected category and down categories
                i = len(up_categories) - 1
                choose_return_up_cat = True
                while choose_return_up_cat is True:
                    # new while for new choice go to up category
                    i -= 1
                    new_down_categories, prods_id_no_cat = new_main_category.found_down_categories()
                    display.display_category(new_main_category, new_down_categories)
                    with_new_down_cat = False
                    if new_down_categories != []:
                        with_new_down_cat = True
                    with_prods_id_no_cat = False
                    if prods_id_no_cat != []: # Display a list of products
                        products_no_cat = []
                        for prod_id_no_cat in prods_id_no_cat:
                            product_no_cat = product.Product(prod_id_no_cat)
                            products_no_cat.append(product_no_cat)
                        title = ""
                        if with_new_down_cat is True:
                            title = "PRODUITS SANS SOUS-CATEGORIE"
                        display.display_products_list(title, products_no_cat)
                        with_prods_id_no_cat = True
                    # Choice B
                    msg, nbre_choice = input_user.found_input_msg_ch_b(
                        with_new_down_cat, with_prods_id_no_cat
                    )
                    display.display_choice_b(
                        new_main_category.name, with_new_down_cat, with_prods_id_no_cat
                    )
                    user_choice = False
                    while user_choice is False:
                        user_choice = input_user.save_input_user(msg, nbre_choice, False)
                        if user_choice is False:
                            display.display_error_msg()
                    if (
                            ((user_choice == 4) and (nbre_choice == 5)) or
                            ((user_choice == 3) and (nbre_choice != 5)) or
                            ((user_choice == 2) and (nbre_choice == 3))
                    ):
                        new_main_category = up_categories[i]
                        if new_main_category.cat_id == "M":
                            choose_return_up_cat = False
                    else:
                        choose_return_up_cat = False
                # new main cat is MAIN cat -> needed with new choice go to up category
                if new_main_category.cat_id == "M":
                    main_category = new_main_category
                    down_categories = main_category.found_down_categories()
                    up_categories = []
                    up_categories.append(main_category)
                    continue
                # no up cat choosed
                choose_product = False
                if (
                        (user_choice == 5) or
                        ((user_choice == 4) and (nbre_choice != 5)) or
                        ((user_choice == 3) and (nbre_choice == 3))
                ): # user want return to main menu
                    return_main_menu = True
                elif (
                        (user_choice == 3) or 
                        (user_choice == 2)  or
                        ((user_choice == 1) and (with_new_down_cat is False))
                ): # user want to select a product
                    choose_product = True
                    if ((with_prods_id_no_cat is True) and (user_choice == 2)):
                        display.display_products_list(
                            "PRODUITS SANS SOUS-CATEGORIE", products_no_cat
                        )
                        list_products_id = prods_id_no_cat
                    else:
                        new_products = []
                        for new_product_id in new_main_category.products_id:
                            new_product = product.Product(new_product_id)
                            new_products.append(new_product)
                        display.display_products_list(
                            "".join(["PRODUITS DE LA CATEGORIE ", new_main_category.name]),
                            new_products
                        )
                        list_products_id = new_main_category.products_id
                else: # user want to select a down category
                    main_category = new_main_category
                    down_categories = new_down_categories
                if choose_product is True: # user choose to select a product
                    user_choice = False
                    while user_choice is False:
                        user_choice = input_user.save_input_user(
                            "\nChoisir un produit en saisissant son numéro: ",
                            len(list_products_id),
                            False
                        )
                        if user_choice is False:
                            display.display_error_msg()
                    selected_product_id = list_products_id[user_choice - 1]
                    selected_product = product.Product(selected_product_id)
                    display.display_product(selected_product)
                    substitutes_id = selected_product.found_substitutes()
                    substitutes_id = substitutes_id[:10] # limit the number of subsitute at 10
                    substitutes = []
                    for substitute_id in substitutes_id:
                        substitute = product.Product(substitute_id)
                        substitutes.append(substitute)
                    if substitutes == []:
                        print("Désolé, aucun substitut nutri-score A trouvé  :(")
                    else: # substitues founded
                        title = "SUBSTITUT(S)   NUTRI-SCORE : A   :)"
                        display.display_products_list(title, substitutes)
                        user_choice = False
                        while user_choice is False:
                            user_choice = input_user.save_input_user(
                                "\nChoisi un substitut en saisissant son numéro: ",
                                len(substitutes),
                                False
                            )
                            if user_choice is False:
                                display.display_error_msg()
                        selected_substitute = substitutes[user_choice - 1]
                        display.display_product(selected_substitute)
                        display.display_choice_c()
                        user_choice = False
                        while user_choice is False:
                            user_choice = input_user.save_input_user(
                                "Taper 1 ou 2 puis entrée: ", 2, True
                            )
                            if user_choice is False:
                                display.display_error_msg()
                        if user_choice == "q":
                            appli_on = False
                        elif user_choice == 1: # saved favorite in db
                            new_favorite = favorite.Favorite(
                                selected_product.id_prod, selected_substitute.id_prod
                            )
                            new_favorite.save_in_db()
                        return_main_menu = True
        else:
            # Favorites
            favorites_id = favorite.found_favorites()
            if favorites_id == []:
                print("Aucun Favori n'est enregistré")
            else:
                favorites = []
                for favorite_id in favorites_id:
                    fav_prod = product.Product(favorite_id[0])
                    fav_sub = product.Product(favorite_id[1])
                    favorites.append((fav_prod, fav_sub))
                display.display_favorites_list(favorites)
                display.display_choice_favorite()
                user_choice = False
                while user_choice is False:
                    user_choice = input_user.save_input_user(
                        "Taper 1, 2 ou 3 puis entrée: ", 3, False
                    )
                    if user_choice is False:
                        display.display_error_msg()
                if user_choice == 3:
                    # user want return to main menu
                    pass
                else:
                    if user_choice == 2:
                        print(
                            "\n !!! Attention Suppression demandée !!! taper 'q' pour annuler"
                        )
                    favorite_choice = False
                    while favorite_choice is False: # User select a categorie
                        favorite_choice = input_user.save_input_user(
                            "\nChoisir un favori en saisissant son numéro: ",
                            len(favorites),
                            True
                        )
                        if favorite_choice is False:
                            display.display_error_msg()
                    if favorite_choice == ("q" or "Q"):
                        pass
                    elif user_choice == 2:
                        # user want to delete a favorite
                        favorite_id = favorites_id[favorite_choice - 1]
                        fav_to_delete = favorite.Favorite(
                            favorite_id[0], favorite_id[1]
                        )
                        fav_to_delete.delete_in_db()
                    else:
                        # user want to see a favorite
                        selected_favorite = favorites[favorite_choice - 1]
                        display.display_favorite(selected_favorite)
    display.display_end_msg()


if __name__ == "__main__":
    main()
