import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout

from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Color, Rectangle, PopMatrix, PushMatrix, Rotate
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen

import math
import numpy as np

from kivy.core.window import Window
from kivy.graphics.context_instructions import Scale
from kivy.lang import Builder

import globalvars

import util
import shipimage

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
            size: self.size[0] - 10, self.size[1]-10
            pos: self.pos[0]+5, self.pos[1]+5
            
    Label:
        size_hint: 0.25,1
        text: entry.site.fancy_name  
    
    GridLayout:
        size_hint: 0.15,0.7
        pos_hint: {'center_x': .5, 'center_y': .5}
        rows: 3
        cols: 3
        #padding: 15, 15
        MineLoc:
            opacity: 0.1 if entry.site.mine[0] > entry.site.explored else 1.0
        MineLoc:
            opacity: 0.1 if entry.site.mine[1] > entry.site.explored else 1.0
        MineLoc:
            opacity: 0.1 if entry.site.mine[2] > entry.site.explored else 1.0
        MineLoc:
            opacity: 0.1 if entry.site.mine[3] > entry.site.explored else 1.0        
        MineLoc:
            opacity: 0.1 if entry.site.mine[4] > entry.site.explored else 1.0                    
        MineLoc:
            opacity: 0.1 if entry.site.mine[5] > entry.site.explored else 1.0        
        MineLoc:
            opacity: 0.1 if entry.site.mine[6] > entry.site.explored else 1.0                        
        MineLoc:
            opacity: 0.1 if entry.site.mine[7] > entry.site.explored else 1.0        
        MineLoc:
            opacity: 0.1 if entry.site.mine[8] > entry.site.explored else 1.0            
    StackLayout:
        id: ships
        orientation: 'tb-lr'
'''


Builder.load_string(entry_small_kv)

class SiteEntrySmall(BoxLayout):
    def __init__(self, **kwargs):
        self.site = kwargs['site']
        super(SiteEntrySmall, self).__init__(**kwargs)                
        
        for s in self.site.stuff:
            self.ids['ships'].add_widget(s.image)
        
        
    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)
        touch.pop()
        if touched:
            print self.site.location, self.site.resources.virtual
            sname = util.short_id(self.site.id)+'-site'
            if not globalvars.root.screen_manager.has_screen(sname):
                s = SiteView(site=self.site)
                globalvars.root.screen_manager.add_widget( s )
            globalvars.root.onNextScreen(sname)
            
site_view_kv = '''
<ShipTwist>:
    size_hint_y: None
    height: 50
    canvas.before:
        PushMatrix
        Rotate:
            angle: 0
            origin: self.center
    canvas.after:
        PopMatrix
    
<ShipBox>:
    size_hint_y: None
    height: 50
    ShipImage:
        id: ship
        ship: 'None'
        canvas.before:
            PushMatrix
            Rotate:
                angle: 90
                origin: self.parent.center
        canvas.after:
            PopMatrix

<SiteView>:
    id: sview
    size_hint: 0.9, 0.9
    pos_hint: {'center_x': .5, 'center_y': .5}
    
    FloatLayout:
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
        StackLayout:
            pos_hint: {'x': 0, 'y':0}
            size_hint: 0.25,0.75
            canvas:
                Color:
                    rgb: (0.45, 0.45, 0.45)
                BorderImage:
                    border: 5,5,5,5
                    source: 'images/kivy/button_white.png'
                    pos: self.pos
                    size: self.size 
            Label:
                text: 'Occupants'
                size_hint: 1, 0.25
            ScrollView:
                do_scroll_x: False
                pos_hint: {'center_x': .5, 'center_y': .5}
                size_hint: 1, 0.75
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    orientation: 'vertical'
                    id: shiplist
                    size_hint_y: None
                    height: 50*len(sview.site.stuff)
                
                
        BoxLayout:
            pos_hint: {'right': 1, 'top':1}
            size_hint: 0.75,0.25     
            
            BoxLayout:                
                Label:
                    text: 'Site'
                Label:
                    text: 'Site info'
        BoxLayout:
            pos_hint: {'center_x': 0.5, 'y':0}
            size_hint: 0.5,0.75     
            id: panel
            display: 'Info'
            canvas:
                Color:
                    rgb: (0.05, 0.05, 0.05)
                Rectangle:
                    size: self.size
                    pos: self.pos
            
            BoxLayout:
                orientation: 'vertical'                
                Label:
                    text: 'Info Panel'  
        
        BoxLayout:
            pos_hint: {'right': 1, 'y':0}
            size_hint: 0.25,0.75     
            
            BoxLayout:
                padding: 10,10,10,10
                orientation: 'vertical'                
                Button:
                    text: 'Info'
                Button:
                    text: 'Build'
                Button:
                    text: 'Transfer'
                Label:
                    text: 'Button'
                Label:
                    text: 'Button'
                    
                     
                
'''


Builder.load_string(site_view_kv)            
            
class ShipTwist(shipimage.ShipImage):            
    pass            
            
class ShipBox(BoxLayout):
    pass            
            
class SiteView(Screen):
    def __init__(self, **kwargs):
        self.site = kwargs['site']
        self.name = util.short_id(self.site.id)+'-site'
        super(SiteView, self).__init__(**kwargs)                    
        
        for s in self.site.stuff:    
            b = ShipTwist(ship=s, source = shipimage.shipimages[s.imagename])
            self.ids['shiplist'].add_widget(b)
