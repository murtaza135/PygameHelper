class Error(Exception):
    """Base class for other exceptions
    
    Attributes:
        message -- explanation of the error
    """
    pass

class PygameInitError(Error):
    """Raised when pygame.display.init() has not been called whilst trying to access an attribute which requires pygame to be initialised"""

    def __init__(self):
        self.message = "Pygame has not been intialised yet. Please make sure pygame.display.init() has been called."
        super().__init__(self.message)

class DeleteError(Error):
    """Raised when someone tries to delete a class or instance attribute which is pivotal to the class"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)