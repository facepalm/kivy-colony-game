
from structure import Structure
import util

class Ark(Structure):

    recipes = [{'unobtanium':1000000, 'antimatter':1000, 'computronium':1000}] 

    #antimatter: 9E15 J/kg ~ 1E16
    #antimatter containment: 1.21 jiggawatts * 3600 * 24 = 104544 E9 J ~= 1E14 J
    process =  [{   'name' : 'Power (Antimatter)', 
                    'input': {'antimatter':1}, 
                    'output': {'electricity':1E16},
                    'period': util.seconds(50,'days') },
                
                {   'name' : 'Antimatter Containment',
                    'input': {'electricity':1E14}, 
                    'output': {},
                    'period': util.seconds(1,'day') },
                    
                {   'name' : 'Remote Exploration',
                    'input' : {'electricity':1E2},
                    'output' : {'Exploration (System)' : 0.01 },
                    'period': util.seconds(1,'year') }
               ]

    def __init__(self, **kwargs):
        if not 'imagename' in kwargs:
            kwargs['imagename'] = 'Ark'
        super(Ark, self).__init__(**kwargs)
        self.occupation_level = 3
