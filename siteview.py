import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
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

entry_small_kv = '''
<MineLoc@Widget>:
    size: 25,25
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas:
        BorderImage:
            border: 5,5,5,5
            source: 'images/kivy/button_white.png'
            pos: self.center_x-10, self.center_y - 10
            size: 20,20

<SiteEntrySmall>:
    orientation: 'horizontal'
    id: entry
    
    canvas:
        Color:
            rgb: (0.05, 0.05, 0.15)
        Rectangle:
            size: self.size[0], self.size[1]*0.9
            pos: self.pos     
            
    Label:
        text: entry.site.location    
    
    MineLoc:
        opacity: 0.1 if not entry.site.mine[0] else 1.0
    MineLoc:
        opacity: 0.1 if not entry.site.mine[1] else 1.0
    MineLoc:
        opacity: 0.1 if not entry.site.mine[2] else 1.0
    MineLoc:
        opacity: 0.1 if not entry.site.mine[3] else 1.0        
    MineLoc:
        opacity: 0.1 if not entry.site.mine[4] else 1.0                    
    MineLoc:
        opacity: 0.1 if not entry.site.mine[5] else 1.0        
    MineLoc:
        opacity: 0.1 if not entry.site.mine[6] else 1.0                        
    MineLoc:
        opacity: 0.1 if not entry.site.mine[7] else 1.0        
    MineLoc:
        opacity: 0.1 if not entry.site.mine[8] else 1.0            
    Label:
        text: "End"       
'''


Builder.load_string(entry_small_kv)

class SiteEntrySmall(BoxLayout):
    def __init__(self, **kwargs):
        self.site = kwargs['site']
        super(SiteEntrySmall, self).__init__(**kwargs)                
        
        
    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_widget)
        touched = self.collide_point(*touch.pos)
        touch.pop()
        if touched:
            print self.site.location, self.site.resources, self.site.effective_resources
