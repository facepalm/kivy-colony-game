
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string("""
<ResourceEntry>:    
    number: 0.0
    name: ' ' 
    padding: 3
    Label: 
        text: self.parent.name
    ProgressBar:
        max: 1.0
        value: float(self.parent.number)

<RawResourceSquare>:  
    cols: 3
    rows: 3
    spacing: 4
    size_hint: 0.8,0.8
    ResourceEntry:
        name: 'Fe'
        number: float(self.parent.planetresources.raw[0])
    ResourceEntry:
        name: 'Li'
        number: float(self.parent.planetresources.raw[1])
    ResourceEntry:
        name: 'U'
        number: float(self.parent.planetresources.raw[2])
    ResourceEntry:
        name: 'Si'
        number: float(self.parent.planetresources.raw[3])
    ResourceEntry:
        name: 'Au'
        number: float(self.parent.planetresources.raw[4])
    ResourceEntry:
        name: 'Fl'
        number: float(self.parent.planetresources.raw[5])
    ResourceEntry:
        name: 'H2O'
        number: float(self.parent.planetresources.raw[6] )
    ResourceEntry:
        name: 'C'
        number: float(self.parent.planetresources.raw[7])
    ResourceEntry:
        name: 'Xe'
        number: float(self.parent.planetresources.raw[8])
        """)

class ResourceEntry(BoxLayout):
    pass

class RawResourceSquare(GridLayout):
    def __init__(self, **kwargs):
        self.planetresources = kwargs['planetresources']
        super(RawResourceSquare, self).__init__(**kwargs)
        
        
res_select_kv='''
<ResourceItem>:
    number: 0.0
    selected: self.ids.myval.value
    orientation: 'vertical'
    name: ' ' 
    padding: 3
    Label: 
        text: self.parent.name+': '+str(self.parent.selected)
    Slider:
        range: 0.0, float(self.parent.number)
        id: myval
        step: 1.0
        value: 0.0

<ResourceSelector>:
    size_hint: 1, None
    orientation: 'vertical'
'''

Builder.load_string(res_select_kv)

class ResourceItem(BoxLayout):
    pass

class ResourceSelector(BoxLayout):
    def __init__(self, **kwargs):
        self.resources = kwargs['resources']
        super(ResourceSelector, self).__init__(**kwargs)
        
        for r in self.resources.physical:
            ri = ResourceItem()
            ri.name = r
            ri.number = self.resources.physical[r]
            self.add_widget(ri)
