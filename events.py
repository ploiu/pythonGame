import pygame

class EventHandler:
    def __init__(self, gamepads, scoreManager):
        # our list of gamepads to set the events on
        self._gamepads = gamepads
        # the event type for something being scored
        self.__SCORE_EVENT = 64
        # init our score manager
        self.__scoreManager = scoreManager
        
    def handle_events(self):
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
            elif event.type == pygame.USEREVENT and event.custom_type == self.__SCORE_EVENT:
                self.__scoreManager.score(event.ball)
        
        # return if the game should continue running
        return hasQuitEvent
    
    def __handle_gamePadEvent(self, event):
        """handles the input event for a gamepad"""
        # get the gamepad associated with the event
        gamepadNumber = event.joy
        gamepad = self._gamepads[gamepadNumber]
        if event.type == pygame.JOYBUTTONDOWN:
            # dispatch the event associated with that button
            gamepad.press_button(event.button)
        elif event.type == pygame.JOYBUTTONUP:
            # call the release function for that button
            gamepad.release_button(event.button)
        elif event.type == pygame.JOYAXISMOTION:
            # call the directional button press on the gamepad
            gamepad.press_directionalButton(event.axis, event.value)
        