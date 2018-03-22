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
# to INSERT datas INTO table Favorite
ADD_FAVORITE = ("INSERT INTO Favorite "
                "(product_id, substitute_id) "
                "VALUES (%s, %s)")
DELETE_FAVORITE = ("DELETE FROM Favorite "
                   "WHERE product_id = %s AND substitute_id = %s")
# to SELECT * in Favorite ->
QUERY_ALL_FAVORITE = ("SELECT product_id, substitute_id FROM Favorite ")


class Favorite():
    """docstring for Favorite"""
    def __init__(self, product_id=None, substitute_id=None):
        """init Favorite: association product_id subtitute_id """
        self.product_id = product_id
        self.substitute_id = substitute_id


    def save_in_db(self):
        """ method to save favorite in DB """
        try:
            CURSOR.execute(ADD_FAVORITE, (self.product_id, self.substitute_id))
        except mysql.connector.errors.IntegrityError:
            # Favorite already saved
            msg = "Ce Favori a déjà été enregistré"
        except mysql.connector.errors.DatabaseError:
            msg = "Problème !!! Favori non enregistré"
        else:
            CNX.commit()
            msg = "Enregistrement du Favori effectué"
        print(msg)

    
    def delete_in_db(self):
        """method to delete favorite in db"""
        try:
            CURSOR.execute(DELETE_FAVORITE, (self.product_id, self.substitute_id))
        except mysql.connector.errors.DatabaseError:
            msg = "Problème lors de l'effacement"
        else:
            CNX.commit()
            msg = "Suppression du Favori effectué"
        print(msg)



def found_favorites():
    """ function called to found favorites saved in db
    and return a list of favorites : [(product_id, substitute_id)]"""
    favorites = []
    CURSOR.execute(QUERY_ALL_FAVORITE, ())
    for (product_id, substitute_id) in CURSOR:
        favorites.append((product_id, substitute_id))
    return favorites
