from settings import *
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)

        # load animation frames
        self.idle_frames = []
        self.load_animations()

        # surface
        self.current_frame = random.randint(0, len(self.idle_frames) - 1)
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)

        # animation
        self.animation_speed = 0.15

    def load_animations(self):
        sprite_path = 'assets/sprites/enemy'

        # idle animation
        for i in range(4):
            img = pygame.image.load(f"{sprite_path}/idle{i}.png")
            img = pygame.transform.scale_by(img, 2)
            self.idle_frames.append(img)

    def update(self):
        self.animate()

    def animate(self):
        frames = self.idle_frames

        # advance frame
        self.current_frame += self.animation_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0

        # update image
        img = frames[int(self.current_frame)]
        self.image = img.convert_alpha()
