import pygame

class ObjectRenderer:
    """class used to draw the objects and entities on the screen"""
    def __init__(self, screen):
        # the pygame.surface to draw to
        self.screen = screen
    
    def renderWorldObject(self, worldObject):
        """draw the worldObject's rect in its color"""
        pygame.draw.rect(self.screen, worldObject.get_color(), worldObject.get_hitBox())
        
    def renderWorldObjects(self, worldObjects):
        """ draws the world objects passed by delegating to the renderWorldObject method"""
        for worldObject in worldObjects:
            self.renderWorldObject(worldObject)