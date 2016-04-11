import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout

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

kv = '''
<PlanetPanel>:
    size_hint: 0.8, 0.8
    pos_hint: {'center_x': .5, 'center_y': .5}
    id: panel
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
        size_hint: 0.2, 0.2

        canvas:
            Color:
                rgb: (0.5, 0.5, 0.5)
            BorderImage:
                border: 5,5,5,5
                source: 'images/kivy/button_white.png'
                pos: self.pos
                size: self.size
        Image:
            size_hint: 0.9, 0.9
            pos_hint: {'center_x': .5, 'center_y': .5}
            source: panel.planet.image
            
        
    BoxLayout:
        size_hint_y: None
        height: sp(100)
        canvas:
            Color:
                rgb: (0.05, 0.15, 0.05)
            Rectangle:
                size: self.size
                pos: self.pos                  
        
'''


Builder.load_string(kv)

class PlanetPanel(StackLayout):
    def __init__(self, **kwargs):
        self.planet = kwargs['planet']
        super(PlanetPanel, self).__init__(**kwargs)
        

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
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
        
    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_widget)
        touched = self.collide_point(*touch.pos)
        touch.pop()
        if not touched:
            globalvars.root.remove_widget(self)
            #self._keyboard_closed()
            return True
                  
    def _keyboard_closed(self):
        if self._keyboard: self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None    
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        keycode1 = keycode[0]
        
        if keycode1 == 27 or keycode1 == 1001:            
            globalvars.root.remove_widget(self)
            self._keyboard_closed()
            return True
        return False               
            
