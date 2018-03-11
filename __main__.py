#! /usr/bin/env python3
# coding: utf-8

""" imports all necessary modules and play application : main() """

# import from local modules
from off_class import category, product, favorite
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
            "Taper 1 ou 2 puis entrée: ", 2, True
        )
        if user_choice == "q":
            appli_on = False
        elif user_choice == 1:
            # Build  the main category Category() : application
            cat_id = "M"
            level = 0
            name = "OpenFoodFactsApp"
            main_category = category.Category(cat_id, level, name)
            down_categories = main_category.found_down_categories()
            return_main_menu = False
            while return_main_menu is False:
                # Display  main category or new main and down categories
                off_function.display_category(main_category, down_categories)
                # User select a categorie
                user_choice = off_function.save_input_user(
                    "\nChoisir une catégorie en saisissant son numéro: ",
                    len(down_categories),
                    False
                )
                cat_selected = down_categories[user_choice - 1]
                new_main_category = category.Category(
                    cat_selected[0],
                    main_category.level + 1,
                    cat_selected[1],
                    main_category.products_id
                )
                # Display the selected category and down categories
                new_down_categories, prods_id_no_cat = new_main_category.found_down_categories()
                off_function.display_category(new_main_category, new_down_categories)
                # Display a list of products
                with_prods_id_no_cat = False
                if prods_id_no_cat != []:
                    products_no_cat = []
                    for prod_id_no_cat in prods_id_no_cat:
                        product_no_cat = product.Product(prod_id_no_cat)
                        products_no_cat.append(product_no_cat)
                    off_function.display_products_list(
                        "PRODUITS SANS SOUS-CATEGORIE", products_no_cat
                    )
                    with_prods_id_no_cat = True
                # Choice B
                msg = "Taper 1"
                with_new_down_categories = False
                if new_down_categories != []:
                    with_new_down_categories = True
                    if with_prods_id_no_cat is True:
                        nbre_choice = 4
                        msg = "".join([msg, ", 2, 3 ou 4 (puis entrée): "])
                    else:
                        nbre_choice = 3
                        msg = "".join([msg, ", 2 ou 3 (puis entrée): "])
                else:
                    if with_prods_id_no_cat is True:
                        nbre_choice = 3
                        msg = "".join([msg, ", 2 ou 3 (puis entrée): "])
                    else:
                        nbre_choice = 2
                        msg = "".join([msg, "ou 2 (puis entrée): "])
                off_function.display_choice_b(
                    new_main_category.name, with_new_down_categories, with_prods_id_no_cat
                )
                user_choice = off_function.save_input_user(msg, nbre_choice, False)
                # found corresponding msg with the user choice
                choose_product = False
                if user_choice == 4:
                    return_main_menu = True
                elif user_choice == 3:
                    if nbre_choice == 4:
                        # user choose to select a product
                        choose_product = True
                        new_products = []
                        for new_product_id in new_main_category.products_id:
                            new_product = product.Product(new_product_id)
                            new_products.append(new_product)
                        off_function.display_products_list(
                            "".join(["PRODUITS DE LA CATEGORIE ", new_main_category.name]),
                            new_products
                        )
                        list_products_id = new_main_category.products_id
                    else:
                        return_main_menu = True
                elif user_choice == 2:
                    if nbre_choice == 2:
                        return_main_menu = True
                    elif nbre_choice == 3:
                        choose_product = True
                        new_products = []
                        for new_product_id in new_main_category.products_id:
                            new_product = product.Product(new_product_id)
                            new_products.append(new_product)
                        off_function.display_products_list(
                            "".join(["PRODUITS DE LA CATEGORIE ", new_main_category.name]),
                            new_products
                        )
                        list_products_id = new_main_category.products_id
                    else:
                        choose_product = True
                        off_function.display_products_list(
                                "PRODUITS SANS SOUS-CATEGORIE", products_no_cat
                        )
                        list_products_id = prods_id_no_cat
                else:
                    if with_new_down_categories is True:
                        main_category = new_main_category
                        down_categories = new_down_categories
                    elif with_prods_id_no_cat is True:
                        choose_product = True
                        off_function.display_products_list(
                                "PRODUITS SANS SOUS-CATEGORIE", products_no_cat
                        )
                        list_products_id = prods_id_no_cat
                    else:
                        choose_product = True
                        new_products = []
                        for new_product_id in new_main_category.products_id:
                            new_product = product.Product(new_product_id)
                            new_products.append(new_product)
                        off_function.display_products_list(
                            "".join(["PRODUITS DE LA CATEGORIE ", new_main_category.name]),
                            new_products
                        )
                        list_products_id = new_main_category.products_id
                if choose_product is True:
                    # user choose to select a product
                    user_choice = off_function.save_input_user(
                        "\nChoisir un produit en saisissant son numéro: ",
                        len(list_products_id),
                        False
                    )
                    selected_product_id = list_products_id[user_choice - 1]
                    selected_product = product.Product(selected_product_id)
                    off_function.display_product(selected_product)
                    substitutes_id = selected_product.found_substitutes()
                    # limit the number of subsitute at 10
                    substitutes_id = substitutes_id[:10]
                    substitutes = []
                    for substitute_id in substitutes_id:
                        substitute = product.Product(substitute_id)
                        substitutes.append(substitute)
                    if substitutes == []:
                        title = "Désolé, aucun substitut nutri-score A trouvé  :("
                    else:
                        title = "SUBSTITUT(S)   NUTRI-SCORE : A   :)"
                    off_function.display_products_list(
                        title,
                        substitutes
                    )
                    if substitutes != []:
                        user_choice = off_function.save_input_user(
                            "\nChoisi un substitut en saisissant son numéro: ",
                            len(substitutes),
                            False
                        )
                        selected_substitute = substitutes[user_choice - 1]
                        off_function.display_product(selected_substitute)
                        off_function.display_choice_c()
                        user_choice = off_function.save_input_user(
                            "Taper 1 ou 2 puis entrée: ", 2, True
                        )
                        if user_choice == "q":
                            appli_on = False
                            return_main_menu = True
                        elif user_choice == 2:
                            return_main_menu = True
                        else:
                            new_favorite = favorite.Favorite(
                                selected_product.id_prod, selected_substitute.id_prod
                            )
                            print(new_favorite.save_in_db())
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
                off_function.display_favorites_list(favorites)
    off_function.display_end_msg()


if __name__ == "__main__":
    main()
