


class Resource(object):
    def __init__(self):
        self.res={}
        self.virtual_limit = 10
        self.mass = 0.0

    def add(self,name,amt=0.0,virtual=False,affect_mass=True):
        if amt <= 0: return 0
        if not name in self.res:
            self.res[name]=0.0
        if virtual:
            amtadded = min(amt,self.res[name]*self.virtual_limit)
            self.res[name] += amtadded
            return amtadded/amt
        else:
            self.res[name] += amt
            if affect_mass: self.mass += amt
            return 1.0
            
    def sub(self,name, amt = 0.0, virtual = False):
        if amt < 0: return 0
        if amt == 0: return 1
        if not name in self.res:
            self.res[name]=0.0
        amtsub = min(amt, self.res[name])
        self.res[name] -= amtsub
        if not virtual:
            self.mass -= amtsub
        return amtsub/amt

    def check(self,name, amt = 0.0):
        if amt < 0: return 0
        if amt == 0: return 1
        if not name in self.res:
            self.res[name]=0.0
        amtsub = min(amt, self.res[name])
        return amtsub/amt

    def merge(self,resource):
        for r in resource.res:
            self.add(resource.res[r],affect_mass = False)
        self.mass += resource.mass
        
    def split(self,shopping_list):
        fraction = 1.0
        for s in shopping_list: #will only split off as much as the most limiting resource allows
            fraction = min(fraction,self.check(shopping_list[s]))
        outr = Resource()
        #mass is not preserved in this case.  Handle later, somehow
        for s in shopping_list:
            self.sub(s,shopping_list[s]*fraction)
            outr.add(s,shopping_list[s]*fraction)
        return outr, fraction
            


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
    

                

