import pygame


class UIManager:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)

        # heart images
        self.heart_full = pygame.image.load("assets/ui/ui_heart_full.png")
        self.heart_half = pygame.image.load("assets/ui/ui_heart_half.png")
        self.heart_empty = pygame.image.load("assets/ui/ui_heart_empty.png")

        # scale heart images
        heart_scale = 2
        self.heart_full = pygame.transform.scale_by(self.heart_full, heart_scale)
        self.heart_half = pygame.transform.scale_by(self.heart_half, heart_scale)
        self.heart_empty = pygame.transform.scale_by(self.heart_empty, heart_scale)

        self.heart_width = self.heart_full.get_width()
        self.heart_height = self.heart_full.get_height()

    def draw_player_ui(self, screen, player):
        # player ui top left
        ui_x = 10
        ui_y = 10

        # player icon
        player_icon = pygame.transform.scale_by(player.idle_frames[0], 2)
        screen.blit(player_icon, (ui_x, ui_y))

        # player hp
        hearts_start_y = ui_y + player_icon.get_height() + 5
        self.draw_hearts(screen, ui_x, hearts_start_y, player.HP, player.max_HP)

    def draw_enemy_ui(self, screen, enemy, enemy_hp, enemy_max_hp):
        # enemy ui top right
        ui_x = screen.get_width() - 10
        ui_y = 10

        # enemy icon
        enemy_icon = pygame.transform.scale_by(enemy.idle_frames[0], 2)
        icon_rect = enemy_icon.get_rect()
        icon_rect.topright = (ui_x, ui_y)
        screen.blit(enemy_icon, icon_rect)

        # enemy hp
        hearts_start_y = ui_y + enemy_icon.get_height() + 5
        hearts_x = icon_rect.right - (((enemy_max_hp + 1) // 2) * (self.heart_width + 2))
        self.draw_hearts(screen, hearts_x, hearts_start_y, enemy_hp, enemy_max_hp)

    def draw_hearts(self, screen, x, y, current_hp, max_hp):
        max_hearts = (max_hp + 1) // 2
        for i in range(max_hearts):
            heart_x = x + (i * (self.heart_width + 2))

            # choose heart image based on hp
            hp_for_this_heart = current_hp - (i * 2)

            if hp_for_this_heart >= 2:
                # full heart
                screen.blit(self.heart_full, (heart_x, y))
            elif hp_for_this_heart == 1:
                # half heart
                screen.blit(self.heart_half, (heart_x, y))
            else:
                # empty heart
                screen.blit(self.heart_empty, (heart_x, y))

    def draw_attack_prompt(self, screen, enemy_pos):
        # alternative prompt idea
        prompt_text = "Press E to attack"
        text_surface = self.font.render(prompt_text, True, (255, 255, 255))

        # prompt above enemy
        text_rect = text_surface.get_rect()
        text_rect.centerx = enemy_pos[0]
        text_rect.bottom = enemy_pos[1] - 10

        # Draw background for text
        bg_rect = text_rect.copy()
        bg_rect.inflate(10, 4)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)

        screen.blit(text_surface, text_rect)
