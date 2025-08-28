from settings import *
from level import Level
from sprites.player import Player
from sprites.enemy import Enemy


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

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
        # create new game
        self.new_game()
        # game loop
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # update game
        self.all_sprites.update()

        # handle collisions
        self.handle_collisions()

        # game fps
        self.clock.tick(FPS)

    def handle_collisions(self):
        # check collisions
        self.check_player_wall_collision()
        self.check_player_enemy_collision()

    def check_player_wall_collision(self):
        # check player collision with wall
        for wall in self.level.walls:
            print(wall)
            if self.player.rect.colliderect(wall):
                self.resolve_collision(wall)
                break

    def check_player_enemy_collision(self):
        # find collided enemy sprites
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)

        if hit_enemies:
            for enemy in hit_enemies:
                print(enemy)
                self.resolve_collision(enemy.rect)
                # self.enemy_encounter(enemy)
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

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
