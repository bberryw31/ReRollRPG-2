from settings import *
from enum import Enum


class InteractionType(Enum):
    FIGHT = "fight"
    OPEN = "open"


class InteractionPopup:
    def __init__(self):
        # state management
        self.active = False
        self.interaction_type = None
        self.target_name = None
        self.target_object = None

        # popup ui
        self.font = pygame.font.SysFont("comicsans", 36)
        self.small_font = pygame.font.SysFont("comicsans", 20)

        # result
        self.confirmed = False
        self.completed = False

    def start_interaction(self, interaction_type, target_name, target_object=None):
        self.active = True
        self.interaction_type = interaction_type
        self.target_name = target_name
        self.target_object = target_object
        self.confirmed = False
        self.completed = False
        print("Starting interaction", interaction_type, target_name)

    def handle_input(self, event):
        if not self.active:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.confirmed = True
                self.execute_interaction()
                return True
            else:
                self.confirmed = False
                self.end_interaction()
                return True
        return False

    def get_popup_text(self):
        # choose appropriate text for current interaction
        if self.interaction_type == InteractionType.FIGHT:
            return f"Fight {self.target_name}?", "Press E to confirm"
        # to be added later

    def draw(self, screen):
        if not self.active:
            return
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        # Popup box
        popup_width, popup_height = 400, 150
        popup_x = (screen.get_width() - popup_width) // 2
        popup_y = (screen.get_height() - popup_height) // 2

        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(screen, (50, 50, 50), popup_rect)
        pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2)

        # Get text for current interaction
        main_text, instruction_text = self.get_popup_text()

        # Draw text
        main_surface = self.font.render(main_text, True, (255, 255, 255))
        main_rect = main_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + 50))
        screen.blit(main_surface, main_rect)

        inst_surface = self.small_font.render(instruction_text, True, (200, 200, 200))
        inst_rect = inst_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + 100))
        screen.blit(inst_surface, inst_rect)

    def execute_interaction(self):
        print("Executing interaction")

    def end_interaction(self):
        self.active = False
        self.completed = True
        print("Ending interaction")
