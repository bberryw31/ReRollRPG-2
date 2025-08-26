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
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (TILESIZE, TILESIZE))
                        self.image.blit(tile, (x * TILESIZE, y * TILESIZE))

    def load_objects(self):
        # load objects from tmx
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    x = obj.x * (TILESIZE / ORIGINAL_TILESIZE)
                    y = obj.y * (TILESIZE / ORIGINAL_TILESIZE)
                    w = obj.width * (TILESIZE / ORIGINAL_TILESIZE)
                    h = obj.height * (TILESIZE / ORIGINAL_TILESIZE)

                    if obj.name == 'walls':
                        self.walls.append(pygame.Rect(x, y, w, h))
                    elif obj.name == 'player':
                        self.spawn_point = pygame.math.Vector2(x, y)
                    elif obj.name == 'enemies':
                        self.enemy_spawns.append((x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)