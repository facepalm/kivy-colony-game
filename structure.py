
import util

class Structure(object):
    recipes = [{'Unobtanium':1}] #Contains a number of possible recipes for the creation of this structure

    process = { 'input': {}, 
                'output': {},
                'period': util.seconds(1,'day') }

    def __init__(self,**kwargs):
        self.built=False
        self.recipe = None
        self.components = None
        
        
    def build(self, resources=None, free=False):
        if free or self.built:
            self.built = True
            return resources
        
        for r in recipes:
            if resources.check(self.recipes[r]):
                self.recipe = r
                break
        
        if not self.recipe:
            return resources
            
        test, self.components = resources.sub(self.recipes[self.recipe])
        
        if test: self.built = True
        
        return resources
