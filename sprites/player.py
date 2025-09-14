from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, character_data):
        super().__init__(groups)

        # character data
        self.character_data = character_data
        self.class_info = character_data["class"]
        self.stats = character_data["stats"]
        self.HP = character_data["HP"]
        self.max_HP = character_data["max_HP"]
        self.sprite_path = character_data["class"]["sprite_path"]

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

        # damage blink effect
        self.blink_timer = 0
        self.blink_duration = 15  # frames to blink
        self.is_blinking = False

    def take_damage(self, damage):
        # take damage and return if alive
        self.HP = max(0, self.HP - damage)
        self.start_blink()
        return self.HP > 0

    def heal(self, amount):
        # heal
        self.HP = min(self.max_HP, self.HP + amount)

    def load_animations(self):
        sprite_path = f'assets/sprites/player/{self.sprite_path}'

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

        for i in range(len(self.idle_frames)):
            self.idle_frames[i] = self.trim_transparent_borders(self.idle_frames[i])
        for i in range(len(self.run_frames)):
            self.run_frames[i] = self.trim_transparent_borders(self.run_frames[i])

    def trim_transparent_borders(self, surface):
        # remove transparent borders from surface
        mask = pygame.mask.from_surface(surface)
        if mask.get_bounding_rects():
            bounds = mask.get_bounding_rects()[0]
            return surface.subsurface(bounds).copy()
        return surface

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
        # update player position
        self.position += self.direction * PLAYER_SPEED
        self.rect.center = self.position

    def animate(self):
        # update blink effect
        self.update_blink()

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

        # apply blink effect
        if self.is_blinking and (self.blink_timer // 5) % 2:  # blink every 5 frames
            # create white tinted version
            white_tint = pygame.Surface(img.get_size(), pygame.SRCALPHA)
            white_tint.fill((255, 255, 255, 180))
            img = img.copy()
            img.blit(white_tint, (0, 0), special_flags=pygame.BLEND_ADD)

        old_bottom = self.rect.bottom
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.centerx = self.position.x
        self.position = pygame.math.Vector2(self.rect.center)

    def start_blink(self):
        # start the damage blink effect
        self.is_blinking = True
        self.blink_timer = 0

    def update_blink(self):
        # handle blink timing
        if self.is_blinking:
            self.blink_timer += 1
            if self.blink_timer >= self.blink_duration:
                self.is_blinking = False
                self.blink_timer = 0
