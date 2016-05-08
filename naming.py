import numpy as np
import random
import uuid
import string

planets = {'comfy':[],'cold':[],'generic':[]}

def load_names():
    global planets
    
    pos = 'Generic'
    namefile = file('generic_planet_names.txt','r')
    for line in namefile.readlines():
        line=line.strip()
        if line == '': continue
        if line == 'Comfy Names:':
            pos = 'Comfy'
            continue
        if line == 'Cold Names:':
            pos = 'Cold'
            continue
        if line == "Generic Names:":
            pos = 'Generic'
            continue
        if pos == 'Comfy': planets['comfy'].append(line)
        if pos == 'Cold': planets['cold'].append(line)
        if pos == 'Generic': planets['generic'].append(line)

def planet_name(planet=None,planet_type=None):
    if not planet_type: 
        if (not planet or not hasattr(planet,'mass')): 
            planet_type == 'Generic'
        elif planet.mass < 1E20:
            planet_type == 'Planetoid'
        elif (planet.mass > 6E23 and planet.mass < 6E24):
            planet_type == 'Comfy'
    if planet_type == 'Planetoid': 
        #TODO add a letter at the beginning to make it look better
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(6))
    if planet_type == 'Comfy': 
        return random.choice(planets['comfy'])
    if planet_type == 'Cold': 
        return random.choice(planets['cold'])    
    return random.choice(planets['generic'])
        
load_names()        

mil_names = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey', 'X-ray', 'Yankee', 'Zulu']
        
def mil_name():
    return random.choice(mil_names)+' '+random.choice(mil_names)
        
if __name__ == "__main__":        
    print planet_name()
    print planet_name(planet_type='Comfy')
    print planet_name(planet_type='Planetoid')
    
