import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout

class SystemView(FloatLayout):
    def __init__(self, **kwargs):
        super(SystemView, self).__init__(**kwargs)
        self.primary = kwargs['primary']
        
        
        self.children = []
        self.scale = None
        
        self.add_widget(self.primary.image)                
            
    def add_child(self,_list=[]):        
        self.children.extend(_list)
           
    def remove_child(self,obj):
        self.children.remove(obj)    
        
    def update(self):      
        for body in self.primary.orbiting_bodies:
            self.add_widget( body.orbit_image )

        
            
