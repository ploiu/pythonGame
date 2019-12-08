import world, enum, random

class PowerUp(world.WorldObject):
    def __init__(self, posX, posY, color, ball, players):
        world.WorldObject.__init__(self, posX, posY, 20, 20, color)
        # needed during initialization time because we can't easily get it later
        self._ball = ball
        self._players = players
        # the amount of time the powerUp has to live
        self.life = 540
        
    def _perform_action(self, owningPlayer = None):
        """function to be called when a player uses this powerUp"""
        pass
    
    def _get_powerUpId(self):
        """returns a numeric value representing the id of this power up"""
        return None
    
    def get_ItemForm(self, owningPlayer = None):
        """returns a dict, with the key being the id of the powerUp, and the value being this powerUp''s action"""
        return {'id': self._get_powerUpId(), 'action': (lambda: self._perform_action(owningPlayer)), 'color': self.color}
    
    def update(self):
        world.WorldObject.update(self)
        # decrease the amount of time the powerUp has left
        self.life -= 1
        # if the powerUp has been hit by the ball and it's not dead, kill the powerUp and give it to the player
        if self.life > 0 and self._ball.owner != 'none' and self.hitbox.colliderect(self._ball.hitbox):
            self.life = 0
            # get the ball's owner
            owner = self._ball.owner
            owner.add_powerUp(self.get_ItemForm(self._ball.owner))
            
        
    
class SpeedBallPowerUp(PowerUp):
    def __init__(self, posX, posY, ball, players):
        PowerUp.__init__(self, posX, posY, (0, 30, 232), ball, players)
    
    def _perform_action(self, owningPlayer = None):
        # the random bonus to be applied to one of the axes
        randomXBonus = random.randint(0, 3)
        randomYBonus = random.randint(0, 3)
        self._ball.velX *= (3 + randomXBonus)
        self._ball.velY *= (3 + randomYBonus)
    
    def _get_powerUpId(self):
        return 0
    
class OwnerSwitchPowerUp(PowerUp):
    def __init__(self, posX, posY, ball, players):
        PowerUp.__init__(self, posX, posY, (200, 170, 0), ball, players)
        
    def _perform_action(self, owningPlayer = None):
        # make the ball switch teams
        otherPlayer = next((player for index,player in enumerate(self._players) if player != self._ball.owner), None)
        # if there is another player, change the ball's owner to that
        if otherPlayer is not None:
            print(otherPlayer)
            self._ball.switch_owner(otherPlayer)
        
    def _get_powerUpId(self):
        return 1
    
class SwitchDirectionPowerUp(PowerUp):
    def __init__(self, posX, posY, ball, players):
        PowerUp.__init__(self, posX, posY, (230, 0, 20), ball, players)
        
    def _perform_action(self, owningPlayer = None):
        # get the ball's initial velocity
        ballVelocity = self._ball.get_velocity()
        self._ball.set_velocity(-ballVelocity['x'], -ballVelocity['y'])
        
    def _get_powerUpId(self):
        return 2
    
class BallSizePowerUp(PowerUp):
    def __init__(self, posX, posY, ball, players):
        PowerUp.__init__(self, posX, posY, (0, 200, 50), ball, players)
        
    def _perform_action(self, owningPlayer = None):
        # get the ball's initial velocity
        ballSize = random.randint(1, 80)
        self._ball.set_size(ballSize, ballSize)
        
    def _get_powerUpId(self):
        return 3
    
class RandomizeLocationPowerUp(PowerUp):
    def __init__(self, posX, posY, ball, players):
        PowerUp.__init__(self, posX, posY, (200, 100, 0), ball, players)
        
    def _perform_action(self, owningPlayer = None):
        # get the player that did not use the power up
        if owningPlayer is not None:
            otherPlayer = next((player for index,player in enumerate(self._players) if player != owningPlayer), None)
            # randomize the y position of the other player
            otherPlayer.set_location(otherPlayer.posX, random.randint(0, (500 - otherPlayer.height)))
            
    def _get_powerUpId(self):
        return 4
            
            
class BounceBallPowerUp(PowerUp):
    def __init__(self, posX, posY, ball, players):
        PowerUp.__init__(self, posX, posY, (100, 0, 200), ball, players)
        
    def _perform_action(self, owningPlayer = None):
        bounceAmount = random.randint(1, 3)
        # bounce the ball
        self._ball.bounce('y', bounceAmount)
        
    def _get_powerUpId(self):
        return 5