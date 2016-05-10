
import util
import globalvars
import shipimage
import resource

class Structure(object):
    recipes = [{'unobtanium':1}] #Contains a number of possible recipes for the creation of this structure

    process = [{ 'input': {}, 
                'output': {},
                'period': util.seconds(1,'day') }]

    root_name = 'Generic Structure'

    def __init__(self,**kwargs):
        self.built=False
        self.recipe = None
        self.composition = resource.Resource()
        
        self.occupation_level = 1
        
        if 'site' in kwargs:
            self.site = kwargs['site']
            self.site.stuff.append(self)
        else:
            self.site = None
        
        self.image = None
        self.imagename = kwargs['imagename'] if 'imagename' in kwargs else 'Default'
        
        self.id = util.register(self)
        
        self.generate_image()
        
        
    def build(self, resources=None, free=False):
        if self.built: return resources
        if free:
            self.recipe = self.recipes[0]
            for r in self.recipes[0]:
                self.composition.add(r,self.recipes[0][r])
            self.built = True
            return resources
        
        for r in self.recipes:
            if resources.cansplit(self.recipes[r]) >= 1.0:
                self.recipe = r
                break
        
        if not self.recipe:
            return resources
            
        self.composition, test = resources.split(self.recipes[self.recipe])
        
        if test >= 1.0: self.built = True
        
        return resources
        
    def update(self,dt):
        secs = dt*globalvars.config['TIME FACTOR']
        
        if self.site and self.site.planet and self.site.planet.occupied < self.occupation_level:
            self.site.planet.occupied = self.occupation_level
        
        #TODO: refactor the below in some more organized fashion.  
        #It doesn't need to be run by the base structure object
        for p in self.process:        
            timeslice = secs/p['period']              
            #run p for timeslice seconds     
            
            #compute inputs, check inputs
            inputs = p['input'].copy()
            run_process = 1.0
            
            if not self.site: continue
            
            for i in inputs:
                inputs[i] *= timeslice
                assert inputs[i] != p['input'][i] or timeslice == 1.0, "Sanity check: processing is changing input dictionary"
                
                #handle special case inputs here
                    
            #real_input = {k:v for k,v in inputs.items() if k in self.site.resources.physical}
            
            run_process = self.site.resources.cansplit( inputs )
            
            if run_process: #we doin this
                #subtract inputs
                r,fraction = self.site.resources.split(inputs)
                for i in inputs:
                    #special case stuff here
                    pass 
                    
                #generate outputs
                outputs = p['output'].copy()
                
                for o in outputs:
                    outputs[o] *= timeslice    
                    outputs[o] *= fraction
                    #handle special case inputs here
                    tagged, ro, tags = resource.untag(o) 
                    
                    if ro == 'Exploration (System)': #TODO move this to sites
                        limit = p['explore-limit'] if 'explore-limit' in p else 0.1                        
                        globalvars.universe.add_exploration(outputs[o],limit)
                    
                    
                #real_output = {k:v for k,v in outputs.items() if k in self.site.resources.res}
                    
                    self.site.resources.add(ro,outputs[o], virtual = 'virtual' in tags)
                
                
            #handle outputs
            
            
    def name(self):
        return self.root_name+'-'+util.short_id(self.id)                            
        
        
    def generate_image(self,clear=False, new=False):
        if clear: pass #handle deleting image here
        if new: 
            return shipimage.ShipImage(ship=self, source = shipimage.shipimages[self.imagename])
        if self.image is None:
            self.image = shipimage.ShipImage(ship=self, source = shipimage.shipimages[self.imagename])
        
        
        
class PlaceholderRegolithMiner(Structure):
    recipes = [{'metal':1000, 'computronium':1}] 

    process =  [{   'name' : 'Regolith Harvesting', 
                    'input': {}, 
                    'output': {'regolith|virtual':1000},
                    'period': util.seconds(1,'days') }                                
               ]

    root_name = 'RegMiner'        
        
class RTG(Structure):
    recipes = [{'metal':20, 'enriched radioactives':5}] 

    #TODO gradual decay of power?
    process =  [{   'name' : 'Power (Continuous)', 
                    'input': {}, 
                    'output': {'electricity|virtual':125},
                    'period': 1 }                    
               ]
    root_name = 'RTG'
        
        
