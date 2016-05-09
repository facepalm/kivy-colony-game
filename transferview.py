from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel


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
    Label:
        text: 'Destination:'
        size_hint: 1, 0.1
    ScrollView:
        id:treepanel
        do_scroll_x: False
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: 1, 0.75
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
        
        right = RightPanel()
        dest_tree = TransferTree()
        right.ids['treepanel'].add_widget(dest_tree)
        
        super(TransferView, self).__init__(**kwargs)                    
        print self.ids
        self.ids['mainpanel'].add_widget(left)
        self.ids['mainpanel'].add_widget(MidPanel())
        self.ids['mainpanel'].add_widget(right)
        
        
tree_view_kv = '''
<TransferTree>:
    

'''        
Builder.load_string(tree_view_kv)            

class TransferTree(TreeView):
    def __init__(self, **kwargs):    
        self.system = kwargs['system'] if 'system' in kwargs else globalvars.universe.primary
        super(TransferTree, self).__init__(**kwargs)                    
                                                
        self.populate(None,self.system)

        #quit()
                
    def populate(self,node=None,body=None):
        if hasattr(body,'orbiting_bodies'):
            if node: node.no_selection=True
            for o in body.orbiting_bodies:
                l = TreeViewLabel(text=o.name)
                n = self.add_node(l,node)
                self.populate(n,o)
        if hasattr(body,'sites'):
            if node: node.no_selection=True
            for o in body.sites:
                l = TreeViewLabel(text=o.name)
                n = self.add_node(l,node)
                self.populate(n,o)
                      
