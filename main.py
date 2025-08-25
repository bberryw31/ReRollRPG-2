from settings import *
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("ReRollRPG 2")
        self.clock = pygame.time.Clock()
        self.running = True

        # setup
        self.setup()

    def setup(self):
        # load map
        game_map = load_pygame('../data/maps/lv1.tmx')
        print(game_map)

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        pygame.quit()


if __name__ == "__main__":
    # run game
    game = Game()
    game.run()


