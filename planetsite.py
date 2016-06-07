
import numpy as np

import globalvars
import siteview
import planetresources
import resource
import util
import naming

class Site(object):
    def __init__(self,location='Orbit'):
        
        self.location = location
        self.id = util.register(self)
        
        self.fancy_name = 'Orbit' if 'Orbit' in self.location else 'GS-'+naming.mil_name()
        self.name = self.fancy_name                
        
        #self.raw_resources = np.zeros(planetresources.raw_num,dtype='float32').squeeze()
        
        self.explored = 1.0
        self.planet = None
        
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
    def __init__(self,planet=None,location='Orbit'):         
        super(PlanetSite, self).__init__(location=location)            
        self.planet = planet
        
        self.raw_resources = np.zeros(planetresources.raw_num,dtype='float32').squeeze() if 'Orbit' in self.location else np.multiply(2*np.random.random(planetresources.raw_num),self.planet.resources.raw)
        self.effective_resources = np.multiply(self.raw_resources, self.planet.resources.raw_dist)
        if self.effective_resources.sum() > 0: self.effective_resources /= sum(self.effective_resources)
        
        self.mine_init = np.random.random(planetresources.raw_num)
        self.mine = self.mine_init/(self.raw_resources/1.5) if self.raw_resources.any() > 0 else np.ones(planetresources.raw_num,dtype='float32')*2  #self.mine_init < (self.resources/2)
        
        self.explored = self.planet.explored
        
            
class TransferSite(Site):           
    def __init__(self,transfer=None,ships=[],resources=None, site=None): 
        super(TransferSite, self).__init__(location='Transit')
        self.name = 'GET FROM TRIP OBJECT'
        self.fancy_name = self.name
        
        self.trip = transfer
        self.ships = ships
        self.trip_resources = resources
        
        self.start_site = site
        if site: self.resources = site.resources 
        
        for s in self.ships:
            s.site.stuff.remove(s)
            s.site = self
            self.stuff.append(s)
            
        self.status = 'Waiting'
        
    def arrive(self):
        self.status = 'Arrived'
        #merge
        site = self.trip.end
        
        for s in self.ships:
            s.site = site
            site.stuff.append(s)
                         
        site.resources.merge(self.resources)
                
        
    def update(self,dt):
        if self.status == 'Arrived': return
        print 'Transit updating!'  
        secs = dt*globalvars.config['TIME FACTOR']    
        trans = self.trip.update(secs)
        if self.status == 'Waiting' and trans == 'Transit':
            self.status = 'Transit'
            self.resources = self.trip_resources
        elif self.status == 'Transit' and trans == 'Arrived':
            self.arrive()
        print self.status, util.short_timestring(self.trip.delay_until), util.short_timestring(self.trip.duration_til)
        
                
