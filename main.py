from settings import *
from level import Level
from sprites.player import Player
from sprites.enemy import Enemy
from interaction_manager import InteractionManager, InteractionType
from ui_manager import UIManager
from character_generator import CharacterGenerator, CharacterPreviewPlayer
from game_states import GameState


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # instance variables
        self.interaction_manager = InteractionManager()
        self.ui_manager = UIManager()

        # state management
        self.current_state = GameState.TITLE

        # character generation
        self.character_generator = CharacterGenerator()
        self.current_character_data = None
        self.tutorial_level = None
        self.preview_sprites = None
        self.preview_player = None

        # silkscreen fonts
        self.title_font = pygame.font.Font("assets/fonts/Silkscreen/slkscrb.ttf", 72)
        self.medium_font = pygame.font.Font("assets/fonts/Silkscreen/slkscr.ttf", 36)
        self.small_font = pygame.font.Font("assets/fonts/Silkscreen/slkscr.ttf", 24)

    def new_game(self):
        # initialize a new game
        self.level = Level('assets/maps/lv1.tmx', self)

        # sprites
        self.all_sprites = pygame.sprite.Group()

        # player
        self.player = Player(self.level.spawn_point, self.all_sprites)

        # enemy
        self.enemies = pygame.sprite.Group()
        for spawn in self.level.enemy_spawns:
            Enemy(spawn, [self.all_sprites, self.enemies])

    def run(self):
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                # handle events based on current state
                if self.current_state == GameState.TITLE:
                    self.handle_title_events(event)
                # elif self.current_state == GameState.CHARACTER_GENERATION:
                #     self.handle_character_events(event)

            # update based on current state
            if self.current_state == GameState.TITLE:
                self.draw_title()
            # elif self.current_state == GameState.CHARACTER_GENERATION:
            #     self.update_character_generation()
            #     self.draw_character_generation()

            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_title_events(self, event):
        # title screen key input
        if event.type == pygame.KEYDOWN:
            self.current_state = GameState.CHARACTER_GENERATION
            # self.init_character_generation()

    def draw_title(self):
        # draw title screen
        self.screen.fill(BLACK)

        # title
        title = self.title_font.render("ReRollRPG 2", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(title, title_rect)

        # instructions
        instruction = self.medium_font.render("Press any key to start", True, (200, 200, 200))
        inst_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.screen.blit(instruction, inst_rect)

    def events(self):
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # interaction key input
            self.interaction_manager.handle_input(event)

    def update(self):
        if not self.interaction_manager.in_combat:
            # update game
            self.all_sprites.update()

            # handle collisions
            self.handle_collisions()

            # check nearby enemies
            self.interaction_manager.update(self.player, self.enemies)

        # game fps
        self.clock.tick(FPS)

    def handle_collisions(self):
        # check collisions
        self.check_player_wall_collision()
        self.check_player_enemy_collision()

    def check_player_wall_collision(self):
        # check player collision with wall
        for wall in self.level.walls:
            if self.player.rect.colliderect(wall):
                self.resolve_collision(wall)
                break

    def check_player_enemy_collision(self):
        # find collided enemy sprites
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)

        if hit_enemies:
            for enemy in hit_enemies:
                self.resolve_collision(enemy.rect)

                break

    def resolve_collision(self, target):
        # calculate overlaps on each side
        overlap_left = self.player.rect.right - target.left
        overlap_right = target.right - self.player.rect.left
        overlap_top = self.player.rect.bottom - target.top
        overlap_bottom = target.bottom - self.player.rect.top

        # find minimum overlap (shortest distance to push)
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left:
            # push left
            self.player.rect.right = target.left
        elif min_overlap == overlap_right:
            # push right
            self.player.rect.left = target.right
        elif min_overlap == overlap_top:
            # push up
            self.player.rect.bottom = target.top
        else:
            # push down
            self.player.rect.top = target.bottom

        # Update position to match rect
        self.player.position = pygame.math.Vector2(self.player.rect.center)

    def draw(self):
        # draw game
        self.screen.fill(BLACK)

        # draw level
        self.level.draw(self.screen)

        # draw sprites
        self.all_sprites.draw(self.screen)

        # draw UI
        self.ui_manager.draw_player_ui(self.screen, self.player)

        if self.interaction_manager.nearby_enemy:
            # draw interaction popup
            self.interaction_manager.draw(self.screen)

            nearby_enemy = self.interaction_manager.nearby_enemy
            self.ui_manager.draw_enemy_ui(self.screen, nearby_enemy, nearby_enemy.HP, nearby_enemy.max_HP)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
