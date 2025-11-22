import sys
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
    def __init__(self, text, x, y, action_code):
        self.rect = pygame.Rect(x, y, 450, 80)
        self.text = text
        self.text_surf = font_btn.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.action_code = action_code
        self.is_hovered = False

    def draw(self, surface):
        color = BTN_HOVER_COLOR if self.is_hovered else BTN_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        surface.blit(self.text_surf, self.text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return self.action_code
        return None


# main
def main_menu():
    center_x = SCREEN_WIDTH // 2 - 450 // 2

    btn_single = Button("Single Player(Task 1)", center_x, 200, "SINGLE")
    btn_online = Button("Online Mode(Task 2&3)", center_x, 300, "ONLINE")
    btn_pvp = Button("2 Players(Task 4)", center_x, 400, "PVP")

    buttons = [btn_single, btn_online, btn_pvp]

    running = True
    while running:
        title_surf = font_title.render("SandboxVR Wordle Task", True, GREEN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    for btn in buttons:
                        action = btn.check_click(mouse_pos)
                        if action:
                            print(f"Selected Mode: {action}")
                            return action

        for btn in buttons:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)


# run main
if __name__ == "__main__":
    while True:
        mode = main_menu()

        print(f"--> Loading game mode: {mode}...")

        pygame.time.delay(1000)
