import world, random

class PowerUpManager:
    def __init__(self, ball, players):
        """manager for powerUps. handles placeing powerUps in the world and choosing when and what type the powerUp is"""
        self._ball = ball
        self._players = players
        # time until next attempt to spanw a powerUp takes place
        self.__DEFAULT_POWERUP_TIMER = 20
        self._timeUntilNextPowerUp = self.__DEFAULT_POWERUP_TIMER
        # only 1 powerUp can exist in the world at a time
        self.powerUp = None
        self._powerUpMapping = {
                0: world.SpeedBallPowerUp,
                1: world.OwnerSwitchPowerUp,
                2: world.SwitchDirectionPowerUp,
                3: world.BallSizePowerUp,
                4: world.RandomizeLocationPowerUp,
                5: world.BounceBallPowerUp
            }
        """a dict containing powerUp IDs and the powerUp they''re associated with, used to instantiate the corresponding powerUp when it comes to place one in the world"""
        
    def _create_powerUp(self):
        """creates a random powerUp in the world at a random (but constrained) location"""
        # the max distance from the center that the powerUp can spawn from
        maxDistanceX = 30
        maxDistanceY = 100
        # the x spawn location
        spawnX = random.randint(-maxDistanceX, maxDistanceX)
        spawnY = random.randint(-maxDistanceY, maxDistanceY)
        # the powerUp id to spawn in TODO change when we get more powerUps
        powerUpType = random.randint(0, len(self._powerUpMapping) - 1)
        # the powerUp to spawn in
        powerUpToSpawn = self._powerUpMapping[powerUpType](250 + spawnX, 250 + spawnY, self._ball, self._players)
        self.powerUp = powerUpToSpawn
    
    def tick(self):
        """called periodically in the game loop, used to check for powerUp status and spawn in new powerUps / remove expired ones from the world"""
        # if there's already a powerUp, don't change the timer
        if self.powerUp is None:
            self._timeUntilNextPowerUp -= 1
            if self._timeUntilNextPowerUp <= 0:
                # reset the timer and attempt to spawn a powerUp
                self._timeUntilNextPowerUp = self.__DEFAULT_POWERUP_TIMER
                self._attempt_spawnPowerup()
        elif self.powerUp.life <= 0:
            # set our powerUp to be none
            self.powerUp = None
        else:
            self.powerUp.update()
            
    def _attempt_spawnPowerup(self):
        # if we don't have a powerUp, attempt to generate one
        if self.powerUp is None and random.randint(0, 10) == 1:
            # create a powerUp
            self._create_powerUp()