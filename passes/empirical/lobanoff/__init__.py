print(__name__)
import json
from os import path


with open(path.join(__path__[0], "data.json")) as file:
    DATA = json.load(file)
    print(DATA["book"])

