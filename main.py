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
        globalvars.root = root
        autoloaded = util.autoload() if globalvars.config['AUTOLOAD'] else False
                
        #root.add_widget( Image( source = 'generic_sun.png'))#'NGC134_70wendel1024.jpg' ) )  
                
            
                
        if not autoloaded:
            #generate universe
            globalvars.universe = game.Universe()
            #autosave?
            
        
        root.add_widget (globalvars.universe.primary.view)                
        globalvars.universe.primary.view.update(clear=True)
        
                
        #if not autoloaded: root.add_widget( IntroPanelView() )
        return root

if __name__ == '__main__':
    GameApp().run()
