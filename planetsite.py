
import numpy as np

import globalvars
import siteview

class Site(object):
    def __init__(self,planet,location='Orbit'):
        self.planet = planet
        self.location = location
        
        self.resources = np.zeros((1,10),dtype='float32') if 'Orbit' in self.location else np.multiply(2*np.random.random(10),self.planet.resources.raw)
        self.effective_resources = np.multiply(self.resources, self.planet.resources.raw_dist)
        if self.effective_resources.sum() > 0: self.effective_resources /= sum(self.effective_resources)
        
        print self.planet.name, self.location, self.effective_resources
        
    def small_view(self):
        return siteview.SiteEntrySmall(site=self)        
