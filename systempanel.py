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
        
    def update(self,clear=True):
        if clear:
            self.clear_widgets()
            self.add_widget(self.primary.image)  
        for body in self.primary.orbiting_bodies:
            if body.orbit_image.parent and body.orbit_image.parent is not self:
                #remove body's designation
                body.orbit_image.parent.remove_widget(body.orbit_image)
            if not body.orbit_image.parent:
                self.add_widget( body.orbit_image )

        
            
