import pygame

pygame.init()

# Screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
TITLE = "SandboxVR Wordle Game"

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
BTN_COLOR = (70, 130, 180)
BTN_HOVER_COLOR = (100, 149, 237)

# init panel
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font_title = pygame.font.Font(None, 60)
font_btn = pygame.font.Font(None, 50)


class Button:
    def __init__(self, text, x, y, width, height, action_code):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_surf = font_btn.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.action_code = action_code
        self.is_hovered = False


# main
def main_menu():
    running = True
    while running:

        pygame.display.flip()
        clock.tick(60)


# run main
if __name__ == "__main__":
    while True:
        mode = main_menu()
        pygame.time.delay(1000)
