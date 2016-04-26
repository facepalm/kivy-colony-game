
import util
import globalvars
import shipimage

class Structure(object):
    recipes = [{'unobtanium':1}] #Contains a number of possible recipes for the creation of this structure

    process = [{ 'input': {}, 
                'output': {},
                'period': util.seconds(1,'day') }]

    def __init__(self,**kwargs):
        self.built=False
        self.recipe = None
        self.composition = None
        
        self.occupation_level = 1
        
        self.site=None
        
        self.image = None
        self.imagename = kwargs['imagename'] if 'imagename' in kwargs else 'Default'
        
        util.register(self)
        
        self.generate_image()
        
        
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
            
            #run p for timeslice seconds     
            #compute inputs, check inputs
            #generate outputs
            #handle outputs
            
            
        if self.site and self.site.planet and self.site.planet.occupied < self.occupation_level:
            self.site.planet.occupied = self.occupation_level                
        
        
    def generate_image(self,clear=False):
        if clear: pass #handle deleting image here
        if self.image is None:
            self.image = shipimage.ShipImage(ship=self, source = shipimage.shipimages[self.imagename])
        
        
        
        
        
