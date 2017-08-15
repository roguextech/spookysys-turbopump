"""Implements first-guess methods from Lobanoff's Centrigugal Pumps book"""
from os import path
import json
from misc import memoized


@memoized
def _jsondata():
    with open(path.join(path.dirname(__file__), "data.json"), 'r') as file:
        tmp = json.load(file)
    return tmp


def do_metric():
    pass
