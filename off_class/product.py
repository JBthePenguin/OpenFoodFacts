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
    user="OpenFoodFactsApp", password='BonAppetit', host="127.0.0.1", database="db_openfoodfacts")
CURSOR = CNX.cursor()
## Query Models
# to SELECT Product.* with id
QUERY_PRODUCT = (
    "SELECT name, brands, nutrition_grade, url_link, description, stores   FROM Product "
    "WHERE id = %s"
)


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
