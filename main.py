from settings import *
from level import Level
from sprites.player import Player
from sprites.enemy import Enemy
from interaction_manager import InteractionManager, InteractionType
from ui_manager import UIManager
from character_generator import CharacterGenerator, CharacterPreviewPlayer
from game_states import GameState
from camera import Camera


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
        self.preview_player = None

        # silkscreen fonts
        self.title_font = pygame.font.Font("assets/fonts/Silkscreen/slkscr.ttf", 72)
        self.medium_font = pygame.font.Font("assets/fonts/Silkscreen/slkscr.ttf", 36)
        self.small_font = pygame.font.Font("assets/fonts/Silkscreen/slkscr.ttf", 24)

    def run(self):
        # run the game
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                # handle events based on current state
                if self.current_state == GameState.TITLE:
                    self.handle_title_events(event)
                elif self.current_state == GameState.CHARACTER_GENERATION:
                    self.handle_character_events(event)
                elif self.current_state == GameState.GAMEPLAY:
                    self.handle_gameplay_events(event)

            # update based on current state
            if self.current_state == GameState.TITLE:
                self.draw_title()
            elif self.current_state == GameState.CHARACTER_GENERATION:
                self.update_character_generation()
                self.draw_character_generation()
            elif self.current_state == GameState.GAMEPLAY:
                self.update_gameplay()
                self.draw_gameplay()
            elif self.current_state == GameState.COMBAT:
                self.update_combat()
                self.draw_combat()

            pygame.display.flip()
            self.clock.tick(FPS)

    # =============== TITLE ===============
    def handle_title_events(self, event):
        # title screen key input
        if event.type == pygame.KEYDOWN:
            self.current_state = GameState.CHARACTER_GENERATION
            self.init_character_generation()

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

    # =============== CHARACTER GENERATION ===============
    def init_character_generation(self):
        # generate random character
        self.current_character_data = self.character_generator.generate_random_character()

        # tutorial map
        self.tutorial_level = Level('assets/maps/tutorial.tmx', self)

        # create preview character
        self.preview_player = CharacterPreviewPlayer(
            self.tutorial_level.spawn_point,
            self.current_character_data
        )

    def handle_character_events(self, event):
        # character generation input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # reroll character
                self.reroll_character()
            elif event.key == pygame.K_RETURN:
                # venture forth to gameplay
                self.current_state = GameState.GAMEPLAY
                self.init_gameplay()

    def reroll_character(self):
        # generate new character
        self.current_character_data = self.character_generator.generate_random_character()
        self.preview_player.update_character_data(self.current_character_data)

    def update_character_generation(self):
        # update character movement
        self.preview_player.update()

        # handle collisions with tutorial room walls
        for wall in self.tutorial_level.walls:
            if self.preview_player.rect.colliderect(wall):
                self.preview_player.revert_movement()
                break

    def draw_character_generation(self):
        # character generation screen
        self.screen.fill(BLACK)

        # tutorial room and character
        self.tutorial_level.draw(self.screen)
        self.preview_player.draw(self.screen)

        # draw character info
        self.draw_character_info()

    def draw_character_info(self):
        character = self.current_character_data

        # ui position
        ui_x = WIDTH / 2
        ui_y = HEIGHT / 3

        # class name
        class_text = self.medium_font.render(f"Class: {character['class']['name']}", True, WHITE)
        self.screen.blit(class_text, (ui_x, ui_y))

        # HP
        ui_y += 70
        hp_text = self.small_font.render(f"HP: {character['HP']}", True, WHITE)
        self.screen.blit(hp_text, (ui_x, ui_y))

        # stats
        ui_y += 30
        stats = character['stats']
        self.screen.blit(self.small_font.render(f"STR: {stats['str']}", True, WHITE), (ui_x, ui_y))
        self.screen.blit(self.small_font.render(f"DEX: {stats['dex']}", True, WHITE), (ui_x + 150, ui_y))
        self.screen.blit(self.small_font.render(f"INT: {stats['int']}", True, WHITE), (ui_x, ui_y + 30))
        self.screen.blit(self.small_font.render(f"LUC: {stats['luc']}", True, WHITE), (ui_x + 150, ui_y + 30))

        # control text
        ui_x = 370
        ui_y += 150
        reroll_text = self.medium_font.render(f"   R        Reroll Character", True, WHITE)
        self.screen.blit(reroll_text, (ui_x, ui_y))
        ui_y += 50
        start_text = self.medium_font.render(f"ENTER       Venture Forth!", True, WHITE)
        self.screen.blit(start_text, (ui_x, ui_y))

    # =============== GAME ===============
    def init_gameplay(self):
        # initialize main gameplay with selected character
        # load main game level
        self.level = Level('assets/maps/level1.tmx', self)

        # initiate camera
        self.camera = Camera(self.level.width, self.level.height)

        # initialize game systems
        self.interaction_manager = InteractionManager()
        self.interaction_manager.game = self  # set reference for state changes

        # all sprites
        self.all_sprites = pygame.sprite.Group()

        # player
        self.player = Player(self.level.spawn_point, self.all_sprites, self.current_character_data)

        # enemies
        self.enemies = pygame.sprite.Group()
        for spawn in self.level.enemy_spawns:
            Enemy(spawn, [self.all_sprites, self.enemies])

    def handle_gameplay_events(self, event):
        # handle gameplay events
        self.interaction_manager.handle_input(event, self.player)

    def update_gameplay(self):
        if not self.interaction_manager.in_combat:
            # update sprites
            self.all_sprites.update()

            # handle collisions
            self.handle_collisions()

            # update camera to follow player
            self.camera.update(self.player)

            # check nearby enemies
            self.interaction_manager.update(self.player, self.enemies)

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

    def draw_gameplay(self):
        # draw game
        self.screen.fill(BLACK)

        # draw level
        self.level.draw(self.screen, self.camera)

        # draw sprites
        for sprite in self.all_sprites:
            sprite_rect = self.camera.apply(sprite.rect)
            screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            # only draw if sprite is visible on screen
            if sprite_rect.colliderect(screen_rect):
                self.screen.blit(sprite.image, sprite_rect)

        # draw UI
        self.ui_manager.draw_player_ui(self.screen, self.player)

        if self.interaction_manager.nearby_enemy:
            # draw interaction popup
            self.interaction_manager.draw(self.screen, self.camera)

            nearby_enemy = self.interaction_manager.nearby_enemy
            self.ui_manager.draw_enemy_ui(self.screen, nearby_enemy, nearby_enemy.HP, nearby_enemy.max_HP)

    # =============== COMBAT ===============
    def update_combat(self):
        # update combat system
        self.interaction_manager.combat_system.update()

        # update sprite animations
        for sprite in self.all_sprites:
            sprite.animate()

        # update camera during combat (maintain zoom focus on player)
        self.camera.update(self.player)

        # check if combat ended
        if not self.interaction_manager.in_combat:
            # start zoom out transition but stay in combat state until zoom completes
            self.camera.set_zoom(1.0)
            # only switch to gameplay when zoom is close to 1.0
            if abs(self.camera.get_zoom() - 1.0) < 0.1:
                self.current_state = GameState.GAMEPLAY

    def draw_combat(self):
        # create temporary surface for scaling
        zoom = self.camera.get_zoom()

        if zoom == 1.0:
            # no zoom - draw directly to screen  
            render_surface = self.screen
        else:
            # create smaller surface to scale up
            base_size = (int(WIDTH / zoom), int(HEIGHT / zoom))
            render_surface = pygame.Surface(base_size, pygame.SRCALPHA)

            # adjust camera for smaller render area
            original_camera_pos = (self.camera.camera.x, self.camera.camera.y)
            zoom_offset_x = (WIDTH - base_size[0]) // 2
            zoom_offset_y = (HEIGHT - base_size[1]) // 2
            self.camera.camera.x += zoom_offset_x
            self.camera.camera.y += zoom_offset_y

        # draw everything to render surface
        render_surface.fill(BLACK)

        # draw level
        self.level.draw(render_surface, self.camera)

        # draw sprites
        for sprite in self.all_sprites:
            # only draw if sprite is visible
            if hasattr(sprite, 'visible') and not sprite.visible:
                continue

            sprite_rect = self.camera.apply(sprite.rect)
            render_rect = pygame.Rect(0, 0, render_surface.get_width(), render_surface.get_height())
            if sprite_rect.colliderect(render_rect):
                render_surface.blit(sprite.image, sprite_rect)

        # draw combat effects
        self.interaction_manager.combat_system.draw_effects(render_surface, self.camera)

        # draw UI at normal size after handling zoom
        if zoom != 1.0:
            # restore camera position
            self.camera.camera.x, self.camera.camera.y = original_camera_pos

            # scale surface and center it
            scaled_surface = pygame.transform.scale(render_surface, (WIDTH, HEIGHT))
            self.screen.fill(BLACK)
            self.screen.blit(scaled_surface, (0, 0))

        # always draw UI at normal size (never scale UI)
        self.ui_manager.draw_player_ui(self.screen, self.player)
        if self.interaction_manager.combat_system.combat_enemy:
            enemy = self.interaction_manager.combat_system.combat_enemy
            self.ui_manager.draw_enemy_ui(self.screen, enemy, enemy.HP, enemy.max_HP)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
