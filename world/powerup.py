import world, enum

class PowerUp(world.WorldObject):
    def __init__(self, posX, posY, color, ball, players):
        world.WorldObject.__init__(self, posX, posY, 12, 12, color)
        # needed during initialization time because we can't easily get it later
        self._ball = ball
        self._players = players
        # the amount of time the powerUp has to live
        self.life = 20
        
    def _perform_action(self):
        """function to be called when a player uses this powerUp"""
        pass
    
    def _get_powerUpId(self):
        """returns a numeric value representing the id of this power up"""
        return None
    
    def get_ItemForm(self):
        """returns a dict, with the key being the id of the powerUp, and the value being this powerUp''s action"""
        return {self._get_powerUpId(): (lambda: self._perform_action())}
    
    def update(self):
        world.WorldObject.update(self)
        # decrease the amount of time the powerUp has left
        self.life -= 1
        # if the powerUp has been hit by the ball and it's not dead, kill the powerUp and give it to the player
        if self.life > 0 and self.hitbox.colliderect(self._ball.hitbox):
            self.life = 0
            # get the ball's owner
            owner = self._ball.owner
        
    
class SpeedBallPowerUp(PowerUp):
    def __init__(self, posX, posY, ball, players):
        PowerUp.__init__(self, posX, posY, (0, 30, 232), ball, players)
    
    def _perform_action(self):
        self._ball.velX *= 2
        self._ball.velY *= 2
    
    def _get_powerUpId(self):
        return 0