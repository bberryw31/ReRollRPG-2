from settings import *
from level import Level
from sprites.player import Player


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
        self.player = Player((self.level.spawn_point[0], self.level.spawn_point[1]), self.all_sprites)

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
        self.clock.tick(FPS)

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
