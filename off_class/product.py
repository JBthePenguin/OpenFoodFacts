#! /usr/bin/env python3
# coding: utf-8

""" Module with class Product """

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
# to SELECT Product.* with id
QUERY_PRODUCT = (
    "SELECT name, brands, nutrition_grade, url_link, description, stores   FROM Product "
    "WHERE id = %s"
)
# to SELECT Product.nutrition_grade with id:
QUERY_PRODUCT_NG = ("SELECT nutrition_grade FROM Product "
                    "WHERE id = %s")
# to SELECT CategoryProduct.category_id with product_id
QUERY_CATEGORY_PRODUCT = ("SELECT category_id FROM CategoryProduct "
                          "WHERE product_id = %s")
# to SELECT CategoryProduct.product_id with category_id
QUERY_PRODUCT_CATEGORY = ("SELECT product_id FROM CategoryProduct "
                          "WHERE category_id = %s")
# to SELECT Category.level with id and level
QUERY_CATEGORY_LEVEL = ("SELECT level FROM Category "
                       "WHERE id = %s")


class Product():
    """" class Product : request  DB to get data to init"""
    def __init__(self, id_prod):
        """ create object with id_prod
        - nutrition grade OpenFoodFacts : str -> 'a' for good to 'e' for bad
        - name : str
        - link to OFF's page : str
        - description of ingredients : str
        - stores where the product is available : str
        """
        self.id_prod = id_prod
        CURSOR.execute(QUERY_PRODUCT, (id_prod,))
        for (
                name,
                brands,
                nutrition_grade,
                url_link,
                description,
                stores
        ) in CURSOR:
            self.name = name
            self.brands = brands
            self.nutrition_grade = nutrition_grade
            self.url_link = url_link
            self.description = description
            self.stores = stores


    def found_substitutes(self):
        """ with product's categories {id:level} 
        return a list of possible substitutes [product_id] with grade a"""
        # select categories and and make dict -> {cat_id:level}
        categories = {}
        categories_id = []
        CURSOR.execute(QUERY_CATEGORY_PRODUCT, (self.id_prod,))
        for category_id in CURSOR:
            categories_id.append(category_id[0])
        for category_id in categories_id:
            CURSOR.execute(QUERY_CATEGORY_LEVEL, (category_id,))
            for level in CURSOR:
                categories[category_id] = level[0]
        # make a list of available levels
        categories_level = []
        for key in categories:
            categories_level.append(categories[key])
        # each level appears only once and put the bigest on in first place 
        categories_level = list({level for level in categories_level})
        categories_level.sort(reverse=True)
        # try to found substitues -> begin bigest level, and next one, ...
        # stop if substitute nutri grade A or B founded, or nothing in all categories
        categories_end = False
        substitutes_id = []
        i = 0
        while categories_end is False:
            possible_substitutes_id = []
            for key in categories:
                if categories[key] == categories_level[i]:
                    CURSOR.execute(QUERY_PRODUCT_CATEGORY, (key,))
                    for product_id in CURSOR:
                        if product_id[0] != self.id_prod:
                            possible_substitutes_id.append(product_id[0])
            if possible_substitutes_id != []:
                # select substitute with nutrition grade A or B
                for possible_substiute_id in possible_substitutes_id:
                    CURSOR.execute(QUERY_PRODUCT_NG, (possible_substiute_id,))
                    for product_ng in CURSOR:
                        if product_ng[0].lower() == "a": # or (product_ng[0].lower() == "b"):
                            substitutes_id.append(possible_substiute_id)
                if substitutes_id != []:
                    categories_end = True
            i += 1
            if i == len(categories_level):
                categories_end = True
        return substitutes_id
