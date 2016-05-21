
import numpy as np
from math import pi
import planetsite
import planet

#this might eventually become a better approach for orbits
#could handle eccentricites, etc
#not worth it now though
class Orbit(object):
    def __init__(self, **kwargs):
        self.primary = kwargs['primary'] if 'primary' in kwargs else None
        self.semimajor = kwargs['distance'] if 'distance' in kwargs else 1E6        
      
    
class Transfer(object):
    def __init__(self,start_site,end_site):
        self.start = start_site
        self.end = end_site
        
        self.dry_mass=None
        self.resources=None
        
        self.transfer_breakdown()

    def transfer_breakdown(self):
        transfer_list = []                
        
        listA = []
        A = self.start.planet
        while A is not None:
            listA.append(A)
            A = A.primary
        listA = list(reversed(listA))
        
        planetB = self.end.planet
        if 'Orbit' not in self.end.location:
            transfer_list.append(TransferStep('Land',None,self.end))
        
        B = planetB
        while B.primary not in listA:
            transfer_list.append(TransferStep('Enter',None,B))
            B = B.primary
        
        #TODO check for weirdness where A and B are not in the same system
        lcpi = listA.index(B.primary)
        if lcpi < len(listA)-1: transfer_list.append(TransferStep('Transfer',listA[lcpi+1],B))
        for i in range(lcpi+2,len(listA)):
            transfer_list.append(TransferStep('Escape',listA[i],None))
                
        
        if 'Orbit' not in self.start.location:
            transfer_list.append(TransferStep('Launch',siteA,None))

        transfer_list = list(reversed(transfer_list))

        self.stages = transfer_list
        
    def dv(self):
        return reduce( (lambda x, y: x + y), [s.dv for s in self.stages] )       
        
    def high_dv(self):
        return reduce( (lambda x, y: x + y), [s.dv for s in self.stages if s.min_impulse > 0] )        
        
    def duration(self):
        return reduce( (lambda x, y: x + y), [s.duration for s in self.stages] ) 
        
    def timing(self):
        return reduce( (lambda x, y: x + y), [s.timing for s in self.stages] )                 
        

    def calculate(self):
        peak_accel = reduce( (lambda x, y: max(x,y)), [s.min_accel for s in self.stages] )  
        
        
        

class TransferStep(object):
    def __init__(self,transfer_type='Transfer',source=None,dest=None):    
        self.transfer_type = transfer_type
        self.source = source
        self.dest = dest
        self.timing = 0.0 #transfer can start timing seconds from now
        self.duration = 0.0 #how long this phase takes
        self.min_accel = 0.0 #how much oomph we need for it
        self.dv = 0.0 # dv required for this leg
        
        self.init_transfer()

    def init_transfer(self):
        if self.transfer_type == 'Launch':
            assert isinstance(self.source,planetsite.Site) and 'Orbit' not in self.source.location, 'Source for launch is not a ground site.  What gives?'
            self.duration = 600.0 #about ten minutes to reach orbit
            self.dv = self.source.planet.launch_dv()
            self.min_accel = self.dv/self.duration
        elif self.transfer_type == 'Land':
            assert isinstance(self.dest,planetsite.Site) and 'Orbit' not in self.dest.location, 'Something wrong with the landing parameters!'
            self.duration = 600.0 #about ten minutes to land
            self.dv = self.dest.planet.launch_dv() #considering propulsive landing only, for now
            self.min_accel = self.dv/self.duration
        elif self.transfer_type == 'Escape':
            assert (isinstance(self.source,planet.Planet) or isinstance(self.source,planet.Sun)) and self.source.primary is not None, 'Something wrong with our escape trajectory!'           
            self.dv = self.source.escape_velocity() 
        elif self.transfer_type == 'Enter':
            assert (isinstance(self.dest,planet.Planet) or isinstance(self.dest,planet.Sun)) and self.dest.primary is not None, 'Something wrong with our entry trajectory!'          
            self.dv = self.dest.escape_velocity()       
        elif self.transfer_type == 'Transfer':
            #assume hohmann for now
            self.hohmann_string = calculate_hohmann(self.source,self.dest)            
            self.dv = abs(self.hohmann_string[2])
            self.duration = self.hohmann_string[3]
            self.min_accel = self.dv/self.duration
            self.timing = self.hohmann_string[4]
            
            
#equations from https://en.wikipedia.org/wiki/Hohmann_transfer_orbit
def calculate_hohmann(planetA, planetB):
    if planetA == planetB:
        print "Same planet, forget it"
    assert planetA.primary == planetB.primary, 'Hohmann transfers currently require matching primaries'
    r1 = planetA.orbit * 149597870700
    r2 = planetB.orbit * 149597870700
    
    mu = 6.674E-11 * planetA.primary.mass
    
    vee_1 = np.sqrt(mu/r1) * ( np.sqrt( (2*r2) / (r1 + r2) ) - 1)
    vee_2 = np.sqrt(mu/r2) * ( 1 - np.sqrt( (2*r1) / (r1 + r2) ) )
    
    dee_vee = vee_1 + vee_2
    
    time = pi*np.sqrt( pow(r1+r2,3) / (8*mu) )
    
    w2 = np.sqrt(mu/pow(r2,3)) 
    w1 = np.sqrt(mu/pow(r1,3)) 
    
    target_angle = pi - w2*time # pi*(1- (1/(2*np.sqrt(2)))*np.sqrt(pow(r1/r2+1,3)) )
    
    target_angle = target_angle % (2*pi)
    
    curr_angle = (planetB.orbit_pos - planetA.orbit_pos) % (2*pi)
    angular_v = w2 - w1        
    
    if angular_v > 0:
        ang_dist = target_angle + 2*pi - curr_angle
        ang_dist = ang_dist % (2*pi)
    else:
        ang_dist = target_angle - 2*pi - curr_angle
        ang_dist = ang_dist % (2*pi) - (2*pi)
    
    
    #ang_dist = target_angle + 2*pi if (target_angle - curr_angle)*angular_v < 0 else target_angle
    #ang_dist -= curr_angle
    go_time = ang_dist/angular_v
    
    print "Hohmann transfer from ",planetA.name,' to ',planetB.name
    print 'radii:',r1, r2
    print 'dVs:',vee_1,vee_2,dee_vee, ' transit time:',time
    print 'Target angle:',target_angle,' Current angle:',curr_angle
    print 'Transfer in:',go_time,'s'
    
    return vee_1, vee_2, dee_vee, time, go_time      
