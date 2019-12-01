import pygame
from enum import IntEnum

class SNESController:
    """Representation of a SNES controller with helpful functions for handling input and getting button states"""
    
    def __init__(self, joystickId):
        # init the joystick for the id
        self.joystick = pygame.joystick.Joystick(joystickId)
        self.joystick.init()
        # create a variable for the mappings of each of our buttons
        self.buttonMappings = {}
        # the button mappings for the directional pad on the controller
        self.directionalMappings = {}
        # store the joystick id in a variable for quick access
        self.joystickId = joystickId
        
    def get_buttonState(self, button):
        """gets the state of button represented by the passed buttonName. The button cannot be one of the direction buttons. buttonName is a value in the SNESButtons enum"""
        return self.joystick.get_button(button.value)
        
    def map_button(self, button, pressCommand = None, releaseCommand = None):
        """used to set a particular function to be called when the passed button is pressed. the command must not take any parameters, making a lambda function useful for the commands"""
        # if command is not none, then register the button to the command
        if pressCommand is not None and releaseCommand is not None:
            self.buttonMappings[button] = {'press': pressCommand, 'release': releaseCommand}
        else:
            # deregister the button
            del self.buttonMappings[button]
            
    def map_directionalButton(self, axis, positiveCommand = None, negativeCommand = None, releaseCommand = None):
        """used to set a particular function to be called for each state of the passed axis for the directional pad of the controller. The states are positive, negative, and release (0)"""
        # if all 3 commands are set, then register the button to the commands
        if positiveCommand is not None and negativeCommand is not None and releaseCommand is not None:
            self.directionalMappings[axis] = {'positive': positiveCommand, 'negative': negativeCommand, 'release': releaseCommand}
        else:
            # deregister the axis
            del self.directionalMappings[axis]

    def press_button(self, button):
        """calls the function associated with the passed button, if that button is mapped to anything"""
        if button in self.buttonMappings:
            # call the function defined in the press function
            self.buttonMappings[button]['press']()
            
    def release_button(self, button):
        """calls the function associated with releasing the passed button, if that button has been mapped to a function"""
        if button in self.buttonMappings:
            self.buttonMappings[button]['release']()
    
    def press_directionalButton(self, axis, direction):
        """calls the function associated with pressing the directional pad on the passed axis"""
        if axis in self.directionalMappings:
            # determine which function to call based on the state of the axis (negative, 0, or positive)
            if direction < 0:
                self.directionalMappings[axis]['negative']()
            elif direction == 0:
                self.directionalMappings[axis]['release']()
            else:
                self.directionalMappings[axis]['positive']()
    
    def get_controllerNumber(self):
        return self.joystickId
    
class SNESButtons(IntEnum):
    """enum for the list of non-directional buttons on a snes controller"""
    X = 0
    A = 1
    B = 2
    Y = 3
    LBUMPER = 4
    RBUMPER = 5
    SELECT = 8

class SNESAxes(IntEnum):
    """
        enum for a list of the directional buttons on a snes controller
        
        For a note to later so I don't forget: pygame uses a value of 1/-1 for when the button is pressed, and 0 for when it's released
    """
    HORIZONTAL = 0
    VERTICAL = 1