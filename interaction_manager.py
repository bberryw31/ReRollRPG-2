import pygame
import math
from enum import Enum


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

    def draw(self, screen):
        if not self.nearby_enemy:
            return

        # enemy position
        enemy_x = self.nearby_enemy.rect.centerx
        enemy_y = self.nearby_enemy.rect.top

        # prompt text
        prompt_text = "Press E to attack"
        text_surface = self.font.render(prompt_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = enemy_x
        text_rect.bottom = enemy_y - 10

        # prompt background
        bg_rect = text_rect.copy()
        bg_rect.inflate(10, 4)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)

        screen.blit(text_surface, text_rect)
