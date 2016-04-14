import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

import math
import numpy as np

from kivy.core.window import Window
from kivy.graphics.context_instructions import Scale
from kivy.lang import Builder

import globalvars
import matplotlib.pyplot as plt
import planetresources
import siteview

kv = '''
<PlanetPanel>:
    size_hint: 0.8, 0.8
    #size: app.root_window.width*0.8,app.root_window.height*0.8
    pos_hint: {'center_x': .5, 'center_y': .5}
    
    id: panel
    StackLayout:
        id: panel2
        size_hint: 1, 1
        canvas:
            Color:
                rgb: (0.05, 0.05, 0.05)
            Rectangle:
                size: self.size
                pos: self.pos  
            Color:
                rgb: (0.5, 0.5, 0.75)  
            BorderImage:
                border: 10,10,10,10
                source: 'images/kivy/button_white.png'
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint: 0.25, 0.25

            canvas:
                Color:
                    rgb: (0.5, 0.5, 0.5)
                BorderImage:
                    border: 5,5,5,5
                    source: 'images/kivy/button_white.png'
                    pos: self.pos
                    size: self.size
            Image:
                size_hint: 1, 1
                pos_hint: {'center_x': .5, 'center_y': .5}
                source: panel.planet.image
        BoxLayout:
            orientation: 'vertical'
            size_hint: 0.5, 0.25
            padding: 10, 10, 10, 10
            Label:
                text: panel.planet.type + ' "' + panel.planet.name + '"'
                font_size: 24
            Label:
                text: "Orbit: %.2f AU" % panel.planet.orbit
                font_size: 16
            Label:
                text: "{0:.0f} % explored".format(100*panel.planet.exploration)
                font_size: 16
        FloatLayout:
            size_hint: 0.25, 0.25
            Button:
                size_hint: 0.90, 0.90
                pos_hint: {'center_x': .5, 'center_y': .5}
                text: "View"                                
        ScrollView:
            do_scroll_x: False
            pos_hint: {'center_x': .5, 'center_y': .5}
            size_hint: 1, 0.75
            
            BoxLayout:
                pos_hint: {'center_x': .5, 'center_y': .5}
                orientation: 'vertical'
                id: panel3
                size_hint_y: None
                height: 100*len(panel.planet.sites)
            
'''


Builder.load_string(kv)

class PlanetPanel(StackLayout):
    def __init__(self, **kwargs):
        self.planet = kwargs['planet']
        super(PlanetPanel, self).__init__(**kwargs)
        
        for s in self.planet.sites:    
            b = BoxLayout(size_hint_y =None,height=100)
            b.add_widget(s.small_view())
            self.ids['panel3'].add_widget(b)
            
        Window.bind(on_keyboard=self.onBackBtn)        

        '''pr = self.planet.resources.raw.squeeze()
        x = np.arange(0,2*math.pi,0.2*math.pi)
        x = np.append(x,0)
        pr = np.append(pr,pr[0])
        print x, pr
        plt.polar(x,pr,'b')
        plt.fill_between(x,pr,color='#5c7de8',alpha=0.75)
        plt.thetagrids(np.arange(0,360,36),planetresources.raw_names)
        plt.ylim(0,1)
        plt.yticks([2.0])
        plt.show()'''
        
    '''def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_widget)
        touched = self.collide_point(*touch.pos)
        touch.pop()
        if not touched:
            globalvars.root.remove_widget(self)
            return True
        else:
            return super(PlanetPanel, self).on_touch_down(touch)
            #return True'''
                  
    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc Key """
        # If user presses Back/Esc Key
        if key == 27 or key == 1001:
            if self in globalvars.root.children:
                globalvars.root.remove_widget(self)
                return True
        return False                  
                  
