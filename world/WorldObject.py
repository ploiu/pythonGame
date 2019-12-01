import pygame

class WorldObject:
    """
        The base class for any object that exists in the world
        All objects have an X and Y coordinate, as well as a color, width, and height
    """
    def __init__(self, posX, posY, width, height, color):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.color = color
        # this object's hitbox that can be used for interaction purposes
        self.hitbox = pygame.Rect(posX, posY, width, height)
        
    def set_location(self, x = None, y = None):
        """Updates the location of this object, using the passed-in x and y values"""
        # check if our x and y have values to determine what to update our posX and posY to
        if x is not None:
            self.posX = x
        if y is not None:
            self.posY = y
        # update our hitbox
        self.__updateHitBox()
        
    def get_location(self):
        """gets the location of this object in the world as a dict"""
        return {'x': self.posX, 'y': self.posY}
    
    def __updateHitBox(self):
        """updates the location and size of this object's hitbox"""
        # delete our current hitbox
        del self.hitbox
        # re-init our hitbox
        self.hitbox = pygame.Rect(self.posX, self.posY, self.width, self.height)
       
    def get_hitBox(self):
        return self.hitbox
    
    def get_color(self):
        return self.color
    
    def set_color(self, color = (0,0,0)):
        self.color = color
        
    def set_size(self, width = None, height = None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        # update our hitbox to reflect the changes
        self.__updateHitBox()
        
class Entity(WorldObject):
    """An entity is a type of world object that can move, and has an update method to update its state on every game loop"""
    def __init__(self, posX, posY, width, height, color, spdX, spdY):
        # the speed values are the base speeds used for the base velocity when the entity moves "on its own"
        self.__spdX = spdX
        self.__spdY = spdY
        # the velocity of this entity for each axis, which is used to determine the actual speed of the entity
        self.velX = 0
        self.velY = 0
        # call the super constructor
        WorldObject.__init__(self, posX, posY, width, height, color)
        
    def add_velocity(self, x = 0, y = 0):
        """adds to the current velocity of this entity with the passed values"""
        # update the x velocity
        self.velX += x
        self.velY += y
    
    def subtract_velocity(self, x = 0, y = 0):
        """subtracts the passed velocity values from this entity's current velocity. The passed-in arguments should be positive values"""
        self.add_velocity(-x, -y)
        
    def set_velocity(self, x = 0, y = 0):
        """sets the velocity of both x and y axes for this entity"""
        self.velX = x
        self.velY = y
    
    def get_speed(self):
        """gets the base speed values for this entity as a dict containing the x and y values"""
        return {'x': self.__spdX, 'y': self.__spdY}
    
    def get_velocity(self):
        """gets the current velocity for this entity as a dict containing the x and y velocities. These values are the 'true' speed of the entity currently"""
        return {'x': self.velX, 'y': self.velY}
    
    def __update_location(self):
        """updates the location of this entity based on its current location and velocity, and also updates this entity's hitbox"""
        # the new x location this entity should be at
        newX = self.posX + self.velX
        # the new y location this entity should be at
        newY = self.posY + self.velY
        # update this entity's location and hitbox
        self.set_location(newX, newY)
        
    def update(self):
        """updates all necessary values of this entity, called within the game loop"""
        # update the entity's location
        self.__update_location()
        
class Player(Entity):
    """A Player is a type of entity that can be controlled with a controller"""
    def __init__(self, color, posX = 0, posY = 0):
        Entity.__init__(self, posX, posY, 10, 10, color, 5, 5)
