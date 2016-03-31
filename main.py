import kivy
kivy.require('1.9.2')

from kivy.app import App
from intropanel import IntroPanelView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image

import util
import globalvars
import game

#graphics stuff

class GameApp(App):

    def build(self):
        root = AnchorLayout()
        autoloaded = util.autoload() if globalvars.config['AUTOLOAD'] else False
                
        root.add_widget( Image( source = 'NGC134_70wendel1024.jpg' ) )        
                
        if not autoloaded:
            #generate universe
            globalvars.universe = game.Universe()
            
            #autosave()
            root.add_widget( IntroPanelView() )
        return root

if __name__ == '__main__':
    GameApp().run()
