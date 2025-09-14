from settings import *


class Chest(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)

        # load chest spritesheet
        self.spritesheet = pygame.image.load("../assets/sprites/chest/chest.png")

        # define frame dimensions (you'll need to measure your spritesheet)
        self.frame_width = 16  # adjust based on your chest size
        self.frame_height = 16  # adjust based on your chest size

        # load frames
        self.closed_frame = self.get_frame(0, 0)  # first row, first column
        self.open_frame = self.get_frame(1, 0)  # first row, second column (if it exists)

        # chest state
        self.is_open = False
        self.image = self.closed_frame
        self.rect = self.image.get_rect(center=position)

    def get_frame(self, col, row):
        # extract a single frame from the spritesheet
        x = col * self.frame_width
        y = row * self.frame_height

        frame_rect = pygame.Rect(x, y, self.frame_width, self.frame_height)
        frame = self.spritesheet.subsurface(frame_rect).copy()

        # scale up to match game scale
        frame = pygame.transform.scale_by(frame, SCALE_FACTOR)

        return frame.convert_alpha()

    def open_chest(self):
        if not self.is_open:
            self.is_open = True
            self.image = self.open_frame
            return True  # return True if chest was successfully opened
        return False  # chest was already open
