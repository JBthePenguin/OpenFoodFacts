#! /usr/bin/env python3
# coding: utf-8

""" Tests for module input_user """

""" imports all necessary modules"""
import sys
sys.path.append('..')

# import local modules
from off_function import input_user


class TestInputUser:
    """ Tests for function """
    MSG = "Taper 1, 2"

    def test_found_input_msg_ch_b(self):
        """ Test if msg and nbre_choice are ok for all cmbination"""
        msg, nbre_choice = input_user.found_input_msg_ch_b(False, False)
        assert msg == "".join([self.MSG, " ou 3 (puis entrée): "])
        assert nbre_choice == 3
        
        msg, nbre_choice = input_user.found_input_msg_ch_b(True, False)
        assert msg == "".join([self.MSG, ", 3 ou 4 (puis entrée): "])
        assert nbre_choice == 4

        msg, nbre_choice = input_user.found_input_msg_ch_b(False, True)
        assert msg == "".join([self.MSG, " ou 3 (puis entrée): "])
        assert nbre_choice == 3

        msg, nbre_choice = input_user.found_input_msg_ch_b(True, True)
        assert msg == "".join([self.MSG, ", 3, 4 ou 5 (puis entrée): "])
        assert nbre_choice == 5
