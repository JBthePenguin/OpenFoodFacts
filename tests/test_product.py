#! /usr/bin/env python3
# coding: utf-8

""" Tests for module produt """

""" imports all necessary modules"""
import sys
import mysql.connector
# import local modules
from off_class import product

sys.path.append('..')

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
    "SELECT id, name, brands, nutrition_grade, url_link, description, stores   FROM Product "
    "WHERE id = %s"
)



class TestProduct:
    """ Tests for class Product"""
    PRODUCT_TEST = product.Product(29910)
    
    def test_product_init(self):
        """ Test if the int of class Product is ok"""
        CURSOR.execute(QUERY_PRODUCT, (29910,))
        for (prod_id, name, brands, nutrition_grade, url_link, description, stores) in CURSOR:
            assert self.PRODUCT_TEST.id_prod == prod_id
            assert self.PRODUCT_TEST.name == name
            assert self.PRODUCT_TEST.brands == brands
            assert self.PRODUCT_TEST.nutrition_grade == nutrition_grade
            assert self.PRODUCT_TEST.url_link == url_link
            assert self.PRODUCT_TEST.description == description
            assert self.PRODUCT_TEST.stores == stores

    def test_found_subsitutes(self):
        """ Test if product_id 149, 181, 185, 533 are in subtitutes_id list"""
        substitutes_id_test = self.PRODUCT_TEST.found_substitutes()
        assert 149 in substitutes_id_test
        assert 181 in substitutes_id_test
        assert 185 in substitutes_id_test
        assert 533 in substitutes_id_test
        assert 5616 not in substitutes_id_test
        assert 75771 not in substitutes_id_test
        assert 75793 not in substitutes_id_test
        assert 58751 not in substitutes_id_test

