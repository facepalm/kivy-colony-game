
import random
from kivy.uix.image import Image

#manager for planet images & icons
planet_dict = { 'Brown-Dwarf': ['browndwarf'],
                'Gas' : ['cloud0','gas5','gas1','gas2','gas4','gas7','cloud5','cloud7'],
                'Ice Giant':['gas0','gas3','gas6','uranus','cloud1','cloud2','cloud6','fog0'],
                'Habitable' : ['earth','cloud3'],
                'Rocky-Bare': ['callisto','desert0','desert5'] ,
                'Rocky-Atmosphere': ['venus','cloud4'],
                'Ice-Bare': ['dust5','dust6','desert5','europa','ice0','ice1'] 
                
                }
                
def _es(imagename):
    prefix = 'images/endless-sky/images/planet/'
    return prefix+imagename+'.png'
    
  
                
def random_image(planet):
    if planet.type == 'Gas giant':
        if planet.orbit < planet.primary.ice_line:
            img = _es(random.choice(planet_dict['Gas']))
        else:
            img = _es(random.choice(planet_dict['Ice Giant']))
    elif planet.type == 'Planet':
        if planet.primary.is_habitable(planet.orbit):
            img = _es(random.choice(planet_dict['Habitable']))
        elif planet.orbit > planet.primary.snow_line:
            img = _es(random.choice(planet_dict['Ice-Bare']))
        else:
            img = _es(random.choice(planet_dict['Rocky-Atmosphere']))
    elif planet.type == 'Dwarf planet':           
        if planet.orbit < planet.primary.snow_line:
            img = _es(random.choice(planet_dict['Rocky-Bare']))
        else:
            img = _es(random.choice(planet_dict['Ice-Bare']))
    elif planet.type == 'Brown dwarf':
        img = _es(random.choice(planet_dict['Brown-Dwarf']))
    else: 
        print planet.type
        img = 'generic_asteroid.png'
        
    return img

def load_primary(imagename):
    img = Image(source=imagename,allow_stretch=True,size_hint=(None, None))   
    sz = img.texture.size
    minlen= min(sz[0],sz[1])
    size = (round(100.0*sz[0]/minlen),round(100.0*sz[1]/minlen))        
    img.size=size    
    #print imagename,img.size,img.texture.size
    return img
    
def load_orbital(imagename,radius=1.0):
    img = Image(source=imagename,allow_stretch=True,size_hint=(None, None))   
    sz = img.texture.size
    minlen= min(sz[0],sz[1])
    size = (round(100.0*radius*sz[0]/minlen),round(100.0*radius*sz[1]/minlen))        
    img.size=size    
    #print imagename,img.size,img.texture.size
    return img    
    
        
