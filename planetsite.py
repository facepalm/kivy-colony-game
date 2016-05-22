
import numpy as np

import globalvars
import siteview
import planetresources
import resource
import util
import naming

class Site(object):
    def __init__(self,planet=None,location='Orbit'):
        self.planet = planet
        self.location = location
        self.id = util.register(self)
        
        self.fancy_name = 'Orbit' if 'Orbit' in self.location else 'GS-'+naming.mil_name()
        self.name = self.fancy_name
        
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

class PlanetSite(Site):           
    def __init__(self,**kwargs): 
        super(PlanetSite, self).__init__(location='Transit')            
        
            
class TransitSite(Site):           
    def __init__(self,**kwargs): 
        super(TransitSite, self).__init__(planet=None,location='Transit')
