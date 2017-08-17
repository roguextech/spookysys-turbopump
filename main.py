from __future__ import print_function
from matplotlib import pyplot as plt
from CoolProp.CoolProp import PropsSI
import lobanoff
import lobanoff.graphs.generate
from units import ureg


hello = PropsSI('T', 'P', 101325, 'Q', 0, 'Water')
print(hello)
