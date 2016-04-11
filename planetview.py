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

from kivy.core.window import Window
from kivy.graphics.context_instructions import Scale
from kivy.lang import Builder

import globalvars

kv = '''
<PlanetPanel>:
    size_hint: 0.8, 0.8
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas:
        Color:
            rgb: (0.05, 0.05, 0.05)
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgb: (0.25, 0.25, 0.5)
        Line:
            rectangle: self.x,self.y,self.width,self.height
            width: 2
    
'''

Builder.load_string(kv)

class PlanetPanel(StackLayout):
    def __init__(self, **kwargs):
        super(PlanetPanel, self).__init__(**kwargs)
        self.planet = kwargs['planet']

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
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
            
