import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

import math
import globalvars

from kivy.core.window import Window
from kivy.graphics.context_instructions import Scale
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

orbit_constant = 3.0


class SystemScreen(Screen):
    def __init__(self, **kwargs):
        super(SystemScreen, self).__init__(**kwargs)
        self.system_view = SystemView(**kwargs)
        self.add_widget( self.system_view )
        self.name = kwargs['name']

class SystemView(ScrollView):
    def __init__(self, **kwargs):
        super(SystemView, self).__init__(**kwargs)
        self.map = FloatLayout(size=(2000,2000),size_hint = (None, None))
        self.add_widget(self.map)
        self.primary = kwargs['primary']
        self.orbit_constant = orbit_constant #scaling factor for map
        
        self.map.add_widget(self.primary.primary_image())      
        self.scroll_x = 0.5
        self.scroll_y = 0.5

         
        Window.bind(on_keyboard=self.onBackBtn)        

    def on_touch_down(self, touch):
        super(SystemView, self).on_touch_down(touch)
        self.map.on_touch_down(touch)
        return False
           
        
    def update(self,clear=True):
        if clear:
            self.map.clear_widgets()
            
            self.map.add_widget(self.primary.primary_image())  
            if self.primary.is_sun:
                with self.map.canvas:  
                               
                    Color( 0.25, 0.5, 0.25 )            
                    Line(circle=( self.map.size[0]/2, self.map.size[1]/2, 0.5*self.map.size[0]*float(math.log((self.primary.habitable_start+1),10)/self.orbit_constant)), dash_length=10, dash_offset = 10)
                    Line(circle=( self.map.size[0]/2, self.map.size[1]/2, 0.5*self.map.size[0]*float(math.log((self.primary.habitable_end+1),10)/self.orbit_constant)), dash_length=10, dash_offset = 10)
                    
                    Color( 0.25, 0.25, 0.5 )
                    Line(circle=( self.map.size[0]/2, self.map.size[1]/2, 0.5*self.map.size[0]*float(math.log((self.primary.snow_line+1),10)/self.orbit_constant)), dash_length=10, dash_offset = 10)
    
        self.map.canvas.before.clear()            
        with self.map.canvas.before:
            
            Color( 0,0,0 )
            Rectangle(pos=self.map.pos,size=self.map.size) 
        
        for body in self.primary.orbiting_bodies:
            body.generate_orbital_image()
            
            if not body.orbit_image.parent:
                self.map.add_widget( body.orbit_image, 'after' )
                                                            
                with self.map.canvas.before: 
                    Color( 0.5, 0.5, 0.25 )
                    Line(circle=( self.map.size[0]/2, self.map.size[1]/2, 0.5*self.map.size[0]*float(math.log((body.orbit+1),10)/self.orbit_constant)), dash_length=20, dash_offset = 10)



    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc Key """
        # If user presses Back/Esc Key
        if key == 27 or key == 1001:
            if self in globalvars.root.children:
                globalvars.root.remove_widget(self)
                return True
        return False
            
        
