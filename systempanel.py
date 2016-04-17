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

orbit_constant = 3.0

class SystemView(ScrollView):
    def __init__(self, **kwargs):
        super(SystemView, self).__init__(**kwargs)
        self.map = FloatLayout(size=(2000,2000),size_hint = (None, None))
        self.add_widget(self.map)
        self.primary = kwargs['primary']
        self.orbit_constant = orbit_constant #scaling factor for map
        #self.scale = None
        
        self.map.add_widget(self.primary.primary_image())      
        self.scroll_x = 0.5
        self.scroll_y = 0.5
        #self.size=(1000,1000)          
        #self.size_hint=(1,1)
        
        #globalvars.root.add_widget(self)
         
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
            #if body.orbit_image.parent and ((body.orbit_image.parent.parent and body.orbit_image.parent.parent is not self.map) or clear):
            #    #remove body's designation 
            #    #print "Stealing", body,"from", body.orbit_image.parent              
            #    body.orbit_image.parent.remove_widget(body.orbit_image)
            
            if not body.orbit_image.parent:
                
                #tmpframe = FloatLayout(size=(10,10),pos=(x*self.map.size[0],y*self.map.size[1]))
                    #tmpframe.pos_hint['center_x'] = (ph['center_x']-0.5)/self.orbit_constant + 0.5
                    #tmpframe.pos_hint['center_y'] = (ph['center_y']-0.5)/self.orbit_constant + 0.5
                    #print ph['center_x'], x,y, tmpframe.pos                    
                    #tmpframe.add_widget( body.orbit_image, 'after' )
                #body.orbit_image.pos_hint = {'center_x': x, 'center_y':y}
                #body.orbit_image.pos_hint = (x,y)
                self.map.add_widget( body.orbit_image, 'after' )
                
            
                with self.map.canvas.before:                                        
                    #self.map.canvas.opacity = 0.5
                    Color( 0.5, 0.5, 0.25 )
                    #print self.to_window(self.center_x, self.center_y)
                    #print Window.size[0], self.size[0]
                    #print 1000*float(math.log((body.orbit+1),10)/2)
                    Line(circle=( self.map.size[0]/2, self.map.size[1]/2, 0.5*self.map.size[0]*float(math.log((body.orbit+1),10)/self.orbit_constant)), dash_length=20, dash_offset = 10)
                    #print 0.5*self.map.size[0]*float(math.log((body.orbit+1),10)/2), (.5+ (float(math.log((body.orbit+1),10))/(2.0))), (.5+ (float(math.log((body.orbit+1),10))/(2.0)))*self.map.size[0]
                    
                #with self.map.canvas:
                #self.map.add_widget( tmpframe )
                  
                #with tmpframe.canvas.after:
                #    Line(circle=( 0, 0, 5 ))
                    
                    #body.orbit_image.opacity = 10
                    #self.map.add_widget( body.orbit_image, 'after' )
        #self.map.canvas.before.insert(0,Scale( 1/self.orbit_constant, 1/self.orbit_constant, 1.0, origin = (self.map.size[0]/2,self.map.size[1]/2)))
        #self.map.canvas.before.add(Line(circle=( 1000, 1000, 100)))


    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc Key """
        # If user presses Back/Esc Key
        if key == 27 or key == 1001:
            if self in globalvars.root.children:
                globalvars.root.remove_widget(self)
                return True
        return False
            
        
