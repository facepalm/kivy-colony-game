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
    
        self.initialize_sites()
        
    def initialize_sites(self):
        self.sites = None
        self.orbits = None
    
class Star(Planet):
    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)
        
    
if __name__ == "__main__":        
    janet = Planet()
    print janet, janet.mass, janet.name    
