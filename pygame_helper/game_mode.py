from abc import ABC, abstractmethod
from enum import Enum, unique, auto


class GameMode(ABC):

    def __init__(self, game):
        super().__init__()
        self.game = game

    @abstractmethod
    def process_input(self):
        pass
    
    @abstractmethod
    def update_game_state(self):
        pass

    @abstractmethod
    def render(self, window):
        pass


@unique
class GameModeType(Enum):
    PLAY = auto()
    OVERLAY = auto()