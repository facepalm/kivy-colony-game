
import numpy as np
from math import pi

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
        transfer_list.append(['Land',siteB])
    
    B = planetB
    while B.primary not in listA:
        transfer_list.append(['Enter',B])
        B = B.primary
    
    #TODO check for weirdness where A and B are not in the same system
    lcpi = listA.index(B.primary)
    if lcpi < len(listA)-1: transfer_list.append(['Transfer',listA[lcpi+1],B])
    for i in range(lcpi+2,len(listA)):
        transfer_list.append(['Escape',listA[i]])
            
    
    if 'Orbit' not in siteA.location:
        transfer_list.append(['Launch',siteA])

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
    
    target_angle = pi - w2*time # pi*(1- (1/(2*np.sqrt(2)))*np.sqrt(pow(r1/r2+1,3)) )
    
    target_angle = target_angle % (2*pi)
    
    print "Hohmann transfer from ",planetA.name,' to ',planetB.name
    print 'radii:',r1, r2
    print 'dVs:',vee_1,vee_2,dee_vee, ' transit time:',time
    print 'Target angle:',target_angle
    
    

class TransferStep(object):
    def __init__(self,transfer_type='Transfer',source=None,dest=None):    
        pass
