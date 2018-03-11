#! /usr/bin/env python3
# coding: utf-8

""" import all necessary modules
    connect to database
    make request to pick information to OpenfoodFacts API
    and put only necessary informations in database"""

# pylint: disable=no-name-in-module
# import from third party modules
import requests
import mysql.connector

# pylint: disable=too-many-return-statements
def pick_up_infos(product_off):
    """pick up needed infos of a product in all OpenFoodFacts's infos"""
    try:
        categories = product_off["categories_hierarchy"]
    except KeyError:
        return 0, []
    if categories == []:
        return 0, []
    try:
        brands = product_off["brands"]
    except KeyError:
        return 0, []
    if brands == "":
        return 0, []
    try:
        name = product_off["product_name_fr"]
    except KeyError:
        return 0, []
    if name == "":
        return 0, []
    try:
        nutrition_grade = product_off["nutrition_grade_fr"]
    except KeyError:
        return 0, []
    try:
        url_link = product_off["url"]
    except KeyError:
        return 0, []
    if url_link == "":
        return 0, []
    try:
        description = product_off["ingredients_text_fr"]
    except KeyError:
        return 0, []
    if description == "":
        return 0, []
    try:
        stores = product_off["stores"]
    except KeyError:
        stores = ""
    datas = (name, brands, nutrition_grade, url_link, description, stores)
    return datas, categories

# set the url with country and language if you want to eat like an english man :(
URL = "http://fr.openfoodfacts.org/language/francais/"

###
# DATABASE
###
## Connexion
# to DataBase
CNX = mysql.connector.connect(
    user="OpenFoodFactsApp", password='BonAppetit', host="127.0.0.1", database="db_openfoodfacts")
CURSOR = CNX.cursor()
## Models
# to INSERT datas INTO tables Product, Category, CategoryProduct ###
ADD_PRODUCT = ("INSERT INTO Product "
               "(name, brands, nutrition_grade, url_link, description, stores) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
ADD_CATEGORY = ("INSERT INTO Category "
                "(level, name) "
                "VALUES (%s, %s)")
ADD_CATEGORY_PRODUCT = ("INSERT INTO CategoryProduct "
                        "(category_id, product_id) "
                        "VALUES (%s, %s)")
# to SELECT Category.id and Product.id
QUERY_CATEGORY = ("SELECT id FROM Category "
                  "WHERE level = %s AND name = %s")
QUERY_PRODUCT = ("SELECT id FROM Product "
                 "WHERE name = %s AND brands = %s")

## Pick up categories and products with necessary informations
# make a dict with all categories avalaibles on OpenFoodFacts
CATEGORIES = {}
REQUEST = requests.get(URL + "categories.json")
RESPONSE = REQUEST.json()
TAGS = RESPONSE["tags"]
for category in TAGS:
    CATEGORIES[category["id"]] = category["name"]
# make request to get a list of products for each page
PAGE_NUMBER = 1
NEW_REQUEST = 1
while NEW_REQUEST == 1:
    NEW_URL = URL + str(PAGE_NUMBER) + ".json"
    NEW_RESPONSE = requests.get(NEW_URL)
    NEW_RESPONSE = NEW_RESPONSE.json()
    PAGE_PRODUCTS = NEW_RESPONSE["products"]
    if PAGE_PRODUCTS != []:
        for product in PAGE_PRODUCTS:
            data_product, categories_hierarchy = pick_up_infos(product)
            if (data_product != 0) and (categories_hierarchy != []):
                # if the product have all informations except stores
                # insert datas in Product
                try:
                    CURSOR.execute(ADD_PRODUCT, data_product)
                except mysql.connector.errors.IntegrityError:
                    pass
                else:
                    # insert datas in Category
                    i = 1
                    for category in categories_hierarchy:
                        try:
                            data_category = (i, CATEGORIES[category])
                        except KeyError:
                            pass
                        else:
                            try:
                                CURSOR.execute(ADD_CATEGORY, data_category)
                            except mysql.connector.errors.IntegrityError:
                                pass
                            # insert datas in CategoryProduct
                            try:
                                CURSOR.execute(QUERY_CATEGORY, data_category)
                            except mysql.connector.errors.DatabaseError:
                                pass
                            else:
                                for id_category in CURSOR:
                                    category_id = id_category[0]
                                try:
                                    CURSOR.execute(
                                        QUERY_PRODUCT, (data_product[0], data_product[1]))
                                except mysql.connector.errors.DatabaseError:
                                    pass
                                else:
                                    for id_product in CURSOR:
                                        product_id = id_product[0]
                                    try:
                                        CURSOR.execute(
                                            ADD_CATEGORY_PRODUCT, (category_id, product_id))
                                    except mysql.connector.errors.IntegrityError:
                                        pass
                                    else:
                                        CNX.commit()
                        i += 1
        print("OK !! page " + str(PAGE_NUMBER) + " saved in DB !!")
        PAGE_NUMBER += 1
    else:
        NEW_REQUEST = 0

CNX.close()
