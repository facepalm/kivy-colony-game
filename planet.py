import numpy as np
import util
import logging
import random



class Planet(object):
    def __init__(self,name=None, logger=None, mass = None):
        self.mass = mass if mass else 1E8*random.random()
        self.name = name if name else util.planet_name(self)
        if logger:
            self.logger = logging.getLogger(logger.name + '.' + self.name)
        else: 
            self.logger = logging.getLogger(util.generic_logger.name + '.' + self.name)
    
        if self.mass > 1E29: 
            self.type = 'INVALID' #actually a sun.  Let the Star init handle this later
        elif self.mass > 1E28: 
            self.type = 'Brown dwarf' #counting this as a planet, since they have negligible radiation    
        elif self.mass > 1E26: 
            self.type = 'Gas giant' #position in orbit will affect gas or ice giant
        elif self.mass > 1E23:
            self.type = 'Planet' #rocky world, but capable of retaining an atmosphere, even if barely
        elif self.mass > 1E21:
            self.type = 'Dwarf Planet' #larger moons and asteroids, rounded
        else:
            self.type = 'Planetoid' #small moons, asteroids, rocks, etc
    
        self.initialize_sites()
        
    def initialize_sites(self):
        self.sites = 6 if self.type == 'Planet' else 2 if self.type == 'Dwarf' else 1 if self.type == 'Planetoid' else 0
        self.orbits = 1
        print self.sites, self.orbits
    
class Star(Planet):
    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)
        
    
if __name__ == "__main__":        
    janet = Planet()
    print janet, janet.mass, janet.name    
