import pygame
import pytmx

# game settings


WIDTH = 1280  # 2/3 of 1920
HEIGHT = 720  # 2/3 of 1080
TITLE = "ReRollRPG 2"

TILESIZE = 32
ORIGINAL_TILESIZE = 16
SCALE_FACTOR = TILESIZE / ORIGINAL_TILESIZE

FPS = 60

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# player
PLAYER_SPEED = 3

# camera
CAMERA_SMOOTHING = 0.1
