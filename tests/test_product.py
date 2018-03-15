#! /usr/bin/env python3
# coding: utf-8

""" Tests for module produt """

""" imports all necessary modules"""
import sys
sys.path.append('..')

# import local modules
from off_class import product


class TestProduct:
    """ Tests for class Product"""
    PRODUCT_TEST = product.Product(29910)
    
    def test_product_init(self):
        """ Test if the int of class Product is ok"""
        assert self.PRODUCT_TEST.id_prod == 29910
        assert self.PRODUCT_TEST.name == "Chocolat Crémeux Amère - Chocolat Noir 55% Cacao"
        assert self.PRODUCT_TEST.brands == "Primola"
        assert self.PRODUCT_TEST.nutrition_grade == "e"
        assert self.PRODUCT_TEST.url_link == "".join([
            "https://fr.openfoodfacts.org/produit/5941047824431",
            "/chocolat-cremeux-amere-chocolat-noir-55-cacao-pri"
        ])
        assert self.PRODUCT_TEST.description == "".join([
            "Sucre, pâte de cacao, beurre de cacao, cacao maigre en poudre, ",
            "graisse végétale (palme, karité), émulsifiants (lécithine de _soja_), arôme."
        ])
        assert self.PRODUCT_TEST.stores == "Noz"

    def test_found_subsitutes(self):
        """ Test if product_id 149, 181, 185, 533 are in subtitutes_id list"""
        substitutes_id_test = self.PRODUCT_TEST.found_substitutes()
        assert 149 in substitutes_id_test
        assert 181 in substitutes_id_test
        assert 185 in substitutes_id_test
        assert 533 in substitutes_id_test
