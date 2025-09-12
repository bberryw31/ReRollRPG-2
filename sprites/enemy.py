from settings import *
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)

        # facing direction
        self.facing = "right"  # can be "left" or "right"
        self.original_facing = random.choice(["left", "right"])
        
        # load animation frames
        self.idle_frames = []
        self.idle_frames_left = []
        self.idle_frames_right = []
        self.load_animations()

        # surface
        self.current_frame = random.randint(0, len(self.idle_frames) - 1)
        self.facing = self.original_facing  # set initial facing
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
        
        # load base animations
        for i in range(4):
            img = pygame.image.load(f"{sprite_path}/idle{i}.png")
            img = pygame.transform.scale_by(img, 2)
            
            # store both normal and flipped versions
            right_img = img.convert_alpha()
            left_img = pygame.transform.flip(img, True, False).convert_alpha()
            
            self.idle_frames_right.append(right_img)
            self.idle_frames_left.append(left_img)

        # trim transparent borders for both directions
        for i in range(len(self.idle_frames_right)):
            self.idle_frames_right[i] = self.trim_transparent_borders(self.idle_frames_right[i])
            self.idle_frames_left[i] = self.trim_transparent_borders(self.idle_frames_left[i])
            
        # set idle_frames to the original facing direction
        self.idle_frames = self.idle_frames_right

    def trim_transparent_borders(self, surface):
        # remove transparent borders from surface
        mask = pygame.mask.from_surface(surface)
        if mask.get_bounding_rects():
            bounds = mask.get_bounding_rects()[0]
            return surface.subsurface(bounds).copy()
        return surface

    def update(self):
        self.animate()

    def face_target(self, target_pos):
        # make enemy face towards target position
        if target_pos[0] < self.rect.centerx:
            self.facing = "left"
            self.idle_frames = self.idle_frames_left
        else:
            self.facing = "right"
            self.idle_frames = self.idle_frames_right
            
    def animate(self):
        frames = self.idle_frames

        # advance frame
        self.current_frame += self.animation_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0

        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx

        # update image
        img = frames[int(self.current_frame)]
        self.image = img

        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.centerx = old_centerx
