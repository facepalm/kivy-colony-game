from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.properties import NumericProperty


import globalvars
import util
import resource_views




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
    BoxLayout:
        id: resourcepanel
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
    ship_mass: 0
    destination: None
    resources: None
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1,.1
    BoxLayout:
        orientation: 'vertical'   
        pos_hint: {'center_x': .5, 'center_y': .25}   
        size_hint: .9,.9
        canvas:
            Color:
                rgb: (0.05, 0.05, 0.05)
            Rectangle:
                size: self.size
                pos: self.pos
        Label:
            text: 'Transfer mass: '+str(root.ship_mass)
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1,1
        Label:
            text: 'Buttons go here'

<RightPanel>:
    orientation: 'vertical'
    Label:
        text: 'Destination:'
        size_hint: 1, 0.1
    ScrollView:
        id:treepanel
        do_scroll_x: False
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: 1, 1
        canvas:
            Color:
                rgb: (0.5, 0.5, 0.75)              
            BorderImage:
                border: 10,10,10,10
                source: 'images/kivy/button_white.png'
                pos: self.pos
                size: self.size   
'''        

args_converter = lambda row_index, an_obj: {'size_hint_y': None,
                                         'height': 25,
                                         'ident': an_obj.id,
                                         'ship': an_obj}

Builder.load_string(trans_view_kv)            

class CustomListItem(ListItemButton):
    def __init__(self, **kwargs):
        self.ship=kwargs['ship']
        self.ident=kwargs['ident']
        self.text = self.ship.name()
        super(CustomListItem, self).__init__(**kwargs)       

class LeftPanel(BoxLayout):
    pass

class MidPanel(BoxLayout):
    ship_mass = NumericProperty()

    def ships_changed(self, ship_adapter, *args):
        ship_mass = 0

        for ship in ship_adapter.selection:    
            ship_mass += float(ship.ship.mass())
        self.ship_mass = ship_mass            

    def dest_selected(self,tree,node):
        print args
        print node.text
    
class RightPanel(BoxLayout):
    pass    

class TransferView(Screen):
    def __init__(self, **kwargs):
        self.site = kwargs['site']
        self.name = util.short_id(self.site.id)+'-transfer'
        
        mid = MidPanel()
        
        print self.site.stuff
        
        list_adapter = ListAdapter(data=self.site.stuff,
                           args_converter=args_converter,
                           cls=CustomListItem,
                           selection_mode='multiple',
                           allow_empty_selection=True)

        list_view = ListView(adapter=list_adapter)
        list_adapter.bind(on_selection_change = mid.ships_changed)
    

        resv = resource_views.ResourceSelector(resources=self.site.resources)

        left = LeftPanel()
        left.ids['shipchoicepanel'].add_widget(list_view)
        left.ids['resourcepanel'].add_widget(resv)
        
        right = RightPanel()
        dest_tree = TransferTree()
        
        right.ids['treepanel'].add_widget(dest_tree)
        
        super(TransferView, self).__init__(**kwargs)                    

        self.ids['mainpanel'].add_widget(left)
        self.ids['mainpanel'].add_widget(mid)
        self.ids['mainpanel'].add_widget(right)
        
        
tree_view_kv = '''
<TransferTree>:
    size_hint: 1, None

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
                      
    #def on_touch_down(self, touch):
    #    super(TransferTree, self).on_touch_down(touch)
    #    #self.map.on_touch_down(touch)
    #    return False     
                      
    def on_node_expand(self,node, ):
        #print self.minimum_height
        self.height = self.minimum_height+200
        #if self.parent: 
            #self.parent.update_from_scroll()
        #    print self.parent.viewport_size
        #print self.size           
                              
