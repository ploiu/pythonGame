import pygame, random, math, time

class WorldObject:
    """
        The base class for any object that exists in the world
        All objects have an X and Y coordinate, as well as a color, width, and height
    """
    def __init__(self, posX, posY, width, height, color, worldWidth = 500, worldHeight = 500):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.color = color
        # this object's hitbox that can be used for interaction purposes
        self.hitbox = pygame.Rect(posX, posY, width, height)
        self._worldWidth = worldWidth
        self._worldHeight = worldHeight
        
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
        # move our hitbox
        self.hitbox.left = self.posX
        self.hitbox.top = self.posY
        # reset our hitbox's size
        self.hitbox.width = self.width
        self.hitbox.height = self.height
       
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
        
    def update(self):
        """called whenever the world object needs to have its state updated"""
        pass
        
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
    
    def _update_location(self):
        """updates the location of this entity based on its current location and velocity, and also updates this entity's hitbox"""
        # the new x location this entity should be at
        newX = self.posX + self.velX
        # the new y location this entity should be at
        newY = self.posY + self.velY
        # clamp the locations in
        axesOutsideWorld = self.is_outsideWorld(newX, newY)
        if axesOutsideWorld['x'] or axesOutsideWorld['y']:
            finalLocations = self._clampLocationWithinWorldBounds(newX, newY)
            newX = finalLocations[0]
            newY = finalLocations[1]
        # update this entity's location and hitbox
        self.set_location(newX, newY)
        
    def _clampLocationWithinWorldBounds(self, newX, newY):
        """ensures that the passed newX and newY are within this entity's world limits. If they go outside the bounds, they are clamped within them"""
        # the real x and y positions to use
        finalX, finalY = newX, newY
        if newX <= 0:
            finalX = 0
        elif newX + self.width >= self._worldWidth:
            finalX = self._worldWidth - self.width
        # for the y axis
        if newY <= 0:
            finalY = 0
        elif newY + self.height >= self._worldHeight:
            finalY = self._worldHeight - self.height    
        
        return finalX, finalY
        
    def is_outsideWorld(self, newX, newY):
        """checks if either the newX or newY are outside the coordinates of the viewable world"""
        # a dict of which axes are outside
        axes = {}
        axes['x'] = True if newX <= 0 or (newX + self.width >= self._worldWidth) else False
        axes['y'] = True if newY <= 0 or (newY + self.height >= self._worldHeight) else False
        return axes
        
    def update(self):
        """updates all necessary values of this entity, called within the game loop"""
        # update the entity's location
        self._update_location()
        
class Player(Entity):
    """A Player is a type of entity that can be controlled with a controller"""
    def __init__(self, playerNumber = 0, posX = 0, posY = 0):
        # the array of colors to use that corresponds to the player number
        playerColors = [(255, 0, 50), (50, 0, 255)]
        self.playerNumber = playerNumber
        Entity.__init__(self, posX, posY, 10, 120, playerColors[playerNumber], 5, 7)
        # the player's score
        self.score = 0
        # the list of powerUps the player has
        self.powerUps = []
        
    def use_powerUp(self, powerUpId):
        """calls the function on one of our powerUps that has the passed powerUpId. If no matching powerUp is found, nothing will happen"""
        # get the powerUp associated with the id
        foundPowerupIndex = self._get_firstIndexForPowerUp(powerUpId)
        if foundPowerupIndex > -1:
            # call the function in the powerUp
            self.powerUps[foundPowerupIndex]['action']()
            # remove the powerUp from the player
            del self.powerUps[foundPowerupIndex]
        
    def _get_firstIndexForPowerUp(self, powerUpId):
        """gets the first index of a powerUp with the passed powerUpId, or -1 if no matching powerUp exists"""
        return next((index for index,powerUp in enumerate(self.powerUps) if powerUp['id'] == powerUpId), -1)
    
    def add_powerUp(self, powerUpItem):
        """adds the passed powerUpItem to our powerUp list. Since the max amount of powerUps a player can have is 4, the oldest powerUp is removed if the player already has 4"""
        # only can have 4 powerUps, so make sure that we remove the oldest one if we already have 4
        if len(self.powerUps) == 4:
            del self.powerUps[0]
        # add the powerUpItem to the list
        self.powerUps.append(powerUpItem)
        
    def get_powerUps(self):
        return self.powerUps
        
        
class Ball(Entity):
    def __init__(self, players):
        Entity.__init__(self, 250, 250, 10, 10, (255, 255, 255), 3, 3)
        # currenly no owner
        self.owner = 'none'
        # the list of players this ball has to use in order to bounce off of them
        self.__players = players

        
    def switch_owner(self, player = None):
        # set the color of the ball
        self.color = (255, 255, 255) if player is None else player.color
        self.owner = 'none' if player is None else player

    def _update_location(self):
        # the new x location this entity should be at
        newX = self.posX + self.velX
        # the new y location this entity should be at
        newY = self.posY + self.velY
        # clamp the locations in
        axesOutsideWorld = self.is_outsideWorld(newX, newY)
        if axesOutsideWorld['x']:
            # a goal has been scored! post an event to pygame for our event handler to pick up
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, custom_type = 64, ball = self, position = newX))
        if axesOutsideWorld['y']:
            self.bounce(axis = 'y')
        
        # for each player, if this ball intersects with it, bounce the ball and change its owner
        for player in self.__players:
            if self.hitbox.colliderect(player.hitbox):
                # change the owner and bounce the ball on both axes
                self.switch_owner(player)
                self.bounce('x')
                # the amount to increase the ball's speed by
                speedIncrease = random.randint(1, 2)
                # if the player's y velocity was not 0, then change this ball's y velocity to match the player's
                if player.velY != 0:
                    self.velY = math.copysign(self.velY, player.velY)
                    self.velY += math.copysign(speedIncrease, self.velY)
                else:
                    # make the ball faster on the x axis
                    self.velX += math.copysign(speedIncrease, self.velX)
            
        Entity._update_location(self)
        
    def update(self):
        """updates all necessary values of this entity, called within the game loop"""
        # update the entity's location
        self._update_location()
        
    def bounce(self, axis = 'x', speedMult = 1.0):
        """changes the velocity of the ball based on the passed axis"""
        if axis == 'x':
            self.set_velocity((-self.velX) * speedMult, self.velY)
        else:
            self.set_velocity(self.velX, (-self.velY) * speedMult)
    
    def launch(self):
        """chooses a random velocity for the x and y axes to launch the ball at"""
        # the minimum speed for the ball
        minXSpeed = 4
        minYSpeed = 1
        self.set_size(10, 10)
        # get a random speed for the ball's x and y axes
        spdX = random.randint(-5, 5)
        spdY = random.randint(-3, 3)
        # make sure spdX and spdY aren't really slow or 0
        if spdX < 0:
            spdX = min(spdX, -minXSpeed)
        else:
            spdX = max(spdX, minXSpeed)
            
        if spdY < 0:
            spdY = min(spdY, -minYSpeed)
        else:
            spdY = max(spdY, minYSpeed)
        # pause for a moment to let the player's get their thoughts in order
        time.sleep(1)
        # set our velocities to spdX and spdY
        self.velX, self.velY = spdX, spdY