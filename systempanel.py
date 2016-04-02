import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout

class SystemView(FloatLayout):
    def __init__(self, **kwargs):
        super(SystemView, self).__init__(**kwargs)
        self.primary = kwargs['primary']
        
        
        self.children = []
        self.scale = None
        
        self.add_widget(self.primary.simpleview)                
            
    def add_child(self,_list=[]):
        self.children.extend(_list)
        
            
