from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.boxlayout import BoxLayout

import globalvars
import util


args_converter = lambda row_index, an_obj: {'text': an_obj.name(),
                                         'size_hint_y': None,
                                         'height': 25}


trans_view_kv = '''
<TransferView>:
    id: tview
    size_hint: 0.9, 0.9
    pos_hint: {'center_x': .5, 'center_y': .5}
    
    BoxLayout:
        id: mainpanel
        canvas:              
            Color:
                rgb: (0.5, 0.5, 0.75)  
            BorderImage:
                border: 10,10,10,10
                source: 'images/kivy/button_white.png'
                pos: self.pos
                size: self.size
    
<LeftPanel>:
    orientation: 'vertical'
    Label:
        text: 'Transfer:'
        size_hint: 1, 0.1
    BoxLayout:
        id: shipchoicepanel
        orientation: 'vertical'
        padding: 15,15
       
        canvas:
            Color:
                rgb: (0.5, 0.5, 0.75)              
            BorderImage:
                border: 10,10,10,10
                source: 'images/kivy/button_white.png'
                pos: self.pos
                size: self.size   

<MidPanel>:
    orientation: 'vertical'

<RightPanel>:
    orientation: 'vertical'
        
    
'''
Builder.load_string(trans_view_kv)            

class LeftPanel(BoxLayout):
    pass

class MidPanel(BoxLayout):
    pass
    
class RightPanel(BoxLayout):
    pass    

class TransferView(Screen):
    def __init__(self, **kwargs):
        self.site = kwargs['site']
        self.name = util.short_id(self.site.id)+'-transfer'
        
        list_adapter = ListAdapter(data=self.site.stuff,
                           args_converter=args_converter,
                           cls=ListItemButton,
                           selection_mode='multiple',
                           allow_empty_selection=False)

        list_view = ListView(adapter=list_adapter)

        left = LeftPanel()
        left.ids['shipchoicepanel'].add_widget(list_view)
        
        super(TransferView, self).__init__(**kwargs)                    
        print self.ids
        self.ids['mainpanel'].add_widget(left)
        self.ids['mainpanel'].add_widget(MidPanel())
        self.ids['mainpanel'].add_widget(BoxLayout())
        
