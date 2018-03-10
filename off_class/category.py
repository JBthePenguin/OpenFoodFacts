#! /usr/bin/env python3
# coding: utf-8

""" Module with class Category"""

""" imports all necessary modules"""
# import from third party modules
import mysql.connector

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
# to SELECT all products id, name, brands in Product -> main category
QUERY_ALL_PRODUCT = ("SELECT id FROM Product ")
# to SELECT count(CategoryProduct.product_id) with category_id
QUERY_PRODUCT_CATEGORY_COUNT = ("SELECT count(product_id) FROM CategoryProduct "
                            "WHERE category_id = %s")
# to SELECT CategoryProduct.product_id with category_id
QUERY_PRODUCT_CATEGORY = ("SELECT product_id FROM CategoryProduct "
                            "WHERE category_id = %s")
# to SELECT CategoryProduct.category_id with product_id
QUERY_CATEGORY_PRODUCT = ("SELECT category_id FROM CategoryProduct "
                            "WHERE product_id = %s")
# to SELECT Category.id with level
QUERY_CATEGORY_ID = ("SELECT id, name FROM Category "
                  "WHERE level = %s")
# to SELECT Category.name with id and level
QUERY_CATEGORY_NAME = ("SELECT name FROM Category "
                  "WHERE id = %s AND level = %s")


class Category():
    """class  Category : request  DB when methods are called"""
    def __init__(self, cat_id, level, name, products_id_available=None):
        """create object with a:
        Default setting for main category -> App
        - cat_id : int  (or 'M' for main category)
        - level : int -> 1 to ... 1 means main category, 2 donwn category...
        - name : str
        - products_id : list(product_id)
        """
        self.cat_id = cat_id
        self.level = level
        self.name = name
        # Found products inside self
        products_id = []
        if cat_id == "M":
            CURSOR.execute(QUERY_ALL_PRODUCT, ())
            for product_id in CURSOR:
                products_id.append(product_id[0])
        else:
            CURSOR.execute(QUERY_PRODUCT_CATEGORY, (cat_id,))
            for product_id in CURSOR:
                if product_id[0] in products_id_available:
                    products_id.append(product_id[0])
        self.products_id = products_id


    def found_down_categories(self):
        """ Method to found down_categories in self
        return a list of down_categories  : [(id, name, nbre_products]
        and after 1st choice, and for all other down categories for after,
        return also a list of products id not inside a down category"""
        down_categories = []
        down_categories_id_name = []
        if self.cat_id == "M":
            # Application: down categories -> all categories level 1
            CURSOR.execute(QUERY_CATEGORY_ID, (1,))
            for (cat_id, cat_name) in CURSOR:
                down_categories_id_name.append((cat_id, cat_name))
            for down_category_id_name in down_categories_id_name:
                CURSOR.execute(QUERY_PRODUCT_CATEGORY_COUNT, (down_category_id_name[0],))
                for nbre_products_id in CURSOR:
                    down_categories.append(
                        (down_category_id_name[0], down_category_id_name[1], nbre_products_id[0])
                    )
            return down_categories
        # main category after 1st choice
        # and for all other down categories for after
        down_categories_id = []
        for product_id in self.products_id:
            CURSOR.execute(QUERY_CATEGORY_PRODUCT, (product_id,))
            for category_id in CURSOR:
                if category_id[0] not in down_categories_id:
                    down_categories_id.append(category_id[0])
        for down_category_id in down_categories_id:
            try:
                CURSOR.execute(QUERY_CATEGORY_NAME, (down_category_id, (self.level + 1)))
            except mysql.connector.errors.DatabaseError:
                pass
            else:
                for cat_name in CURSOR:
                    down_categories_id_name.append((down_category_id, cat_name[0]))
        # nbre of products calculate with products available
        products_id_added = []
        for down_category_id_name in down_categories_id_name:
            nbre_products = 0
            CURSOR.execute(QUERY_PRODUCT_CATEGORY, (down_category_id_name[0],))
            for product_id in CURSOR:
                if product_id[0] in self.products_id:
                    nbre_products += 1
                    if product_id[0] not in products_id_added:
                        products_id_added.append(product_id[0])
            down_category = (down_category_id_name[0], down_category_id_name[1], nbre_products)
            down_categories.append(down_category)
        products_id_no_category = []
        for product_id in self.products_id:
            if product_id not in products_id_added:
                products_id_no_category.append(product_id)
        return down_categories, products_id_no_category
