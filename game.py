import util
import numpy as np
import planet
from scipy.stats import wald
import systempanel
import random

class Universe(object):    
    def __init__(self):
        self.generate_system()
        
    def generate_system(self,system_type='Generic'):            
    
        self.system_distribution = util.getWackyDist(total_mass = 1E29, objects = 20, wacky_facty = 0.5)
                            
        primary_star_mass = wald.rvs(loc=0.2, scale=2, size=1)[0]
        
        #self.system_distribution = self.system_distribution[self.system_distribution != primary_star_mass]
        
        self.primary = planet.Star(solar_masses=primary_star_mass)
        
        print self.primary.info()
        
        num_orbits = np.random.randint(8,18)
        orbits = [pow(10,1.5*x)- 0.6 for x in np.random.random(num_orbits)]
        #np.random.shuffle( orbits )
        #orbits = orbits[ orbits != 2 ]
        orbit_mass = np.random.choice(self.system_distribution,size=num_orbits,replace=False)
        
        self.planets = []
        
        for i in range(num_orbits):
            mass = orbit_mass[i]
            print mass, orbits[i]
                
            #initialize planet, extend list (might be a list of asteroids instead)    
            newp = planet.generate_planet(mass,self.primary,orbits[i])
            self.planets.extend(newp)
            
        #habitable zone world        
        newp = planet.generate_planet(random.random()*9E24 + 1E24,self.primary,self.primary.random_habitable_orbit())
        self.planets.extend(newp)    
        
        self.primary.generate_view()
