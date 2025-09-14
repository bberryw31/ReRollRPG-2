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


class InteractionManager:
    def __init__(self):
        # interaction states
        self.nearby_enemy = None
        self.combat_system = CombatSystem()
        self.game = None  # will be set by main game class

        # UI
        self.font = pygame.font.Font(None, 24)

        # Proximity detection
        self.interaction_range = INTERACTION_RANGE

    @property
    def in_combat(self):
        return self.combat_system.in_combat

    def update(self, player, enemies):
        if self.in_combat:
            return

        for enemy in enemies:
            # calculate distance between player and enemy
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)

            # find enemy within interaction range
            if distance <= self.interaction_range:
                self.nearby_enemy = enemy
                break
        else:
            self.nearby_enemy = None

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
        if not self.nearby_enemy:
            return

        # enemy position
        enemy_world_pos = (self.nearby_enemy.rect.centerx, self.nearby_enemy.rect.top)
        enemy_screen_pos = camera.apply_pos(enemy_world_pos)

        # add game area offset
        enemy_screen_x = enemy_screen_pos[0]
        enemy_screen_y = enemy_screen_pos[1]

        # only draw if enemy is visible on screen
        screen_area = pygame.Rect(0, 0, WIDTH, HEIGHT)
        if screen_area.collidepoint(enemy_screen_x, enemy_screen_y):
            # draw prompt text
            prompt_text = "Attack"
            text_surface = self.font.render(prompt_text, True, (255, 50, 50))
            text_rect = text_surface.get_rect()
            text_rect.centerx = enemy_screen_x
            text_rect.bottom = enemy_screen_y - 5

            screen.blit(text_surface, text_rect)
