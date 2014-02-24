# from input import gamepad

class KeyCombination(object):
    '''
    represents a combination of buttons on the gamepad
    '''

    def __init__(self, buttonlist):
        if (type(buttonlist) is list) == False:
            raise Exception("provide a list of buttons")
        
        self.buttonlist = buttonlist
        
        
    def isPressed(self,gamepad):
        result = True
        for currentButton in self.buttonlist:
            result = result & gamepad.buttons[currentButton] 
        
        return result
