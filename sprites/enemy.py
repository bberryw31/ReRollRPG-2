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

        # HP system
        self.max_HP = 10
        self.HP = self.max_HP

    def take_damage(self, damage):
        # take damage and return if alive
        self.HP = max(0, self.HP - damage)
        return self.HP > 0

    def load_animations(self):
        sprite_path = 'assets/sprites/enemy'
        flip = random.choice([True, False])
        # idle animation
        for i in range(4):
            img = pygame.image.load(f"{sprite_path}/idle{i}.png")
            if flip:
                img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale_by(img, 2)
            self.idle_frames.append(img.convert_alpha())

        for i in range(len(self.idle_frames)):
            self.idle_frames[i] = self.trim_transparent_borders(self.idle_frames[i])

    def trim_transparent_borders(self, surface):
        # remove transparent borders from surface
        mask = pygame.mask.from_surface(surface)
        if mask.get_bounding_rects():
            bounds = mask.get_bounding_rects()[0]
            return surface.subsurface(bounds).copy()
        return surface

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
        self.image = img
