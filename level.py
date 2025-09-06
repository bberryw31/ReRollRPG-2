import pygame.math

from settings import *


class Level:
    def __init__(self, filename, game):
        self.game = game

        # load map
        self.tmx_data = pytmx.load_pygame(filename)
        self.width = self.tmx_data.width * TILESIZE
        self.height = self.tmx_data.height * TILESIZE

        # surface
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        # game area offset
        self.rect.x = GAME_OFFSET_X
        self.rect.y = GAME_OFFSET_Y

        # render map
        self.render_map()

        # object positions
        self.walls = []
        self.spawn_point = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)  # Default center
        self.enemy_spawns = []

        # load objects
        self.load_objects()

    def render_map(self):
        # render map from tmx
        print("Rendering map")
        for x, y, image in self.tmx_data.get_layer_by_name('Ground').tiles():
            self.image.blit(pygame.transform.scale_by(image, SCALE_FACTOR), (x * TILESIZE, y * TILESIZE))

    def load_objects(self):
        # load objects from tmx
        print("Loading walls")
        for obj in self.tmx_data.get_layer_by_name('Wall'):
            self.walls.append(
                pygame.Rect(obj.x * SCALE_FACTOR + GAME_OFFSET_X, obj.y * SCALE_FACTOR + GAME_OFFSET_Y,
                            obj.width * SCALE_FACTOR,
                            obj.height * SCALE_FACTOR))
        print("Loading player")
        for obj in self.tmx_data.get_layer_by_name('Player'):
            self.spawn_point = (obj.x * SCALE_FACTOR + GAME_OFFSET_X, obj.y * SCALE_FACTOR + GAME_OFFSET_Y)
        print("Loading enemy")
        for obj in self.tmx_data.get_layer_by_name('Enemy'):
            self.enemy_spawns.append((obj.x * SCALE_FACTOR + GAME_OFFSET_X, obj.y * SCALE_FACTOR + GAME_OFFSET_Y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
