from os import path
import json
from utils import memoized


@memoized
def _data():
    with open(path.join(path.dirname(__file__), "data.json"), 'r') as file:
        tmp = json.load(file)
    return tmp
