from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)

        # load animation frames
        self.idle_frames = []
        self.run_frames = []
        self.load_animations()

        # surface
        self.current_frame = 0
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # movement
        self.position = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2()

        # animation
        self.animation_speed = 0.15
        self.is_moving = False

    def load_animations(self):
        sprite_path = 'assets/sprites/character'

        # idle animation
        for i in range(4):
            img = pygame.image.load(f"{sprite_path}/idle{i}.png")
            img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
            self.idle_frames.append(img)

        # run animation
        for i in range(4):
            img = pygame.image.load(f"{sprite_path}/run{i}.png")
            img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
            self.run_frames.append(img)

    def update(self):
        self.input()
        self.move()
        self.animate()

    def input(self):
        # keys pressed
        keys = pygame.key.get_pressed()

        # direction
        self.direction.x = (int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) * PLAYER_SPEED
        self.direction.y = (int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) * PLAYER_SPEED
        self.direction = self.direction.normalize() if self.direction else self.direction

        # check if moving
        self.is_moving = (self.direction.x != 0 or self.direction.y != 0)

    def move(self):
        # update player position
        self.position += self.direction
        self.rect.center = self.position

    def animate(self):
        # choose animation
        if self.is_moving:
            frames = self.run_frames
        else:
            frames = self.idle_frames

        # advance frame
        self.current_frame += self.animation_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0

        # update image
        self.image = frames[int(self.current_frame)]