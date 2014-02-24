#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
'''
Created on 21.02.2014

@author: Tim
'''

class Gamepad(object):
    '''
    represents the gamepad with all buttons and axis values
    '''

    def __init__(self):
        self.axisLeft_X = 0
        self.axisLeft_Y = 0
        self.axisRight_X = 0
        self.axisRight_Y = 0

        self.buttons = {'triangle': False, 'square': False, 'cross': False, 'circle': False,
                        'up': False, 'down': False, 'left': False, 'right': False,
                        'L1': False, 'L2': False, 'R1': False, 'R2': False,
                        'select': False, 'start': False, 'ps3': False, 'leftstick': False, 'rightstick': False}

    def __str__(self, *args, **kwargs):
        def _format(button):
            return str(int(self.buttons[button]))
        
        symbols = _format("square")+_format("cross")+_format("circle")+_format("triangle")
        direction = _format("up")+_format("down")+_format("left")+_format("right")
        r_buttons = _format("R1")+_format("R2")
        l_buttons = _format("L1")+_format("L2")
        
        axis = "Axis %.2f   %.2f   %.2f   %.2f" % (self.axisLeft_X,self.axisLeft_Y,self.axisRight_X,self.axisRight_Y)
        specials = "select %s  strt %s  ps3 %s" % (_format("select"),_format("start"),_format("ps3"))
        
        
        return u"Gamepad {□x○^ %s  |  udLR %s  |  R12 %s  |  L12 %s  |  %s  |  %s}" % (symbols, direction,r_buttons,l_buttons,axis,specials)