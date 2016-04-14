import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
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

entry_small_kv = '''
<SiteEntrySmall>:
    orientation: 'horizontal'
    
    canvas:
        Color:
            rgb: (0.05, 0.05, 0.15)
        Rectangle:
            size: self.size[0], self.size[1]*0.9
            pos: self.pos      
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
                  
