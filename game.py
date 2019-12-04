import pygame, world, controllers, traceback, time

class Game:
    """the base class for the game, handles the initialization and main loop of the game"""
    def __init__(self):
        # set the components to be nothing for now (will be a dict containing our components for the game)
        self.components = None
        # define the screen as nothing for now
        self.screen = None
        # world for this game that manages all of our world objects
        self.world = None
        
    def __pre_init(self):
        """initializes all non-graphical components of the game, including gamepads and pygame itself. Must be called before init"""
        # start pygame up
        pygame.init()
        # initialize the components
        self.components = {}
        # for each joystick, create a controller from it and add it to our components
        gamepads = [controllers.Controller(joystickNumber) for joystickNumber in range(pygame.joystick.get_count())]
        # add the gamepads to our components
        self.components['gamepads'] = gamepads
        
        
    def __init(self):
        """initializes the graphical component of the game as well as the game world"""
        self.screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF)
        # fill the screen with black
        self.screen.fill((0, 0, 0))
        # initialize the world for the game
        self.world = world.World(self.screen)
        
    def __post_init(self):
        """performs any post-initialization tasks, such as checking to make sure all components are loaded properly. must be called after __init"""
        # assert that our components and screen are loaded
        assert (self.components is not None), 'components failed to load'
        assert (self.screen is not None), 'screen failed to load'
        # assert that the game world loaded properly
        assert (self.world is not None), 'game world failed to initialize'
        
    def start_game(self):
        """runs the initialization methods and starts the game loop"""
        # run the pre-initialization
        self.__pre_init()
        # run the main initialization
        self.__init()
        # check that everything initialized properly
        try:
            self.__post_init()
            print("game started") 
        except AssertionError as error:
            print("game failed to start, error: \n")
            traceback.print_exc()
            # stop pygame and close python
            self.__quit_game()
            
        # add the players
        self.players = self.__addPlayersForEachGamePad(self.components['gamepads'])
        # add the ball
        self.world.add_entity(world.Ball(self.players))
        # start the game's main loop
        self.__start_gameLoop()
            
    def __quit_game(self):
        """stops pygame and closes python"""
        pygame.quit()
        quit()
    
    def __start_gameLoop(self):
        """starts the loop that calls all the game's functions"""
        # the target fps count we want is related to how many times we update the display in a second
        loopRate = 1 / 32
        # the variable that controls if the loop should keep going
        isRunning = True
        while isRunning:
            # handle all events before doing anything else
            isRunning = not self.__handle_events()
            # update the entities and render them
            self.world.tick()
            # clear the screen to prepare for the next draw
            self.screen.fill((0, 0, 0))
            self.world.render()
            # update the display
            pygame.display.flip()
            # sleep for a period of time determined by our loop rate
            time.sleep(loopRate)
        # quit the game
        self.__quit_game()
            
    def __handle_events(self):
        """handles all of the events sent by pygame, and returns a bool corresponding to if QUIT is one of the event types"""
        # if we had a quit event
        hasQuitEvent = False
        # for each event, handle it appropriately
        for event in pygame.event.get():
            # check if it's a quit event
            if event.type == pygame.QUIT:
                hasQuitEvent = True
            elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP or event.type == pygame.JOYAXISMOTION:
                self.__handle_gamePadEvent(event)
        
        # return if the game should continue running
        return hasQuitEvent
    
    def __handle_gamePadEvent(self, event):
        """handles the input event for a gamepad"""
        # get the gamepad associated with the event
        gamepadNumber = event.joy
        gamepad = self.components['gamepads'][gamepadNumber]
        if event.type == pygame.JOYBUTTONDOWN:
            # dispatch the event associated with that button
            gamepad.press_button(event.button)
        elif event.type == pygame.JOYBUTTONUP:
            # call the release function for that button
            gamepad.release_button(event.button)
        elif event.type == pygame.JOYAXISMOTION:
            # call the directional button press on the gamepad
            gamepad.press_directionalButton(event.axis, event.value)
        
    def __addPlayerToGame(self, gamepad):
        """creates a player and binds the button inputs of the gamepad to actions the player can take"""
        # the player number, used to determine where to place the player
        playerNumber = gamepad.get_controllerNumber()
        player = self.world.create_player(playerNumber, posX = (20 if playerNumber == 0 else 480), posY = 200)
        # map the directional buttons to move the player
        gamepad.map_directionalButton(controllers.SNESAxes.VERTICAL, lambda: player.set_velocity(player.velX, player.get_speed()['y']), lambda: player.set_velocity(player.velX, -player.get_speed()['y']), lambda: player.set_velocity(player.velX, 0))
        gamepad.map_button(controllers.SNESButtons.A, pressCommand = lambda: print('A pressed'))
        return player
        
    def __addPlayersForEachGamePad(self, gamepads):
        # the list of players
        players = [self.__addPlayerToGame(gamepad) for gamepad in gamepads]
        return players