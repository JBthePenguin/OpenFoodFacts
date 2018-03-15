#! /usr/bin/env python3
# coding: utf-8

""" Modules with application's functions needed for input user"""
from . import display


# INPUT
def save_input_user(input_msg, nbre_choice, with_quit):
    """ valid the input user before return it"""
    choice = ""
    while choice == "":
        choice = input(input_msg)
    try:
        int(choice[0])  # except negative number
    except ValueError:
        if (with_quit is False) or (choice != "q"):
            choice = False
    else:
        if choice != "q":
            choice = int(choice)
            if choice > nbre_choice:
                choice = False
    return choice


def found_input_msg_ch_b(with_new_down_cat, with_prods_id_no_cat):
    """ found the message for the input choice b with:
    - with_new_down_cat : True or False
    - with_prods_id_no_cat: True or False
    return:
    - msg : message for input user corresponding with user choice
    - nbre_choice : number of possible choice"""
    msg = "Taper 1"
    if with_new_down_cat is True:
        if with_prods_id_no_cat is True:
            nbre_choice = 4
            msg = "".join([msg, ", 2, 3 ou 4 (puis entrée): "])
        else:
            nbre_choice = 3
            msg = "".join([msg, ", 2 ou 3 (puis entrée): "])
    else:
        nbre_choice = 2
        msg = "".join([msg, " ou 2 (puis entrée): "])
    return msg, nbre_choice
