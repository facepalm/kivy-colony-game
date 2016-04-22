
need_dict = { 'structure':  {'metal':1.0, 'brick':4.0},
              'computation': {'electronics':1E6,'microprocessors':1.0,'computronium':1E-6} }

class Resource(object):
    def __init__(self):
        self.res = resource_dict()

    def add(self,res):
        self.res = add_res(self.res, res)
        return True
                        
    def sub(self,res):
        fills = self.check(res)
        (self.res,newres) = sub_res(self.res, res)
        return fills, newres         
        
    def check(self,res):        
        return tst_res(self.res, res)                                
                        
    def mass(self):
        return sum( self.res.values() )
                        

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
    
    return res
    
def add_res(res,newres):
    for r in newres:
        res[r] += newres[r]
        newres[r] = 0
    return res
    
def sub_res(res,subres):
    newres = resource_dict()
    for r in subres:
        newres[r] = min(subres[r],res[r])
        res[r] -= newres[r]
    return res, newres
        
def tst_res(res,subres):
    afford = True
    for r in subres:
        if r in res:
            if subres[r] > res[r]:
                afford = False
        else:
            #test needs
            pass
    return afford
                

