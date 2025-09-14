import math
from enum import Enum
from settings import *
from combat_system import CombatSystem
from game_states import GameState


class InteractionType(Enum):
    FIGHT = "fight"
    DRINK = "drink"
    OPEN = "open"
    CLAIM = "claim"


class InteractionArrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # load arrow animation frames
        self.frames = []
        self.load_frames()

        # animation properties
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        # reference to target enemy
        self.target_enemy = None

        # floating animation
        self.float_offset = 0
        self.float_speed = 0.1

    def load_frames(self):
        for i in range(5):  # 0-4.png
            img = pygame.image.load(f"assets/effects/arrow/{i}.png")
            img = pygame.transform.flip(img, False, True)
            img = pygame.transform.scale_by(img, 0.2)

            # Tint the arrow red
            red_tint = pygame.Surface(img.get_size(), pygame.SRCALPHA)
            red_tint.fill((30, 205, 205, 205))
            img.blit(red_tint, (0, 0), special_flags=pygame.BLEND_SUB)

            self.frames.append(img.convert_alpha())

    def set_target(self, enemy):
        self.target_enemy = enemy

    def update(self):
        if not self.target_enemy:
            return

        # animate arrow frames
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        self.image = self.frames[int(self.current_frame)]

        # floating animation
        self.float_offset += self.float_speed

        # position above enemy
        arrow_y = self.target_enemy.rect.centery * 2 - self.target_enemy.rect.bottom - 50
        self.rect.center = (self.target_enemy.rect.centerx + 14, arrow_y)


class InteractionManager:
    def __init__(self):
        # interaction states
        self.nearby_enemy = None
        self.combat_system = CombatSystem()
        self.game = None  # will be set by main game class

        # UI
        self.font = pygame.font.Font(None, 24)

        # proximity detection
        self.interaction_range = INTERACTION_RANGE

        # interaction arrow
        self.interaction_arrow = InteractionArrow()
        self.arrow_active = False

    @property
    def in_combat(self):
        return self.combat_system.in_combat

    def update(self, player, enemies):
        if self.in_combat:
            # hide arrow during combat
            self.arrow_active = False
            return

        nearby_enemy = None
        for enemy in enemies:
            # calculate distance between player and enemy
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)

            # find enemy within interaction range
            if distance <= self.interaction_range:
                nearby_enemy = enemy
                break

        # update arrow based on nearby enemy
        if nearby_enemy:
            if not self.arrow_active:
                # activate arrow for this enemy
                self.interaction_arrow.set_target(nearby_enemy)
                self.arrow_active = True
            elif self.interaction_arrow.target_enemy != nearby_enemy:
                # switch to new enemy
                self.interaction_arrow.set_target(nearby_enemy)

            # update arrow animation and position
            self.interaction_arrow.update()
        else:
            # no nearby enemy, deactivate arrow
            self.arrow_active = False

        self.nearby_enemy = nearby_enemy

    def handle_input(self, event, player):
        if self.in_combat:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.nearby_enemy:
                self.combat_system.start_combat(player, self.nearby_enemy)
                # switch to combat state and zoom camera
                if self.game:
                    self.game.current_state = GameState.COMBAT
                    self.game.camera.set_zoom(2.0)  # 2x zoom during combat

    def draw(self, screen, camera):
        if not self.arrow_active:
            return

        # draw the arrow
        arrow_screen_pos = camera.apply(self.interaction_arrow.rect)

        # only draw if arrow is visible on screen
        screen_area = pygame.Rect(0, 0, WIDTH, HEIGHT)
        if screen_area.colliderect(arrow_screen_pos):
            screen.blit(self.interaction_arrow.image, arrow_screen_pos)
