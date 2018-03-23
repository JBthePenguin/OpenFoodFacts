#! /usr/bin/env python3
# coding: utf-8

""" Tests for module category """

""" imports all necessary modules"""
import sys
sys.path.append('..')
# import from third party modules
import mysql.connector
# import local modules
from off_class import category
###
# DATABASE
###
## Connexion
# to DataBase
CNX = mysql.connector.connect(
    user="OpenFoodFactsApp", password='BonAppetit', host="127.0.0.1", database="db_openfoodfacts"
)
CURSOR = CNX.cursor()
## Query Models
# to SELECT Category.id and Category.name with level
QUERY_CATEGORY_ID = ("SELECT id, name FROM Category "
                     "WHERE level = %s")
# to SELECT count(CategoryProduct.product_id) with category_id
QUERY_PRODUCT_CATEGORY_COUNT = ("SELECT count(product_id) FROM CategoryProduct "
                                "WHERE category_id = %s")
# to SELECT all id in Product -> main category
QUERY_ALL_PRODUCT = ("SELECT id FROM Product ")
# to SELECT CategoryProduct.product_id with category_id
QUERY_PRODUCT_CATEGORY = ("SELECT product_id FROM CategoryProduct "
                          "WHERE category_id = %s")
# to SELECT CategoryProduct.category_id with product_id
QUERY_CATEGORY_PRODUCT = ("SELECT category_id FROM CategoryProduct "
                          "WHERE product_id = %s")


class TestCategory:
    """ Tests for class Category"""
    MAIN_CAT = category.Category("M", 0, "OpenFoodFactsApp")

    def test_categoy_init(self):
        """ Test if self.products.id is OK for main and one other category """
        # Main category
        main_cat_products_id = []
        CURSOR.execute(QUERY_ALL_PRODUCT, ())
        for product_id in CURSOR:
            main_cat_products_id.append(product_id[0])
        assert main_cat_products_id == self.MAIN_CAT.products_id
        # other category present in db:  1978 |     1 | Gaufres
        cat_products_id = []
        CURSOR.execute(QUERY_PRODUCT_CATEGORY, (1978,))
        for product_id in CURSOR:
            cat_products_id.append(product_id[0])
        cat_in_db = category.Category(1978, 1, "Gaufres", main_cat_products_id)
        assert cat_products_id == cat_in_db.products_id

    def test_found_down_categories(self):
        """ Test if down_categories [(id, name, nbre_products)] is OK
        for main and also products_id_no_category for one other category """
        # Main category  -> down_categories (>500 products)
        main_cat_down_cats = []
        main_cat_down_cats_id_name = []
        CURSOR.execute(QUERY_CATEGORY_ID, (1,))
        for (cat_id, cat_name) in CURSOR:
            main_cat_down_cats_id_name.append((cat_id, cat_name))
        for down_cat_id_name in main_cat_down_cats_id_name:
            CURSOR.execute(QUERY_PRODUCT_CATEGORY_COUNT, (down_cat_id_name[0],))
            for nbre_products_id in CURSOR:
                if nbre_products_id[0] > 500:
                    main_cat_down_cats.append(
                        (down_cat_id_name[0], down_cat_id_name[1], nbre_products_id[0])
                    )
        down_categories = self.MAIN_CAT.found_down_categories()
        # nbre of down categories
        assert len(down_categories) == len(main_cat_down_cats)
        down_category = down_categories[2]
        test_down_category = main_cat_down_cats[2]
        assert down_category[0] == test_down_category[0]
        assert down_category[1] == test_down_category[1]
        assert down_category[2] == test_down_category[2]
        # other category present in db:  520 |     2 | Sandwichs au fromage
        # example down cat : 152702 Sandwichs au chèvre: 5 produits
        # example product_id_no_cat : 31140 Sandwich Fromage et Oignon   Marque: Marks & Spencer
        cat_in_db = category.Category(520, 2, "Sandwichs au fromage", self.MAIN_CAT.products_id)
        down_categories, products_id_no_category = cat_in_db.found_down_categories()
        # nbre of down categories
        CURSOR.execute(QUERY_PRODUCT_CATEGORY, (520,))
        test_products_id = []
        for product_id in CURSOR:
            test_products_id.append(product_id[0])
        categories_id = []
        for test_product_id in test_products_id:
            CURSOR.execute(QUERY_CATEGORY_PRODUCT, (test_product_id,))
            for category_id in CURSOR:
                categories_id.append(category_id[0])
        categories_level_3 = []
        CURSOR.execute(QUERY_CATEGORY_ID, (3,))
        for category_id in CURSOR:
            categories_level_3.append(category_id[0])
        test_categories_id = []
        for cat_level_3 in categories_level_3:
            if cat_level_3 in categories_id:
                test_categories_id.append(cat_level_3)
        assert len(down_categories) == len(test_categories_id)
        #  for one down category
        down_categories_id = []
        down_categories_name = []
        for down_category in down_categories:
            down_categories_id.append(down_category[0])
            down_categories_name.append(down_category[1])
        assert 152702 in down_categories_id
        assert "Sandwichs au chèvre" in down_categories_name
        # nbre products without down categories
        CURSOR.execute(QUERY_PRODUCT_CATEGORY_COUNT, (152702,))
        for nbre_products_id in CURSOR:
            nbre_products = nbre_products_id[0]
        assert nbre_products == 5
        assert 31140 in products_id_no_category
