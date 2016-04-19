
import util
import globalvars

class Structure(object):
    recipes = [{'unobtanium':1}] #Contains a number of possible recipes for the creation of this structure

    process = [{ 'input': {}, 
                'output': {},
                'period': util.seconds(1,'day') }]

    def __init__(self,**kwargs):
        self.built=False
        self.recipe = None
        self.composition = None
        
        self.site=None
        
        util.register(self)
        
        
    def build(self, resources=None, free=False):
        if self.built: return resources
        if free:
            self.composition = self.recipes[0]
            self.built = True
            return resources
        
        for r in recipes:
            if resources.check(self.recipes[r]):
                self.recipe = r
                break
        
        if not self.recipe:
            return resources
            
        test, self.composition = resources.sub(self.recipes[self.recipe])
        
        if test: self.built = True
        
        return resources
        
    def update(self,dt):
        secs = dt*globalvars.config['TIME FACTOR']
        for p in self.process:        
            timeslice = secs/p['period']  
        
        #run self.process for timeslice seconds     
