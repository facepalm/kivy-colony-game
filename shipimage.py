
import random
import math
from kivy.uix.image import Image
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix

import globalvars
import util


shipimages = {  'Ark': 'images/endless-sky/images/ship/world-ship a.png',
                'Default': 'images/endless-sky/images/ship/surveillance drone.png' }

class ShipImage(Image):
    pressed = ListProperty([0, 0])
    
    def __init__(self,**kwargs):
        super(ShipImage, self).__init__(**kwargs)
        self.ship = kwargs['ship'] if 'ship' in kwargs else None
