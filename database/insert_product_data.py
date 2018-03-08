#! /usr/bin/env python3
# coding: utf-8

""" import all necessary modules
    make request to pick up all product's information for each category
    insert data in database : Tables Product, CategoryProduct"""

# pylint: disable=no-name-in-module
# import from third party modules
import json
import requests
import mysql.connector


def pick_up_infos(product_off):
    """pick up needed infos of a product in all OpenFoodFacts's infos
    return a tuple with necessaries infos for insert in db"""
    product_app = 0
    info_error = False
    while info_error is False:
        try:
            brands = product_off["brands"]
        except KeyError:
            break
        if brands == "":
            break
        try:
            name = product_off["product_name"]
        except KeyError:
            break
        if name == "":
            break
        try:
            nutrition_grade = product_off["nutrition_grades"]
        except KeyError:
            break
        if nutrition_grade == "":
            break
        try:
            url = product_off["url"]
        except KeyError:
            break
        if url == "":
            break
        try:
            description = product_off["ingredients_text"]
        except KeyError:
            break
        if description == "":
            break
        try:
            stores = product_off["stores"]
        except KeyError:
            stores = ""
        product_app = (
            name,
            brands,
            nutrition_grade,
            url,
            description,
            stores
        )
        break
    return product_app


###
# DATABASE
###
## Connexion
# to DataBase
CNX = mysql.connector.connect(
    user="OpenFoodFactsApp", password='BonAppetit', host="127.0.0.1", database="db_openfoodfacts")
CURSOR = CNX.cursor()
## Models
# to INSERT datas INTO table Product
ADD_PRODUCT = ("INSERT INTO Product "
               "(name, brands, nutrition_grade, url_link, description, stores) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
# to INSERT datas INTO table CategoryProduct
ADD_CATEGORY_PRODUCT = ("INSERT INTO CategoryProduct "
                        "(category_id, product_id) "
                        "VALUES (%s, %s)")
QUERY_PRODUCT = ("SELECT id FROM Product "
                 "WHERE name = %s AND brands = %s")
# to SELECT id and url_link From Category
QUERY_CATEGORY = ("SELECT id, url_link FROM Category ")

# make a list of categories saved in db
CURSOR.execute(QUERY_CATEGORY, ())
CATEGORIES = []
for (category_id, url_link) in CURSOR:
    category = {
        "category_id": category_id,
        "url_link": url_link
    }
    CATEGORIES.append(category)

ERROR_INSERT = 0
CAT_NUMBER = 0
for category in CATEGORIES:
    CAT_NUMBER += 1
    new_request = True
    page_number = 0
    # for each page
    while new_request is True:
        page_number += 1
        new_url = "".join([category["url_link"], "/", str(page_number), ".json"])
        # make request to get a list of products
        request = requests.get(new_url)
        try:
            response = request.json()
        except json.decoder.JSONDecodeError:
            ERROR_INSERT += 1
            new_request = False
            print("".join(["JSONDecodeError for ", new_url]))
        else:
            try:
                products = response["products"]
            except KeyError:
                ERROR_INSERT += 1
                new_request = False
                print("".join(["KeyError for ", new_url]))
            else:
                if products == []:
                    new_request = False
                else:
                    # get necessary infos for each product
                    for product in products:
                        new_product = pick_up_infos(product)
                        if new_product == 0:
                            ERROR_INSERT += 1
                        else:
                            try:
                                # insert data in Product
                                CURSOR.execute(ADD_PRODUCT, new_product)
                            except mysql.connector.errors.IntegrityError:
                                # continue to save association in CategoryProduct
                                pass
                            else:
                                CNX.commit()
                                print("a new product SAVED")
                            try:
                                CURSOR.execute(QUERY_PRODUCT, (new_product[0], new_product[1]))
                            except mysql.connector.errors.DatabaseError:
                                ERROR_INSERT += 1
                            else:
                                for id_product in CURSOR:
                                    product_id = id_product[0]
                                try:
                                    # insert data in CategoryProduct
                                    CURSOR.execute(
                                        ADD_CATEGORY_PRODUCT, (category["category_id"], product_id)
                                    )
                                except mysql.connector.errors.IntegrityError:
                                    ERROR_INSERT += 1
                                else:
                                    CNX.commit()
                                    print("".join([
                                        "new association  cat : ",
                                        str(category["category_id"]),
                                        "  prod: ",
                                        str(product_id),
                                        " SAVED"
                                    ]))
                    print("".join([
                        "\nproducts of category number ",
                        str(CAT_NUMBER),
                        "    page ",
                        str(page_number),
                        "  SAVED\n"
                    ]))
print("".join(["DB is READY with only ", str(ERROR_INSERT), " ERROR during INSERT" ]))
