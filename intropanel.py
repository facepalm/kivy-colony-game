import kivy
kivy.require('1.9.2')

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class ScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollView, self).__init__(**kwargs)
        with self.canvas.before:
            self.color = Color(0.20,0.20,0.20)
            self.rect = Rectangle(pos=self.pos, size=self.size)
    
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)


class IntroPanelView(AnchorLayout):
    introtext = '''[color=aaaaaa]
[size=10]-~- No autosave found.  Initializing new game -~-[/size][color=ffffff]     
   
It's been a while.
    
Over four centuries ago, 
    
    blah
    blah
    blha
    
You have finally arrived at your destination.  You are nearly out of AM3 fuel for your antimatter engines.
    
Not much about your target system is known, save that it is complex, i.e. its sun has irregular fluctuations indicative of a multi-body solar systems, and it has at least one roughly Earth-sized planet in the habitable zone, a.k.a. the "Goldilocks" region.
    
It will have to do.[/color]
    '''

    def __init__(self, **kwargs):
        super(IntroPanelView, self).__init__(**kwargs)
        
        
        # create a default grid layout with custom width/height
        layout = GridLayout(cols=1, padding=10, spacing=10,
                size_hint=(None, None),pos_hint={'center_x': .5, 'center_y': .5}, width=500)
        
        layout.bind(minimum_height=layout.setter('height'))

        # create a scroll view, with a size < size of the grid
        scrl = ScrollView(size_hint=(None, None), size=(500, 320),
                pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        
        label = Label(
            text=self.introtext,
            size=(480, 500),
            text_size=(480,500),
            size_hint_y=None,
            markup=True)
        
        scrl.add_widget(label)
        layout.add_widget(scrl)
        
        btn = Button(text='Okay', size=(480, 40),
                         size_hint=(None, None), on_press=self.close)
        
        layout.add_widget(btn)
        
        self.add_widget(layout)
        
    def close(self, instance):
        self.parent.remove_widget(self)

