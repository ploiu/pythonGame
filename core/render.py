import pygame, world

class RenderManager:
    def __init__(self):
        # the screen to render everything on
        self.screen = self.__setup_screen()
        # the font to display text in
        self.font = self.__setup_font()
        
    def __setup_screen(self):
        # the screen to return to the caller
        screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF)
        return screen
    
    def __setup_font(self):
        # init the font module
        pygame.font.init()
        gameFont = pygame.font.SysFont('Droid Mono', 30)
        return gameFont
    
    def __renderWorldObject(self, worldObject):
        """draw the worldObject's rect in its color"""
        pygame.draw.rect(self.screen, worldObject.get_color(), worldObject.get_hitBox())
        
    def __renderInWorldPowerUp(self, powerUp):
        pygame.draw.circle(self.screen, powerUp.color, powerUp.hitbox.center, powerUp.hitbox.width // 2)
        
    def renderWorldObjects(self, worldObjects):
        """ draws the world objects passed by delegating to the renderWorldObject method"""
        for worldObject in worldObjects:
            # the power ups render differently than other objects
            if issubclass(type(worldObject), world.PowerUp):
                self.__renderInWorldPowerUp(worldObject)
            else:
                self.__renderWorldObject(worldObject)
            
    def render(self, worldObjects, playerScores, playerPowerUps):
        # clear the screen to prepare for the next draw
        self.screen.fill((0, 0, 0))
        # render all the objects in the world
        self.renderWorldObjects(worldObjects)
        # render the score for the game
        self.render_gameScore(playerScores[0], playerScores[1])
        # render the player power ups
        self.render_powerUpStocks(playerPowerUps[0], playerPowerUps[1])
        # flip the screen to update everything
        pygame.display.flip()
        
    def render_gameScore(self, player1Score, player2Score):
        # render the font, then display it on our screen
        fontSurface = self.font.render("{} | {}".format(player1Score, player2Score), False, (255, 255, 255))
        self.screen.blit(fontSurface, (220, 30))
        
    def render_powerUpStocks(self, player1PowerUps, player2PowerUps):
        self._render_playerPowerUps(player1PowerUps, 100, 470)
        self._render_playerPowerUps(player2PowerUps, 400, 470)
        
    def _render_playerPowerUps(self, powerUps, startX, startY):
        """renders the list of powerUps on the screen in a row, each powerUp rendered in its color"""
        # diameter to render each powerUp
        powerUpRadius = 3
        for index,powerUp in enumerate(powerUps):
            pygame.draw.circle(self.screen, powerUp['color'], (startX + powerUpRadius * index, startY), powerUpRadius)
