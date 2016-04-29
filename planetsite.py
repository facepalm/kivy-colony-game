
import numpy as np

import globalvars
import siteview
import planetresources
import resource
import util

class Site(object):
    def __init__(self,planet,location='Orbit'):
        self.planet = planet
        self.location = location
        self.id = util.register(self)
        
        self.fancy_name = 'Orbit' if 'Orbit' in self.location else 'Ground Site'
        
        self.raw_resources = np.zeros(planetresources.raw_num,dtype='float32').squeeze() if 'Orbit' in self.location else np.multiply(2*np.random.random(planetresources.raw_num),self.planet.resources.raw)
        self.effective_resources = np.multiply(self.raw_resources, self.planet.resources.raw_dist)
        if self.effective_resources.sum() > 0: self.effective_resources /= sum(self.effective_resources)
        
        self.mine_init = np.random.random(planetresources.raw_num)
        self.mine = self.mine_init/(self.raw_resources/1.5) if self.raw_resources.any() > 0 else np.ones(planetresources.raw_num,dtype='float32')*2  #self.mine_init < (self.resources/2)
        
        self.explored = self.planet.explored
        
        self.stuff=[]
        self.occupied = 0
        
        self.resources = resource.Resource()
        
        #print self.planet.name, self.location, self.effective_resources, self.mine
        
    def small_view(self):
        return siteview.SiteEntrySmall(site=self)       
        
    def update_occupied(self):
        self.occupied = 0
        for s in self.stuff:
            self.occupied = max(self.occupied, s.occupation_level)
            
            
            
