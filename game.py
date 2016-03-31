import util
import numpy as np

class Universe(object):    
    def __init__(self):
        self.generate_system()
        
    def generate_system(self,system_type='Generic'):
    
        self.system_distribution = util.getWackyDist(total_mass = 1E29, objects = 20, wacky_facty = 1)
                        
        primary_star_mass = 2E30 + 1E29*np.random.randn() #self.system_distribution.max()
        #self.system_distribution = self.system_distribution[self.system_distribution != primary_star_mass]
        
        num_orbits = np.random.randint(8,18)
        orbits = np.arange(0,30)
        np.random.shuffle( orbits )
        orbits = orbits[ orbits != 2 ]
        orbit_mass = np.random.choice(self.system_distribution,size=num_orbits,replace=False)
        
        self.planets = []
        
        for i in range(num_orbits):
            mass = orbit_mass[i]
            print mass, orbits[i]
                
            #initialize planet, extend list (might be a list of asteroids instead)    
            self.planets.extend([])
