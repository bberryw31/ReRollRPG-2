from settings import *
from enum import Enum


class GameState(Enum):
    TITLE = "title"
    CHARACTER_GENERATION = "character_generation"
    GAMEPLAY = "gameplay"
