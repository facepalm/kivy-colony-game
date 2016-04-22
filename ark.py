
from structure import Structure
import util

class Ark(Structure):

    recipes = [{'unobtanium':1000000, 'antimatter':1000, 'computronium':1000}] 

    #antimatter: 9E15 J/kg ~ 1E16
    #antimatter containment: 1.21 jiggawatts * 3600 * 24 = 104544 E9 J ~= 1E14 J
    process = [{ 'input': {'antimatter':1}, 
                'output': {'electricity':1E16},
                'period': util.seconds(50,'days') },
                { 'input': {'electricity':1E14}, 
                'output': {},
                'period': util.seconds(1,'day') }]

    def __init__(self, **kwargs):
        super(Ark, self).__init__(**kwargs)
