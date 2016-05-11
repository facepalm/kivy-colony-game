
def untag(resourcename):
    if '|' not in resourcename: return False, resourcename, []
    restags = resourcename.split('|')
    resname = restags.pop(0)
    return True, resname, restags

class Resource(object):
    def __init__(self):
        self.physical = {}
        self.virtual = {}
        self.virtual_limit = 10

    def add(self,name,amt=0.0,virtual=False):        
        if amt <= 0: return 0
        physorvirt = 'Virt' if name in self.virtual or virtual else 'Phys'
        if physorvirt == 'Phys' and not name in self.physical:
            self.physical[name]=0.0
        elif physorvirt == 'Virt' and not name in self.virtual:    
            self.virtual[name]=0.0
            
        if physorvirt == 'Virt':
            amtadded = max(min(amt,amt*self.virtual_limit - self.virtual[name]),0)
            self.virtual[name] += amtadded
            return amtadded/amt
        else:
            self.physical[name] += amt
            return 1.0
            
    def sub(self,name, amt = 0.0,virtual=False):
        if amt < 0: return 0
        if amt == 0: return 1
        resdict = self.virtual if name in self.virtual or virtual else self.physical
        if not name in resdict: return 0.0
        amtsub = min(amt, resdict[name])
        resdict[name] -= amtsub
        return amtsub/amt

    def cansub(self,name, amt = 0.0):
        if amt < 0: return 0
        if amt == 0: return 1
        resdict = self.virtual if name in self.virtual else self.physical
        if not name in resdict: return 0.0
        amtsub = min(amt, resdict[name])
        return amtsub/amt
        
    def canadd(self,name, amt = 0.0):
        if amt < 0: return 0
        if amt == 0: return 1
        resdict = self.virtual if name in self.virtual else self.physical
        if resdict == self.physical or not name in resdict: return 1.0
        amtadd = min(amt,amt*self.virtual_limit-self.virtual[name])
        return amtadd/amt        

    def merge(self,resource):
        for r in resource.physical:
            self.add(resource.physical[r])
        for r in resource.virtual:
            self.add(resource.virtual[r],virtual=True)
        
    def split(self,shopping_list):
        fraction = 1.0
        for s in shopping_list: #will only split off as much as the most limiting resource allows
            fraction = min(fraction,self.cansub(s,shopping_list[s]))
        outr = Resource()
        for s in shopping_list:
            self.sub(s,shopping_list[s]*fraction)
            outr.add(s,shopping_list[s]*fraction, virtual = s in self.virtual)
        return outr, fraction
        
    def cansplit(self,shopping_list):
        fraction = 1.0
        for s in shopping_list: #will only split off as much as the most limiting resource allows
            fraction = min(fraction,self.cansub(s,shopping_list[s]))
        return fraction
            
    def mass(self):
        mass = 0 
        for p in self.physical.values():
            mass += p
        return mass

def resource_dict():
    res = {}
    
    #raws 
    res['metallics'] = 0
    res['silicates'] = 0
    res['hydrates'] = 0
    res['rare/alkalis'] = 0
    res['radioactives'] = 0
    res['corrosives'] = 0
    res['conductives'] = 0
    res['organics'] = 0
    res['nobles'] = 0
    
    #simple processing
    res['metal'] = 0
    res['water'] = 0
    res['silicon'] = 0
    res['brick'] = 0   
    res['conductor'] = 0     
    
    #intermediate materials, retro technology
    res['processed rares'] = 0
    res['parts'] = 0
    res['electronics'] = 0
    res['chemical rockets'] = 0
    res['solar panels'] = 0
    res['electromagnets'] = 0
    
    #present-day materials
    res['microprocessors'] = 0
    res['superconductors'] = 0    
    res['ion drives'] = 0
    
    
    #ultramaterials
    res['computronium'] = 0
    res['unobtanium'] = 0
    res['antimatter'] = 0
    
    res['electricity'] = 0
    
    return res
    

                

