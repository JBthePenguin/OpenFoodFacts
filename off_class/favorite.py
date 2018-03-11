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
# to INSERT datas INTO table CategoryProduct
ADD_FAVORITE = ("INSERT INTO Favorite "
                        "(product_id, substitute_id) "
                        "VALUES (%s, %s)")


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
		return msg

