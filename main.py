from settings import *  # Import all our constants


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
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
        self.clock.tick(FPS)

    def draw(self):
        # draw game
        self.screen.fill(BLACK)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()