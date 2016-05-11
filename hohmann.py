
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
    
def transfer_breakdown(siteA, siteB):
    transfer_list = []
    
    
    
    listA = []
    A = siteA.planet
    while A is not None:
        listA.append(A)
        A = A.primary
    listA = list(reversed(listA))
    
    planetB = siteB.planet
    if 'Orbit' not in siteB.location:
        transfer_list.append(['Land',None,siteB])
    
    B = planetB
    while B.primary not in listA:
        transfer_list.append(['Enter',None,B])
        B = B.primary
    
    #TODO check for weirdness where A and B are not in the same system
    lcpi = listA.index(B.primary)
    if lcpi < len(listA)-1: transfer_list.append(['Transfer',listA[lcpi+1],B])
    for i in range(lcpi+2,len(listA)):
        transfer_list.append(['Escape',listA[i],None])
            
    
    if 'Orbit' not in siteA.location:
        transfer_list.append(['Launch',siteA,None])

    transfer_list = list(reversed(transfer_list))

    return transfer_list
    
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
    
    #TODO check if it's supposed to be planetA - planetB instead
    curr_angle = planetB.orbit_pos - planetA.orbit_pos
    deriv_angle = w2 - w1
    
    
    print "Hohmann transfer from ",planetA.name,' to ',planetB.name
    print 'radii:',r1, r2
    print 'dVs:',vee_1,vee_2,dee_vee, ' transit time:',time
    print 'Target angle:',target_angle
    
    return vee_1, vee_2, dee_vee, time
    
    

class TransferStep(object):
    def __init__(self,transfer_type='Transfer',source=None,dest=None):    
        self.transfer_type = transfer_type
        self.source = source
        self.dest = dest
        self.timing = 0.0 #transfer can start timing seconds from now
        self.duration = 0.0 #how long this phase takes
        self.min_impulse = 0.0 #how much oomph we need for it
        self.dv = 0.0 # dv required for this leg
        
        self.init_transfer()

    def init_transfer(self):
        if self.transfer_type == 'Launch':
            assert isinstance(self.source,planetsite.Site) and 'Orbit' not in self.source.location, 'Source for launch is not a ground site.  What gives?'
            self.duration = 600.0 #about ten minutes to reach orbit
            self.dv = self.source.planet.launch_dv()
            self.min_impulse = self.dv/self.duration
        elif self.transfer_type == 'Land':
            assert isinstance(self.dest,planetsite.Site) and 'Orbit' not in self.dest.location, 'Something wrong with the landing parameters!'
            self.duration = 600.0 #about ten minutes to land
            self.dv = self.source.planet.launch_dv() #considering propulsive landing only, for now
            self.min_impulse = self.dv/self.duration
        elif self.transfer_type == 'Escape':
            assert (isinstance(self.source,planet.Planet) or isinstance(self.source,planet.Sun)) and self.source.primary is not None, 'Something wrong with our escape trajectory!'           
            self.dv = self.source.escape_velocity() 
        elif self.transfer_type == 'Enter':
            assert (isinstance(self.dest,planet.Planet) or isinstance(self.dest,planet.Sun)) and self.dest.primary is not None, 'Something wrong with our entry trajectory!'          
            self.dv = self.dest.escape_velocity()       
        elif self.transfer_type == 'Transfer':
            pass
