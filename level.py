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
        for x, y, image in self.tmx_data.get_layer_by_name('Ground').tiles():
            self.image.blit(pygame.transform.scale_by(image, SCALE_FACTOR), (x * TILESIZE, y * TILESIZE))

    def load_objects(self):
        # load objects from tmx
        for obj in self.tmx_data.get_layer_by_name('Wall'):
            self.walls.append(pygame.Rect(obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR, obj.width * SCALE_FACTOR,
                                          obj.height * SCALE_FACTOR))
        for obj in self.tmx_data.get_layer_by_name('Player'):
            self.spawn_point = (obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR)
        for obj in self.tmx_data.get_layer_by_name('Enemy'):
            self.enemy_spawns.append((obj.x * SCALE_FACTOR, obj.y * SCALE_FACTOR))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
