
import numpy as np
from math import pi
import math
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
        
        self.dry_mass=0
        self.resources=None
        self.hohmann = True
        self.status = 'Undetermined'
        self.color = (0., 1., 0.)
        
        self.transfer_breakdown()
        
        self.delay_until = 0
        self.duration_til = 0

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
        if lcpi < len(listA)-1: transfer_list.append(TransferStep('Transfer',listA[lcpi+1],B,high_thrust = self.hohmann))
        for i in range(lcpi+2,len(listA)):
            transfer_list.append(TransferStep('Escape',listA[i],None))
                
        
        if 'Orbit' not in self.start.location:
            transfer_list.append(TransferStep('Launch',siteA,None))

        transfer_list = list(reversed(transfer_list))

        self.stages = transfer_list
        
    def dv(self):
        return reduce( (lambda x, y: x + y), [s.dv for s in self.stages] )       
        
    def high_dv(self):
        return reduce( (lambda x, y: x + y), [s.dv for s in self.stages if s.min_accel > 0] )        
        
    def duration(self):
        return reduce( (lambda x, y: x + y), [s.duration for s in self.stages] ) 
        
    def timing(self):
        return reduce( (lambda x, y: x + y), [s.timing for s in self.stages] )                 
        

    def calculate(self):
        peak_accel = reduce( (lambda x, y: max(x,y)), [s.min_accel for s in self.stages] )  
        total_mass = self.dry_mass
        
        if not self.resources or total_mass+self.resources.mass() <= 0:
            self.status = 'No engines or fuel available!'
            self.color = (1,0,0)
            return False
        
        total_mass += self.resources.mass()
        rocket_mass = self.resources.get('rocket engines')
        ion_mass = self.resources.get('ion engines')
            
        #thrusts in kN
        rocket_thrust = 100.0*rocket_mass
        ion_thrust = ion_mass*0.00002
            
        if rocket_thrust/total_mass < peak_accel:
            self.status = 'Insufficient thrust'
            self.color = (1,0,0)
            return False
            
        #static Isp for now
        rocket_isp = 450
        ion_isp = 2200
        
        rocket_fuel = self.resources.get('rocket fuel') 
        ion_fuel = self.resources.get('xenon') 
        
        max_high_dv = abs(9.806*rocket_isp*math.log((1.*total_mass-rocket_fuel)/total_mass))
        max_dv = abs(9.806*ion_isp*math.log((1.*total_mass-ion_fuel)/total_mass)) + max_high_dv
                        
            
        if max_high_dv < self.high_dv():
            print max_high_dv
            self.status = 'Insufficient high-thrust dv'
            self.color = (1,0,0)
            return False
            
        if max_dv < self.dv():
            self.status = 'Insufficient dv'
            self.color = (1,0,0)
            return False 
            
        
        self.status = 'GO for transfer'
        self.color = (0,0,1)
        return True
            
    def start_transfer(self):
        self.delay_until = self.timing()
        self.duration_til = self.duration()

    def update(self,dt):
        if self.delay_until > 0:
            amt = min(self.delay_until,dt)
            self.delay_until -= amt
            dt -= amt
            if dt <= 0: return 'Waiting'
        self.duration_til -= dt
        return 'Transit' if self.duration_til > 0  else 'Arrived'

class TransferStep(object):
    def __init__(self,transfer_type='Transfer',source=None,dest=None,high_thrust=True):    
        self.transfer_type = transfer_type
        self.source = source
        self.dest = dest
        self.timing = 0.0 #transfer can start timing seconds from now
        self.duration = 0.0 #how long this phase takes
        self.min_accel = 0.0 #how much oomph we need for it
        self.dv = 0.0 # dv required for this leg
        self.high_thrust=high_thrust
        
        self.init_transfer()

    def init_transfer(self):
        if self.transfer_type == 'Launch':
            assert isinstance(self.source,planetsite.Site) and 'Orbit' not in self.source.location, 'Source for launch is not a ground site.  What gives?'
            self.duration = 600.0 #about ten minutes to reach orbit
            self.dv = self.source.planet.launch_dv()
            self.min_accel = self.dv/self.duration
            self.high_thrust=True
        elif self.transfer_type == 'Land':
            assert isinstance(self.dest,planetsite.Site) and 'Orbit' not in self.dest.location, 'Something wrong with the landing parameters!'
            self.duration = 600.0 #about ten minutes to land
            self.dv = self.dest.planet.launch_dv() #considering propulsive landing only, for now
            self.min_accel = self.dv/self.duration
            self.high_thrust=True
        elif self.transfer_type == 'Escape':
            assert (isinstance(self.source,planet.Planet) or isinstance(self.source,planet.Sun)) and self.source.primary is not None, 'Something wrong with our escape trajectory!'           
            self.dv = self.source.escape_velocity() 
        elif self.transfer_type == 'Enter':
            assert (isinstance(self.dest,planet.Planet) or isinstance(self.dest,planet.Sun)) and self.dest.primary is not None, 'Something wrong with our entry trajectory!'          
            self.dv = self.dest.escape_velocity()       
        elif self.transfer_type == 'Transfer':
            if self.high_thrust:
                #assume hohmann
                self.hohmann_string = calculate_hohmann(self.source,self.dest)            
                self.dv = abs(self.hohmann_string[2])
                self.duration = self.hohmann_string[3]
                self.min_accel = self.dv/self.duration
                self.timing = self.hohmann_string[4]
            else:
                #long-term impulsive transfer
                self.ion_string = calculate_long_impulsive(self.source,self.dest)
                self.dv = abs(self.ion_string[0])    
                
            

def calculate_long_impulsive(planetA, planetB):
    if planetA == planetB:
        print "Same planet, forget it"
    assert planetA.primary == planetB.primary, 'Transfers currently require matching primaries'
    
    mu = 6.674E-11 * planetA.primary.mass
    
    r1 = planetA.orbit * 149597870700
    r2 = planetB.orbit * 149597870700
    
    v1 = np.sqrt(mu/r1)
    v2 = np.sqrt(mu/r2)
    
    dee_vee = v2-v1
    
    return dee_vee,
            
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
