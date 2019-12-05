import pygame, controllers

class ComponentManager:
    def __init__(self):
        # the controllers pygame has discovered
        self._controllers = []
        
    def create_gamePadFromJoyStick(self, joystickId):
        # the created controller
        controller = controllers.Controller(joystickId)
        # add the controller to our list of controllers
        self._controllers.append(controller)
        
    def get_controllers(self):
        return self._controllers
    
    def get_controller(self, controllerNum):
        return self._controllers[controllerNum]
    
    def register_controllers(self, controllerCount):
        for controllerNum in range(controllerCount):
            self.create_gamePadFromJoyStick(controllerNum)