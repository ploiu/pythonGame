class ObjectManager:
    """class that keeps track of all the objects in the world, and updates those objects when necessary"""
    def __init__(self):
        # our list of entities
        self.entities = []
        # our list of non-entity objects
        self.worldObjects = []
        
    def add_entity(self, entityToAdd):
        self.entities.append(entityToAdd)
        
    def get_entities(self):
        return self.entities
        
    def add_worldObject(self, worldObjectToAdd):
        self.worldObjects.append(worldObjectToAdd)
        
    def get_worldObjects(self):
        return self.worldObjects
    
    def update_entities(self):
        """calls the update function on all of our entities"""
        for entity in self.entities:
            entity.update()
            
    def update_worldObjects(self):
        pass # TODO
    
    def update_all(self):
        """updates all the entities and world objects registered to this manager"""
        self.update_entities()
        self.update_worldObjects()