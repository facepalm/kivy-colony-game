import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.scrollview import ScrollView

import math

from kivy.core.window import Window


class SystemView(ScrollView):
    def __init__(self, **kwargs):
        super(SystemView, self).__init__(**kwargs)
        self.map = FloatLayout(size=(1000,1000),size_hint = (None, None))
        self.add_widget(self.map)
        self.primary = kwargs['primary']
        self.orbit_constant = 5
        
        self.children = []
        #self.scale = None
        
        self.map.add_widget(self.primary.image)      
        #self.size=(1000,1000)          
        #self.size_hint=(1,1)
                
    def add_child(self,_list=[]):        
        self.children.extend(_list)
           
    def remove_child(self,obj):
        self.children.remove(obj)    
        
    def update(self,clear=True):
        if clear:
            self.map.clear_widgets()
            
            self.map.add_widget(self.primary.image)  
        for body in self.primary.orbiting_bodies:
            if body.orbit_image.parent and body.orbit_image.parent is not self:
                #remove body's designation
                body.orbit_image.parent.remove_widget(body.orbit_image)
            if not body.orbit_image.parent:
                with self.map.canvas.before:
                    Color( 0.75, 0.75, 0.25 )
                    #print self.to_window(self.center_x, self.center_y)
                    #print Window.size[0], self.size[0]
                    Line(circle=( self.map.size[0]/2, self.map.size[1]/2, 1000*float(math.log((body.orbit+1),10)/2)))
                    
                self.map.add_widget( body.orbit_image )

        
            
