#! /usr/bin/env python3
# coding: utf-8

""" imports all necessary modules"""

class Category():
    """class  Category"""
    def __init__(self, cat_id, level, name):
        """create object with a:
        - id : int
        - level : int -> 1 to ... 1 means main category, 2 donwn category...
        - name : str
        """
        self.id = cat_id
        self.level = level
        self.name = name


    def found_products_id(self, cursor, query_category_product):
        """ Method to found products in self
        return a list of product_id """
        products = []
        cursor.execute(query_category_product, (self.id,))
        for id_product in cursor:
            product_id = id_product[0]
            products.append(product_id)
        return products


    def found_nbre_products(self, cursor, query_category_product):
        """ Method found the number of product in self 
        before return it"""
        return len(self.found_products_id(cursor, query_category_product))

    
    def found_down_categories(
        self, products, cursor, query_category, query_category_product):
        """ Method to found down_categories in self
        return a list of down_categories id """
        all_categories_id = []
        for product_id in products:
            cursor.execute(query_category_product, (product_id,))
            for category_id in cursor:
                id_category = category_id[0]
                all_categories_id.append(id_category)
        cursor.execute(query_category, ((self.level+1),))
        down_categories = []
        for (cat_id, cat_level, cat_name) in cursor:
            if cat_id in all_categories_id:
                selected_category = Category(cat_id, cat_level, cat_name)
                down_categories.append(selected_category)
        return down_categories
