from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)

        # load animation frames
        self.idle_frames = []
        self.run_frames = []
        self.load_animations()

        # surface
        self.current_frame = 0
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=position)

        # movement
        self.position = pygame.math.Vector2(position)
        self.direction = pygame.math.Vector2()

        # animation
        self.animation_speed = 0.15
        self.is_moving = False
        self.facing = "right"

    def load_animations(self):
        sprite_path = 'assets/sprites/character'

        # idle animation
        for i in range(4):
            img = pygame.image.load(f"{sprite_path}/idle{i}.png")
            img = pygame.transform.scale_by(img, 2)
            self.idle_frames.append(img.convert_alpha())

        # run animation
        for i in range(4):
            img = pygame.image.load(f"{sprite_path}/run{i}.png")
            img = pygame.transform.scale_by(img, 2)
            self.run_frames.append(img.convert_alpha())

    def update(self):
        self.input()
        self.move()
        self.animate()

    def input(self):
        # keys pressed
        keys = pygame.key.get_pressed()

        # direction
        self.direction.x = (int(keys[pygame.K_d]) - int(keys[pygame.K_a]))
        self.direction.y = (int(keys[pygame.K_s]) - int(keys[pygame.K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction

        # check if moving
        self.is_moving = (self.direction.x != 0 or self.direction.y != 0)
        if self.direction.x > 0:
            self.facing = "right"
        elif self.direction.x < 0:
            self.facing = "left"

    def move(self):
        # store old position
        self.old_position = self.position.copy()

        # update player position
        self.position += self.direction * PLAYER_SPEED
        self.rect.center = self.position

    def revert_movement(self):
        # revert to previous position if needed
        self.position = self.old_position
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
        img = frames[int(self.current_frame)]
        if self.facing == "left":
            img = pygame.transform.flip(img, True, False)
        self.image = img
