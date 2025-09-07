from settings import *


class Camera:
    def __init__(self, width, height):
        # initiate camera
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

        # smooth camera movement
        self.target_x = 0
        self.target_y = 0

    def apply(self, entity_rect):
        # apply camera offset
        return entity_rect.move(-self.camera.x, -self.camera.y)

    def apply_pos(self, pos):
        # apply position
        return (pos[0] - self.camera.x, pos[1] - self.camera.y)

    def update(self, target):
        # update to follow target
        # center camera on target
        self.target_x = target.rect.centerx - GAME_AREA_WIDTH // 2
        self.target_y = target.rect.centery - GAME_AREA_HEIGHT // 2

        # smooth camera movement
        self.camera.x += (self.target_x - self.camera.x) * CAMERA_SMOOTHING
        self.camera.y += (self.target_y - self.camera.y) * CAMERA_SMOOTHING

        # keep camera within map bounds
        self.camera.x = max(0, self.camera.x)
        self.camera.y = max(0, self.camera.y)
        self.camera.x = min(self.width - GAME_AREA_WIDTH, self.camera.x)
        self.camera.y = min(self.height - GAME_AREA_HEIGHT, self.camera.y)

    def get_visible_area(self):
        # get the area currently visible by the camera
        return pygame.Rect(
            self.camera.x,
            self.camera.y,
            GAME_AREA_WIDTH,
            GAME_AREA_HEIGHT
        )
