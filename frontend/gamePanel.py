import sys
import pygame
import random

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

    btn_single = Button("Single Player(Task 1)", center_x, 200, 450, 80, "SINGLE")
    btn_online = Button("Online Mode(Task 2&3)", center_x, 300, 450, 80, "ONLINE")
    btn_pvp = Button("2 Players(Task 4)", center_x, 400, 450, 80, "PVP")

    buttons = [btn_single, btn_online, btn_pvp]

    running = True
    while running:
        screen.fill(DARK_GRAY)
        title_surf = font_title.render("SandboxVR Wordle Task", True, GREEN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
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


# canvas class


class WordleCanvas:
    # single, serve mode
    GRID_ROWS = 6
    GRID_COLS = 5
    DEFAULT_CELL_SIZE = 70
    DEFAULT_CELL_MARGIN = 10

    # PVP mode
    PVP_CELL_SIZE = 40
    PVP_CELL_MARGIN = 7

    def __init__(self, x, y, pvp=False):
        # Canvas top-left position
        self.x = x
        self.y = y
        self.is_pvp = pvp

        if pvp:
            self.cell_size = self.PVP_CELL_SIZE
            self.cell_margin = self.PVP_CELL_MARGIN
            self.font_letter = pygame.font.Font(None, 40)  
        else:
            self.cell_size = self.DEFAULT_CELL_SIZE
            self.cell_margin = self.DEFAULT_CELL_MARGIN
            self.font_letter = pygame.font.Font(None, 60)

        # record for check easily
        self.record = [[None for _ in range(5)] for _ in range(6)]

        self.total_width = (
            self.GRID_COLS * self.cell_size + (self.GRID_COLS - 1) * self.cell_margin
        )
        self.total_height = (
            self.GRID_ROWS * self.cell_size + (self.GRID_ROWS - 1) * self.cell_margin
        )

    @classmethod
    def get_total_dimensions(cls, pvp=False):
        if pvp:
            cell_size = cls.PVP_CELL_SIZE
            cell_margin = cls.PVP_CELL_MARGIN
        else:
            cell_size = cls.DEFAULT_CELL_SIZE
            cell_margin = cls.DEFAULT_CELL_MARGIN

        width = cls.GRID_COLS * cell_size + (cls.GRID_COLS - 1) * cell_margin
        height = cls.GRID_ROWS * cell_size + (cls.GRID_ROWS - 1) * cell_margin
        return width, height

    def draw(self, surface, guesses, results, current_guess, current_row, game_over):
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
 
                x = self.x + col * (self.cell_size + self.cell_margin)
                y = self.y + row * (self.cell_size + self.cell_margin)
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                fill_color = DARK_GRAY
                border_color = GRAY
                letter = ""
 
                if row < current_row:
                    if row < len(results):
                        fill_color = results[row][col]
                        border_color = results[row][col]
                        letter = guesses[row][col]
 
                elif row == current_row and not game_over:
                    border_color = WHITE if col < len(current_guess) else GRAY
                    if col < len(current_guess):
                        letter = current_guess[col]

         
                pygame.draw.rect(surface, fill_color, rect, border_radius=5)
                pygame.draw.rect(surface, border_color, rect, 2, border_radius=5)

                # letter filled
                if letter:
                    letter_surf = self.font_letter.render(letter, True, WHITE)
                    letter_rect = letter_surf.get_rect(center=rect.center)
                    surface.blit(letter_surf, letter_rect)

    @staticmethod
    def line_check(guess, word_length=5):
        return len(guess) == word_length

    @staticmethod
    def result_check(colors):
        global GREEN
        return all(color == GREEN for color in colors)


# single
def game_loop_single():
    WORD_LIST = [
        "APPLE",
        "TIGER",
        "HOUSE",
        "GRAPE",
        "CHAIR",
        "TABLE",
        "PLANE",
        "CANDY",
        "FANCY",
        "DRIVE",
        "REACT",
    ]
 
    BTN_W, BTN_H = 150, 50
    WORD_LENGTH = 5
    MAX_GUESSES = 6

    btn_back = Button("Back", 20, 20, BTN_W, BTN_H, "BACK")
    btn_replay = Button("Replay", SCREEN_WIDTH - BTN_W - 20, 20, BTN_W, BTN_H, "REPLAY")
    game_buttons = [btn_back, btn_replay]



    SECRET_WORD = ""
    current_guess = ""
    guesses = []
    results = []
    current_row = 0
    game_over = False

    def check_guess(guess):
         pass

    def reset_game():
        pass

    #reset game in enter
    reset_game()
 

# run main
if __name__ == "__main__":
    while True:
        mode = main_menu()

        if mode == "SINGLE":
            game_loop_single()
        elif mode == "ONLINE":
            print("Online mode coming soon...")

        # pygame.time.delay(500)
