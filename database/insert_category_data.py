#! /usr/bin/env python3
# coding: utf-8

""" import all necessary modules
    make request to pick up all categories available to OpenfoodFacts API
    and insert data in db"""

# pylint: disable=no-name-in-module
# import from third party modules
import json
import requests
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
# to INSERT datas INTO table Category
ADD_CATEGORY = ("INSERT INTO Category "
                "(level, name, url_link) "
                "VALUES (%s, %s, %s)")

# Make a list of available categories
REQUEST = requests.get(
    "https://fr.openfoodfacts.org/langue/francais/categories.json"
)
RESPONSE = REQUEST.json()
CATEGORIES = RESPONSE["tags"]
NBRE_CATEGORIES_SAVED = 0
ERROR_INSERT = 0

for category in CATEGORIES:
    # make request to get a list of products
    url = "".join([category["url"], ".json"])
    request = requests.get(url)
    try:
        response = request.json()
    except json.decoder.JSONDecodeError:
        ERROR_INSERT += 1
    else:
        try:
            products = response["products"]
        except KeyError:
            ERROR_INSERT += 1
        else:
            # get the first product
            try:
                product = products[0]
            except IndexError:
                ERROR_INSERT += 1
            else:
                # get the category hierarchy
                try:
                    categories_hierarchy = product["categories_hierarchy"]
                except IndexError:
                    ERROR_INSERT += 1
                else:
                    # found the level of category
                    level = 1
                    for category_id in categories_hierarchy:
                        if category_id == category["id"]:
                            # insert category in db
                            CURSOR.execute(ADD_CATEGORY, (level, category["name"], category["url"]))
                            CNX.commit()
                            NBRE_CATEGORIES_SAVED += 1
                            print("".join([
                                "level ",
                                str(level),
                                " -> ",
                                category["name"],
                                "  saved in db"
                            ]))
                            print("".join([
                                "  saved: ",
                                str(NBRE_CATEGORIES_SAVED),
                                "    error: ",
                                str(ERROR_INSERT)
                            ]))
                        level += 1
