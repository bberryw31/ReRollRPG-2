import math
from enum import Enum
from camera import Camera
from settings import *


class InteractionType(Enum):
    FIGHT = "fight"
    DRINK = "drink"
    OPEN = "open"
    CLAIM = "claim"


class InteractionManager:
    def __init__(self):
        # interaction states
        self.nearby_enemy = None
        self.in_combat = False
        self.combat_target = None

        # UI
        self.font = pygame.font.Font(None, 24)

        # Proximity detection
        self.interaction_range = 50

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

    def handle_input(self, event):
        if self.in_combat:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.nearby_enemy:
                self.start_combat(self.nearby_enemy)

    def start_combat(self, enemy):
        print(f"Starting combat with enemy!")
        self.in_combat = True
        self.combat_target = enemy

        # combat logic
        self.end_combat()

    def end_combat(self):
        # end combat
        print("Combat ended!")
        self.in_combat = False
        self.combat_target = None

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
