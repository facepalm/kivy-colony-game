import numpy as np
import util
import logging
import random
import systempanel
import math

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

def generate_planet(mass,sun,orbit):
    p = Planet(mass,sun,orbit)
    #eventually walk through planetary history - greenhouse events, asteroidation, etc
    
    sun.orbiting_bodies.extend([p])
    return [p]

class Planet(object):
    def __init__(self,mass=None,sun=None,orbit=None,name=None, logger=None):
        self.mass = mass if mass else 1E8*random.random()
        self.name = name if name else util.planet_name(self)
        self.sun=sun
        self.orbit = orbit
        if logger:
            self.logger = logging.getLogger(logger.name + '.' + self.name)
        else: 
            self.logger = logging.getLogger(util.generic_logger.name + '.' + self.name)
    
        if self.mass > 1E29: 
            self.type = 'INVALID' #actually a sun.  Throw an error, this shouldnt happen
        elif self.mass > 1E28: 
            self.type = 'Brown dwarf' #counting this as a planet, since they have negligible radiation    
        elif self.mass > 1E26:
            self.type = 'Gas giant' if self.orbit < self.sun.ice_line else 'Ice giant'
        elif self.mass > 1E23:
            self.type = 'Planet' #rocky world, but capable of retaining an atmosphere, even if barely
        elif self.mass > 1E21:
            self.type = 'Dwarf planet' #larger moons and asteroids, rounded
        else:
            self.type = 'Planetoid' #small moons, asteroids, rocks, etc
    
        self.initialize_sites()
        
        self.orbiting_bodies = []
        
        self.orbit_pos = random.random()*np.pi*2
        
        frac = 0.25
        
        self.image=Image(source='generic_sun.png',allow_stretch=True,size_hint=(None, None),size=(round(75*frac), round(75*frac)),pos_hint={'center_x':.5, 'center_y':.5})
        
        self.orbitimage = Image(source='generic_sun.png',allow_stretch=True,size_hint=(None, None),size=(round(75*frac), round(75*frac)),pos_hint={'center_x':.5+ math.cos(self.orbit_pos)*(1/2.0), 'center_y':.5+(math.sin(self.orbit_pos)/2.0)})
        
        
        #self.view = systempanel.SystemView(primary=self)
        
    def initialize_sites(self):
        self.sites = 6 if self.type == 'Planet' else 2 if self.type == 'Dwarf planet' else 1 if self.type == 'Planetoid' else 0
        self.orbits = 1
        #print self.sites, self.orbits
    
class Star(object):
    def __init__(self, solar_masses, name=None, logger=None):
        self.solar_masses = solar_masses
        self.mass = self.solar_masses*2E30
        self.name = name if name else util.star_name(self)
        if logger:
            self.logger = logging.getLogger(logger.name + '.' + self.name)
        else: 
            self.logger = logging.getLogger(util.generic_logger.name + '.' + self.name)
    
        #current assumption: main sequence star.  May want to simulate lifetimes and do giants in the future
        # reference: https://en.wikipedia.org/wiki/Stellar_classification
        saturation = 200.0
        if self.solar_masses < 0.5: 
            self.type = 'M'
            self.radius = 0.7
            self.luminosity = 0.08
            self.color_name = 'Red'
            self.color = np.array([255,204,111,255])/saturation
        elif self.solar_masses < 0.8: 
            frac = (self.solar_masses - 0.5)/0.3
            self.type = 'K'
            self.radius = 0.7 + 0.26*frac
            self.luminosity = 0.08 + 0.52*frac
            self.color_name = 'Orange'
            self.color = np.array([255,210,161,255])/saturation
        elif self.solar_masses < 1.04: 
            frac = (self.solar_masses - 0.8)/0.24
            self.type = 'G'
            self.radius = 0.96 + (1.15-0.96)*frac
            self.luminosity = 0.6 + (1.5 - 0.6)*frac
            self.color_name = 'Yellow'
            self.color = np.array([255, 244, 234,255])/saturation
        elif self.solar_masses < 1.4: 
            frac = (self.solar_masses - 1.04)/0.36
            self.type = 'F'
            self.radius = 1.15 + (1.4-1.15)*frac
            self.luminosity = 1.5 + (5 - 1.5)*frac
            self.color_name = 'Yellow-White'
            self.color = np.array([248, 247, 255,255])/saturation
        elif self.solar_masses < 2.1: 
            frac = (self.solar_masses - 1.4)/0.7
            self.type = 'A'
            self.radius = 1.4 + (1.8-1.4)*frac
            self.luminosity = 5 + (25 - 5)*frac
            self.color_name = 'White'
            self.color = np.array([202, 215, 255,255])/saturation   
        elif self.solar_masses < 16: 
            frac = (self.solar_masses - 2.1)/(16-2.1)
            self.type = 'B'
            self.radius = 1.8 + (6.6-1.8)*frac
            self.luminosity = 25 + (30000 - 25)*frac
            self.color_name = 'Blue-White'  
            self.color = np.array([170, 191, 255,255])/saturation 
        else: # self.solar_masses > 16: 
            frac = (self.solar_masses - 2.1)/(16-2.1)
            self.type = 'O'
            self.radius = 8 #arbitrary
            self.luminosity = 50000 #arbitrary
            self.color_name = 'Blue'     
            self.color = np.array([155, 176, 255,255])/saturation 
        
        self.habitable_start = 0.80 * pow( self.luminosity ,0.5)
        self.habitable_end = 1.4 * pow( self.luminosity ,0.5)
        
        self.snow_line = 3 * pow( self.luminosity ,0.5)
        self.ice_line = 10 * pow( self.luminosity ,0.5)
        
        frac = 0.25
        
        self.image=Image(source='generic_sun.png',color=self.color,allow_stretch=True,size_hint=(None, None),size=(round(75*frac*self.radius), round(75*frac*self.radius)),pos_hint={'center_x':.5, 'center_y':.5})
        
        self.orbitimage = None #primary star doesn't orbit - would need barycenter calculation if multiple suns
        #self.orbitimage = Image(source='generic_sun.png',color=self.color,allow_stretch=True,size_hint=(None, None),size=(round(75*frac*self.radius), round(75*frac*self.radius)),pos_hint={'center_x':.75, 'center_y':.5})
        
        self.orbiting_bodies = []
        
        #self.view = systempanel.SystemView(primary=self)
        
    def random_habitable_orbit(self):
        return (random.random()*0.6 + 0.8) * pow( self.luminosity ,0.5)
        
    def generate_view(self):
        self.view = systempanel.SystemView(primary=self)
        for body in self.orbiting_bodies:
            self.view.add_widget( body.orbitimage )
        return self.view

    def info(self):
        out = self.type+'-type star, with mass of %.2f' % self.solar_masses + ' and luminosity of %.2f' % self.luminosity
        out += ', Habitable zone between %.2f' % self.habitable_start +' and %.2f' % self.habitable_end
        out += ', Snow line at %.2f' % self.snow_line
        return out
        
    
if __name__ == "__main__":        
    janet = Planet()
    print janet, janet.mass, janet.name    
