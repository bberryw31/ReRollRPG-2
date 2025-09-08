from settings import *


class SlashEffect(pygame.sprite.Sprite):
    def __init__(self, position, groups, target_direction):
        super().__init__(groups)

        # load slash animation frames
        self.frames = []
        self.load_frames()

        # animation state
        self.current_frame = 0
        self.animation_speed = 0.3  # faster animation

        # position the slash between attacker and target
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)

        # flip based on direction to target
        if target_direction.x < 0:
            for i in range(len(self.frames)):
                self.frames[i] = pygame.transform.flip(self.frames[i], True, False)

    def load_frames(self):
        # load slash animation frames from assets/effects/slash
        for i in range(4):
            img = pygame.image.load(f"assets/effects/slash{i}.png")
            img = pygame.transform.scale_by(img, 2)
            self.frames.append(img.convert_alpha())

    def update(self):
        # animate the slash
        self.current_frame += self.animation_speed

        # remove when animation completes
        if self.current_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.current_frame)]
