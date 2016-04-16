
import numpy as np

import globalvars
import siteview
import planetresources

class Site(object):
    def __init__(self,planet,location='Orbit'):
        self.planet = planet
        self.location = location
        
        self.resources = np.zeros(planetresources.raw_num,dtype='float32').squeeze() if 'Orbit' in self.location else np.multiply(2*np.random.random(planetresources.raw_num),self.planet.resources.raw)
        self.effective_resources = np.multiply(self.resources, self.planet.resources.raw_dist)
        if self.effective_resources.sum() > 0: self.effective_resources /= sum(self.effective_resources)
        
        self.mine_init = np.random.random(planetresources.raw_num)
        self.mine = self.mine_init/(self.resources/1.5)  #self.mine_init < (self.resources/2)
        
        self.explored = self.planet.explored
        
        print self.planet.name, self.location, self.effective_resources, self.mine
        
    def small_view(self):
        return siteview.SiteEntrySmall(site=self)        
