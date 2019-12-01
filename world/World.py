import world
class World:
    """Class that manages the rendering and state of all object in the game"""
    def __init__(self, screen):
        self.__manager = world.ObjectManager()
        self.__renderer = world.ObjectRenderer(screen)
        
    def get_allObjects(self):
        """gets all objects in the world, regardless of type"""
        return self.__manager.get_entities() + self.__manager.get_worldObjects()
    
    def add_entity(self, entityToAdd):
        """adds an entity to the world and registers it with the object manager"""
        self.__manager.add_entity(entityToAdd)

    def add_object(self, objectToAdd):
        """adds an object to the world and registers it with the object manager"""
        self.__manager.add_worldObject(objectToAdd)

    def tick(self):
        """performs 1 world 'tick', and updates all entities and objects in the world"""
        # update the entities in the world
        self.__manager.update_all()
            
    def render(self):
        """call our renderer to render all objects and entities in the world"""
        self.__renderer.renderWorldObjects(self.get_allObjects())
        
    def create_player(self, color, posX = 0, posY = 0):
        """creates a player, registers it to the world, and returns it"""
        player =  world.Player(color, posX, posY)
        # register the player
        self.add_entity(player)
        return player