
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string("""
<ResourceEntry>:    
    number: 0.0
    name: ' ' 
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

