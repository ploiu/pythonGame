import pygame, world, controllers, traceback, time, events, render, componentManager, scoreManager

class Game:
    """the base class for the game, handles the initialization and main loop of the game"""
    def __init__(self):
        # set the components to be nothing for now (will be a dict containing our components for the game)
        self.components = None
        # world for this game that manages all of our world objects
        self.world = None
        # our event handler
        self._eventHandler = None
        # our render manager
        self._renderManager = None
        # our component manager
        self._componentManager = None
        
    def __pre_init(self):
        """initializes all non-graphical components of the game, including gamepads and pygame itself. Must be called before init"""
        # start pygame up
        pygame.init()
        # init our component manager and setup the controllers with it
        self._componentManager = componentManager.ComponentManager()
        self._componentManager.register_controllers(pygame.joystick.get_count())
        
    def __init(self):
        """initializes the graphical component of the game as well as the game world"""
        # initialize the handler for rendering everything
        self._renderManager = render.RenderManager()
        # initialize the world for the game
        self.world = world.World()
        # initialize the players and the ball
        self.__initPlayersAndBall()
        # init our event handler with the score handler and stuff
        controllers = self._componentManager.get_controllers()
        self._eventHandler = events.EventHandler(controllers, scoreManager.ScoreManager(self.world.get_players()))
        
    def __post_init(self):
        """performs any post-initialization tasks, such as checking to make sure all components are loaded properly. must be called after __init"""
        # assert that the game world loaded properly
        assert (self.world is not None), 'game world failed to initialize'
        assert (self._eventHandler is not None), 'event handler failed to initialize'
        assert (self._renderManager is not None), 'render manager failed to initialize'
        assert (self._componentManager is not None), 'component manager failed to initialize'
        
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
            
        # launch the ball
        self.world.get_ball().launch()
        # render everything for a first tick
        self.world.tick()
        # start the game's main loop after 3 seconds
        time.sleep(3)
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
            isRunning = not self._eventHandler.handle_events()
            # update the entities and render them
            self.world.tick()
            self._renderManager.render(self.world.get_allObjects(), self.world.get_playerScores())
            # sleep for a period of time determined by our loop rate
            time.sleep(loopRate)
        # quit the game
        self.__quit_game()
    
    def __initPlayersAndBall(self):
         # add the players
        self.world.add_player(self._componentManager.get_controller(0))
        self.world.add_player(self._componentManager.get_controller(1))
        # add the ball
        ball = world.Ball(self.world.get_players(), game = None)
        self.world.add_entity(ball)
        self.world.set_ball(ball)
  