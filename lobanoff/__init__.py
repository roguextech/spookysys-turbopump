"""Implements first-guess methods from Lobanoff's Centrigugal Pumps book"""
from os import path
import json

with open(path.join(__path__[0], "data.json"), 'r') as file:
    JSONDATA = json.load(file)
