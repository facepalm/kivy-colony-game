
import random
import numpy as np

#planetary resource model.

# metals silicates hydrates minerals alkalines organics corrosives conductives radioactives nobles
# 777777  AAAAAA    
raw_dist = np.array([ 1.0, 1.0, 1.0, 0.1, 0.1, 0.1, 0.01, 0.01, 0.001, 0.001])
raw_names = ['metals', 'silicates', 'hydrates', 'minerals', 'alkalines', 'organics', 'corrosives', 'conductives', 'radioactives', 'nobles']

class PlanetResources(object):
    def __init__(self,planet):
        self.planet=planet
        self.raw = np.zeros((1,10),dtype=np.float32)
        self.atmo = 0
        self.atmo_type = 'None'
        
        self.raw_dist = raw_dist
        
        if planet.type == 'Planetoid':
            #the most interesting type, planetoids split into VERY diverse categories
            self.raw = np.random.random(10)
            planet.subtype = random.choice('CSXc')
            if planet.subtype == 'C': #carbonaceous, from crust of former planet
                self.raw = np.multiply(self.raw,np.array([0.01,0.1,1,1,0.01,1,1,0.01,0.01,1]))
            elif planet.subtype == 'S': #silicates, from mantle of former planet
                self.raw = np.multiply(self.raw,np.array([0.1,1,0.1,1,0.1,0.1,0.1,0.1,0.1,0.001]))    
            elif planet.subtype == 'X': #metals, from core of former planet
                self.raw = np.multiply(self.raw,np.array([1,0.1,0.01,1,1,0.01,0.01,1,1,0.001]))                    
            else: #c type, chondrites, leave everything as it is
                pass
            if planet.orbit < planet.primary.snow_line:
                self.raw = np.multiply(self.raw,np.array([1,1,0.001,1,1,1,0.01,1,1,0.01]))
                
        elif planet.type == 'Dwarf planet':
            #dwarf planets have raw resources, but no atmo
            self.raw = np.random.random(10)
            if planet.orbit < planet.primary.snow_line:
                self.raw[2] /= 100 #most hydrates boiled off
                self.raw[9] /= 100 #most noble gasses likewise
            #if planet.
        elif planet.type == 'Planet':
            #planets have raw resources, and atmo which can (sometimes) protect them
            self.raw = np.random.random(10)
            self.atmo = random.random() #TODO scale density to planet mass
            self.atmo_type = random.choice(['Organic','Corrosive','Hydrate'])
            if planet.orbit < planet.primary.snow_line and self.atmo < 0.1:
                self.raw[2] /= 10 #most hydrates boiled off
                self.raw[9] /= 10 #most noble gasses likewise
        elif planet.type == 'Gas giant':
            #giants are just atmosphere
            self.atmo = 1
            self.atmo_type = random.choice(['Volatile']) #TODO: ice giant atmospheres, if mining ever added
        else: #brown dwarf, nothing that can be reached
            pass
            
            
