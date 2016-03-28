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
    
if __name__ == "__main__":        
    janet = Planet()
    print janet, janet.mass, janet.name    
