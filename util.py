import logging
import numpy as np
import string
import globalvars
import uuid
import pickle
import os
import naming
import sys
import random

#TIME_FACTOR = 168 # 1 irl hour = 1 week
#TIME_FACTOR = 24 # 1 irl hour = 1 day
#TIME_FACTOR = 120

#ZOOM = 15

equipment_targets = dict()

#GRAPHICS = None
GLOBAL_X=0
GLOBAL_Y=0

def getWackyDist(total_mass = 2E30, objects = 10, wacky_facty = 1):
    '''returns a lopsided distribution, suitable for star systems'''
    array = []
    unusedprob = 1.0
    for i in range(0,objects-1):
        rand = random.random()
        array.append( rand * unusedprob )
        unusedprob -= rand * unusedprob
    array.append( unusedprob )
    odds = np.array([pow(2,10*i*wacky_facty)-1 for i in array])
    odds /= sum(odds)
    odds = odds[ odds > 0 ]
    return odds*total_mass

def radian(deg):
    return 3.14159*deg/180

def degree(rad):
    return 180*rad/3.14159

def register(obj, oid=''):
    new_id = oid if oid else str(uuid.uuid4())
    try:
        globalvars.ids[new_id] = obj
    except:
        assert False, "global id collision!"
    return new_id

def quad_mean(x,y,wx=1,wy=1):
    return pow( (1.0*wx*x*x + wy*y*y)/(wx + wy) ,0.5)
    
def timestring(seconds):
    seconds = int(seconds)
    time=''
    div, rem = (seconds/(2592000*12),seconds%(2592000*12))    
    if div: time = ''.join([time,str(div),' year ' if div==1 else ' years ' ])
    seconds = rem
    div, rem = (seconds/(2592000),seconds%(2592000))    
    if div: time = ''.join([time,str(div),' month ' if div==1 else ' months ' ])
    seconds = rem
    div, rem = (seconds/(86400),seconds%(86400))    
    if div: time = ''.join([time,str(div),' day ' if div==1 else ' days ' ])
    seconds = rem
    div, rem = (seconds/(3600),seconds%(3600))    
    if div: time = ''.join([time,str(div),' hour ' if div==1 else ' hours ' ])
    seconds = rem
    time = ''.join([time,str(seconds),' seconds' ])
    return time    
    
    
    
def seconds(time=1,units='minutes'):
    return time*60 if units == 'minutes' or units == 'minute' \
                                         else time*3600 if units == 'hours' or units == 'hour' \
                                         else time*86400 if units=='days' or units == 'day' \
                                         else time*2592000 if units=='months' or units == 'month' \
                                         else time*2592000*12 if units=='years' or units == 'year' \
                                         else 10    
                                         
                                         
def short_id(long_id):
    return string.upper(long_id[0:6])                                                
                                         
def vec_dist(a,b):
    diff = b-a
    return np.sqrt( np.vdot( diff , diff ) )

def planet_name(planet=None,planet_type=None):
    return naming.planet_name(planet,planet_type)

def star_name(star=None):
    return "Placeholder Star"

generic_logger=logging.getLogger("SystemLog")
generic_logger.setLevel(logging.DEBUG)
#DEBUG INFO WARNING ERROR CRITICAL
#create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
#create formatter
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#add formatter to ch
ch.setFormatter(formatter)
#add ch to logger
generic_logger.addHandler(ch)

generic_logger.debug("Logger initiated.")

def autosave():
    try:
        datafile = open(os.path.join('save','autosave'),'w')
        pickle.dump(globalvars.universe,datafile,2)        
        datafile.close()
        generic_logger.info("Universe saved.  Superman given the day off.")
        return True
    except:
        e = sys.exc_info()[0]
        generic_logger.warning("Autosave failed: %s" % e)
    return False
        
    
def autoload():
    try:
        datafile = open(os.path.join('save','autosave'),'r')
        #global universe
        globalvars.universe = pickle.load(datafile)
        datafile.close()
        generic_logger.info("Universe loaded.  Initiating prime mover...")
        return True
    except:
        e = sys.exc_info()[0]
        generic_logger.warning("Autoload failed: %s" % e)
    return False
       
