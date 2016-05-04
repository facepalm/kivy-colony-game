from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


import globalvars
import util


trans_view_kv = '''
<TransferView>:
    id: tview
    size_hint: 0.9, 0.9
    pos_hint: {'center_x': .5, 'center_y': .5}
    
    FloatLayout:
        canvas:              
            Color:
                rgb: (0.5, 0.5, 0.75)  
            BorderImage:
                border: 10,10,10,10
                source: 'images/kivy/button_white.png'
                pos: self.pos
                size: self.size
    
'''
Builder.load_string(trans_view_kv)            

class TransferView(Screen):
    def __init__(self, **kwargs):
        self.site = kwargs['site']
        self.name = util.short_id(self.site.id)+'-transfer'
        super(TransferView, self).__init__(**kwargs)                    

