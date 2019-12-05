import pygame, world, controllers

class PlayerManager:
    def __init__(self, objectManager):
        # the list of players this manages
        self._players = []
        self._objectManager = objectManager
    
    def addPlayerToGame(self, gamepad):
        """creates a player and binds the button inputs of the gamepad to actions the player can take"""
        # the player number, used to determine where to place the player
        playerNumber = gamepad.get_controllerNumber()
        player = self._create_player(playerNumber, posX = (20 if playerNumber == 0 else 470), posY = 200)
        # map the directional buttons to move the player
        gamepad.map_directionalButton(controllers.SNESAxes.VERTICAL, lambda: player.set_velocity(player.velX, player.get_speed()['y']), lambda: player.set_velocity(player.velX, -player.get_speed()['y']), lambda: player.set_velocity(player.velX, 0))
    
    def _create_player(self, playerNumber, posX = 0, posY = 0):
        """creates a player, registers it to the world, and returns it"""
        player =  world.Player(playerNumber, posX, posY)
        # register the player
        self._objectManager.add_entity(player)
        # add the player to our list to keep track of it
        self._players.append(player)
        return player
    
    def get_players(self):
        return self._players
    