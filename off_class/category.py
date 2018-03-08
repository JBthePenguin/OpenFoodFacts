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
    user="OpenFoodFactsApp", password='BonAppetit', host="127.0.0.1", database="db_openfoodfacts")
CURSOR = CNX.cursor()
## Query Models
# to SELECT all products in Product -> main category
QUERY_ALL_PRODUCT = ("SELECT id FROM Product ")
# to SELECT Product.name and Product.brands with id
QUERY_PRODUCT = ("SELECT name, brands FROM Product "
                 "WHERE id = %s")
# to SELECT CategoryProduct.product_id with category_id
QUERY_PRODUCT_CATEGORY = ("SELECT product_id FROM CategoryProduct "
                            "WHERE category_id = %s")
# to SELECT CategoryProduct.category_id with product_id
QUERY_CATEGORY_PRODUCT = ("SELECT category_id FROM CategoryProduct "
                            "WHERE product_id = %s")
# to SELECT Category.* with level
QUERY_CATEGORY = ("SELECT id, level, name FROM Category "
                  "WHERE level = %s")


class Category():
    """class  Category : request  DB when methods are called"""
    def __init__(self, cat_id, level, name):
        """create object with a:
        Default setting for main category -> App
        - cat_id : int  (or 'M' for main category)
        - level : int -> 1 to ... 1 means main category, 2 donwn category...
        - name : str
        - products_id : list( id of products)
        - products_brands : {products_id: 'name brands'}
        """
        self.cat_id = cat_id
        self.level = level
        self.name = name
        self.products_id = []
        self.products_brands = {}


    def found_products_id(self):
        """ Method to found products in self
        update the list of product_id and products_brands -> display"""
        if self.cat_id == "M":
            CURSOR.execute(QUERY_ALL_PRODUCT, ())
        else:
            CURSOR.execute(QUERY_PRODUCT_CATEGORY, (self.cat_id,))
        for id_product in CURSOR:
            product_id = id_product[0]
            self.products_id.append(product_id)
        if self.cat_id != "M":
            for product_id in self.products_id:
                CURSOR.execute(QUERY_PRODUCT, (product_id,))
                for (name, brands) in CURSOR:
                    product_brand = "".join([name, "        marque: ", brands])
                    self.products_brands[product_id] = product_brand


    def found_down_categories(self):
        """ Method to found down_categories in self
        return a list of down_categories id """
        down_categories_id = []
        if self.cat_id == "M":
            CURSOR.execute(QUERY_CATEGORY, (1,))
            for category_id in CURSOR:
                new_category_id = category_id[0]
                down_categories_id.append(new_category_id)   
        else:
            for product_id in self.products_id:
                CURSOR.execute(
                    QUERY_CATEGORY_PRODUCT, (product_id,)
                )
                for category_id in CURSOR:
                    new_category_id = category_id[0]
                    append_id = True
                    for down_category_id in down_categories_id:
                        if down_category_id == new_category_id:
                            append_id = False
                    if append_id is True: 
                        down_categories_id.append(new_category_id)
        down_categories = []
        try:
            CURSOR.execute(QUERY_CATEGORY, ((self.level+1),))
        except mysql.connector.errors.DatabaseError:
            pass
        else:
            for (cat_id, cat_level, cat_name) in CURSOR:
                if cat_id in down_categories_id:
                    down_category = Category(cat_id, cat_level, cat_name)
                    down_categories.append(down_category)
            # update products_id
            for down_category in down_categories:
                down_category.found_products_id()
        return down_categories

    def update_products_id(self, products_id_available):
        """ update down categories's list of products'id
        with id available"""
        new_products_id = []
        for product_id in self.products_id:
            for product_id_available in products_id_available:
                if product_id == product_id_available:
                    new_products_id.append(product_id)
        self.products_id = new_products_id
        # update products brands
        self.product_brand = {}
        for product_id in self.products_id:
            CURSOR.execute(QUERY_PRODUCT, (product_id,))
            for (name, brands) in CURSOR:
                product_brand = "".join([name, "        marque: ", brands])
                self.products_brands[product_id] = product_brand

