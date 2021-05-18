import os
from .glidenumber.desc import descriptionscrap
import json

def getglidenumber(start, end, country):

    item = descriptionscrap(country, start, end)

    '''
    ##############################################################
    #ITEMS ARE NOW AVAILABLE AS LIST OF DICTIONARIES IN THIS FILE#
    ##############################################################
    '''

    return item

if __name__ == '__main__':
    getdetails()