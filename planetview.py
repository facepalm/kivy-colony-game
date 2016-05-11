import kivy
kivy.require('1.9.2')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen

import math
import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from kivy.core.window import Window
from kivy.graphics.context_instructions import Scale
from kivy.lang import Builder

import globalvars
import matplotlib.pyplot as plt
import planetresources
import siteview
import util
from resource_views import RawResourceSquare

kv = '''
<PlanetPanel>:
    size_hint: 0.9, 0.9
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
        FloatLayout:
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
            Button:
                size_hint: .2, .2
                pos_hint: {'center_x': .88, 'center_y': .12}
                text: "View"
                on_press: panel.switch_system()
        BoxLayout:
            orientation: 'vertical'
            size_hint: 0.5, 0.25
            padding: 10, 10, 10, 10
            Label:
                text: panel.planet.type + ' "' + panel.planet.name + '"'
                font_size: 24
            Label:
                text: "Orbit: %.2f AU   Launch dV: %.2f km/s" % (panel.planet.orbit, panel.planet.launch_dv()/1000)
                font_size: 16
            Label:
                text: "{0:.0f} % explored".format(100*panel.planet.explored)
                font_size: 16
                id: exploration_string
                              
        BoxLayout:
            size_hint: 0.25, 0.25
            id: resimg
            #pos_hint: {'center_x': .5, 'center_y': .5}
                
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

class PlanetPanel(Screen):
    def __init__(self, **kwargs):
        self.planet = kwargs['planet']
        
        self.name = util.short_id(self.planet.id)+'-planet'
        
        nr = 1.0*planetresources.raw_num
        pr = self.planet.resources.raw.squeeze()
        x = np.arange(0,2*math.pi,(2/nr)*math.pi)
        x = np.append(x,0)
        pr = np.append(pr,pr[0])
        print x, pr
        
        '''plt.polar(x,pr,'b')
        plt.fill_between(x,pr,color='#5c7de8',alpha=0.75)
        plt.thetagrids(np.arange(0,360,360/nr),[])#planetresources.raw_names)
        plt.ylim(0,1)
        plt.yticks([2.0])
        
        plt.savefig('temp.png',bbox_inches='tight',dpi=300)
        plt.clf()'''
        
        #im = plt.imread('temp.png')
        #width=250
        #self.imbuf = im[300-width:300+width,410-width:410+width,:]
        #self.imtex = Texture.create(size=(500,500), colorfmt='rgba')
        #self.imtex.blit_buffer(self.imbuf.tostring(), colorfmt='rgba', bufferfmt='ubyte')

        #plt.imshow(im[300-width:300+width,410-width:410+width,:])
        #plt.savefig('temp.png')
        #plt.show()
        
        super(PlanetPanel, self).__init__(**kwargs)
        
        pr = RawResourceSquare(planetresources = self.planet.resources)
        self.ids['resimg'].add_widget(pr)
        
        for s in self.planet.sites:    
            b = BoxLayout(size_hint_y =None,height=100)
            b.add_widget(s.small_view())
            self.ids['panel3'].add_widget(b)
                      
            
        #Window.bind(on_keyboard=self.onBackBtn)        

    def switch_system(self):
        print 'switching to',self.planet.name
        globalvars.root.onNextScreen(util.short_id(self.planet.id)+"-system" )
    
        
    def on_pre_enter(self):
        self.ids['exploration_string'].text = "{0:.0f} % explored".format(100*self.planet.explored)
        
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
            #return True
                  
    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc Key """
        # If user presses Back/Esc Key
        if key == 27 or key == 1001:
            if self in globalvars.root.children:
                globalvars.root.remove_widget(self)
                return True
        return False       '''           
                  
