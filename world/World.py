import world
class World:
    """Class that manages the state of all objects in the game"""
    def __init__(self):
        self._manager = world.ObjectManager()
        self._playerManager = world.PlayerManager(self._manager)
        # TODO add a manager for this since there may be multiple balls in the future
        self.__ball = None
        
    def get_allObjects(self):
        """gets all objects in the world, regardless of type"""
        return self._manager.get_entities() + self._manager.get_worldObjects()
    
    def add_entity(self, entityToAdd):
        """adds an entity to the world and registers it with the object manager"""
        self._manager.add_entity(entityToAdd)

    def add_object(self, objectToAdd):
        """adds an object to the world and registers it with the object manager"""
        self._manager.add_worldObject(objectToAdd)

    def tick(self):
        """performs 1 world 'tick', and updates all entities and objects in the world"""
        # update the entities in the world
        self._manager.update_all()
        
    def add_player(self, gamepad):
        self._playerManager.addPlayerToGame(gamepad)
        
    def get_players(self):
        return self._playerManager.get_players()
    
    def get_playerScores(self):
        players = self.get_players()
        return [players[0].score, players[1].score]
    
    def set_ball(self, ball):
        self.__ball = ball
        
    def get_ball(self):
        return self.__ball