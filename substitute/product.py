#! /usr/bin/env python3
# coding: utf-8

""" imports all necessary modules"""

class Product():
    """" class Product : instance build with an product from OpenFoodFacts, """
    def __init__(
            self, id_prod, name, brands, nutrition_grade,
            url_link, description, stores):
        """ create object with :
        - id_prod
        - nutrition grade OpenFoodFacts : str -> 'a' for good to 'e' for bad
        - name : str
        - link to OFF's page : str
        - description of ingredients : str
        - stores where the product is available : str """
        self.id = id_prod
        self.name = name
        self.brands = brands
        self.nutrition_grade = nutrition_grade
        self.url_link = url_link
        self.description = description
        self.stores = stores
