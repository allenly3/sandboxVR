import sys
import pygame
import random
import requests

pygame.init()

# Screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
TITLE = "SandboxVR Wordle Game"

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
BTN_COLOR = (70, 130, 180)
BTN_HOVER_COLOR = (100, 149, 237)
BTN_SELECT_COLOR = (0, 255, 0)

# init panel
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font_title = pygame.font.Font(None, 60)
font_btn = pygame.font.Font(None, 50)

# global var
WORD_LENGTH = 5
MAX_GUESSES = 6
BTN_W, BTN_H = 150, 50
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
API_BASE_URL = "http://127.0.0.1:8000"
NORMAL = True


# region button class
class Button:
    def __init__(self, text, x, y, width, height, action_code):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_surf = font_btn.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.action_code = action_code
        self.is_hovered = False
        self.is_selected = None

    def draw(self, surface):

        if self.is_selected is None:
            color = BTN_HOVER_COLOR if self.is_hovered else BTN_COLOR
        else:
            if self.is_selected:
                color = BTN_SELECT_COLOR
            else:
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


# region WordleCanvas class
class WordleCanvas:
    # single, serve mode
    GRID_ROWS = 6
    GRID_COLS = 5
    DEFAULT_CELL_SIZE = 70
    DEFAULT_CELL_MARGIN = 10

    # PVP mode
    PVP_CELL_SIZE = 50
    PVP_CELL_MARGIN = 8

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

        # for pvp
        self.completeRow = 0

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

    def draw(
        self,
        surface,
        guesses,
        results,
        current_guess,
        current_row,
        game_over,
        opponentRow=None,
    ):
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
                        if opponentRow is not None:
                            if row < opponentRow:
                                letter = guesses[row][col]
                        else:
                            letter = guesses[row][col]

                elif row == current_row and not game_over:
                    border_color = WHITE if col < len(current_guess) else GRAY
                    if col < len(current_guess) and not self.is_pvp:
                        letter = current_guess[col]

                pygame.draw.rect(surface, fill_color, rect, border_radius=5)
                pygame.draw.rect(surface, border_color, rect, 2, border_radius=5)

                # letter filled
                if letter:
                    letter_surf = self.font_letter.render(letter, True, WHITE)
                    letter_rect = letter_surf.get_rect(center=rect.center)
                    surface.blit(letter_surf, letter_rect)
                    
    #region wordleCanvas static
    @staticmethod
    def line_check(guess, word_length=5):
        return len(guess) == word_length

    @staticmethod
    def result_check(colors):
        global GREEN
        return all(color == GREEN for color in colors)

    @staticmethod
    def guess_check(guess, SECRET_WORD):
        colors = [GRAY] * WORD_LENGTH
        secret_word_letters = list(SECRET_WORD)

        # find correct
        for i in range(WORD_LENGTH):
            if guess[i] == SECRET_WORD[i]:
                colors[i] = GREEN
                secret_word_letters[i] = None

        # find present
        for i in range(WORD_LENGTH):
            if colors[i] == GREEN:
                continue

            try:
                idx = secret_word_letters.index(guess[i])
                colors[i] = YELLOW
                secret_word_letters[idx] = None
            except ValueError:
                pass

        return colors


# region main menu
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


# region  single
def game_loop_single():

    btn_back = Button("Back", 20, 20, BTN_W, BTN_H, "BACK")
    btn_replay = Button("Replay", SCREEN_WIDTH - BTN_W - 20, 20, BTN_W, BTN_H, "REPLAY")
    game_buttons = [btn_back, btn_replay]

    # in game var
    SECRET_WORD = ""
    current_guess = ""
    guesses = []
    results = []
    current_row = 0
    game_over = False

    def reset_game():
        nonlocal SECRET_WORD, current_guess, guesses, results, current_row, game_over
        SECRET_WORD = random.choice(WORD_LIST).upper()
        print(f"New Secret Word: {SECRET_WORD}")
        current_guess = ""
        guesses = []
        results = []
        current_row = 0
        game_over = False

    # reset game in enter
    reset_game()

    grid_total_width, grid_total_height = WordleCanvas.get_total_dimensions(pvp=False)

    grid_start_x = (SCREEN_WIDTH - grid_total_width) // 2
    grid_start_y = 120
    # create canvas for single
    wordle_canvas = WordleCanvas(grid_start_x, grid_start_y, pvp=False)

    running = True
    while running:
        screen.fill(DARK_GRAY)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in game_buttons:
                        action = btn.check_click(mouse_pos)

                        if action == "BACK":
                            return

                        elif action == "REPLAY":
                            reset_game()
                            print("Game reset!")

            # -keyboard listener
            if event.type == pygame.KEYDOWN and not game_over:
                key = event.key
                # print(key)
                # A-Z
                if pygame.K_a <= key <= pygame.K_z:
                    char = chr(key).upper()
                    if len(current_guess) < WORD_LENGTH:
                        current_guess += char

                    # print(guesses)
                    # print(results)
                    # print(current_guess)

                # delete
                elif key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]

                # Enter
                elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:

                    if WordleCanvas.line_check(current_guess, WORD_LENGTH):
                        guess_colors = WordleCanvas.guess_check(
                            current_guess, SECRET_WORD
                        )

                        guesses.append(current_guess)
                        results.append(guess_colors)
                        current_guess = ""

                        if WordleCanvas.result_check(guess_colors):
                            game_over = True
                            # print("Win!")
                        elif current_row + 1 == MAX_GUESSES:
                            game_over = True
                            # print("Game Over. The word was ", SECRET_WORD)

                        current_row += 1
                    else:
                        print("Guess must be 5 letters long!")

        for btn in game_buttons:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        wordle_canvas.draw(
            screen, guesses, results, current_guess, current_row, game_over
        )

        resultColor = GREEN

        if game_over:
            message = ""

            if current_row <= 6 and WordleCanvas.result_check(results[current_row - 1]):
                resultColor = GREEN
                message = "You Win!"
            else:
                resultColor = YELLOW
                message = f"Game Over. Word is: {SECRET_WORD}"

            font_message = pygame.font.Font(None, 50)

            message_surf = font_message.render(message, True, resultColor)
            message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(message_surf, message_rect)

        pygame.display.flip()
        clock.tick(60)


# region single ONLINE


def send_api_reset():
    try:
        response = requests.post(f"{API_BASE_URL}/reset")
        response.raise_for_status()
        print("ONLINE Game reset successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"RESET Error during reset: {e}")
        return None


def send_api_guess(word):
    global NORMAL
    try:
        if NORMAL:
            response = requests.post(f"{API_BASE_URL}/normalguess/{word}")
        else:
            response = requests.post(f"{API_BASE_URL}/cheatguess/{word}")
        response.raise_for_status()
        print("ONLINE Game Guess Checked.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"RESET Error during reset: {e}")
        return None


def game_loop_single_online():
    global NORMAL

    btn_back = Button("Back", 20, 20, BTN_W, BTN_H, "BACK")
    btn_replay = Button("Replay", SCREEN_WIDTH - BTN_W - 20, 20, BTN_W, BTN_H, "REPLAY")

    btn_normal = Button("Normal", 350, 20, BTN_W, BTN_H, "NORMAL")
    btn_cheat = Button("Cheat", SCREEN_WIDTH - BTN_W - 350, 20, BTN_W, BTN_H, "CHEAT")

    game_buttons = [btn_back, btn_replay, btn_normal, btn_cheat]

    if NORMAL:
        btn_normal.is_selected = True
        btn_cheat.is_selected = False
    else:
        btn_normal.is_selected = False
        btn_cheat.is_selected = True

    # in game var
    SECRET_WORD = ""
    current_guess = ""
    guesses = []
    results = []
    current_row = 0
    game_over = False

    def reset_game():
        nonlocal SECRET_WORD, current_guess, guesses, results, current_row, game_over
        current_guess = ""
        guesses = []
        results = []
        current_row = 0
        game_over = False
        if send_api_reset() is None:
            print("ERR: NO SERVER CONNECTION.")
            return False

        return True

    # reset game in enter
    if not reset_game():
        return

    grid_total_width, grid_total_height = WordleCanvas.get_total_dimensions(pvp=False)

    grid_start_x = (SCREEN_WIDTH - grid_total_width) // 2
    grid_start_y = 120
    # create canvas for single
    wordle_canvas = WordleCanvas(grid_start_x, grid_start_y, pvp=False)

    running = True
    while running:
        screen.fill(DARK_GRAY)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in game_buttons:
                        action = btn.check_click(mouse_pos)

                        if action == "BACK":
                            return

                        elif action == "REPLAY":
                            reset_game()

                        elif action == "NORMAL":
                            NORMAL = True
                            btn_normal.is_selected = True
                            btn_cheat.is_selected = False
                        elif action == "CHEAT":
                            NORMAL = False
                            btn_normal.is_selected = False
                            btn_cheat.is_selected = True

            # -keyboard listener
            if event.type == pygame.KEYDOWN and not game_over:
                key = event.key
                # print(key)
                # A-Z
                if pygame.K_a <= key <= pygame.K_z:
                    char = chr(key).upper()
                    if len(current_guess) < WORD_LENGTH:
                        current_guess += char

                    # print(guesses)
                    # print(results)
                    # print(current_guess)

                # delete
                elif key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]

                # Enter
                elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:

                    if WordleCanvas.line_check(current_guess, WORD_LENGTH):
                        resp = send_api_guess(current_guess)
                        if resp is None:
                            print("NO SERVER CONNECTION.")
                            return
                        guess_colors = [tuple(c) for c in resp["colors"]]
                        guesses.append(current_guess)
                        results.append(guess_colors)
                        current_guess = ""

                        if resp["correct"]:
                            game_over = True
                            # print("Win!")
                        elif current_row + 1 == MAX_GUESSES:
                            game_over = True
                            # print("Game Over. The word was ", SECRET_WORD)

                        current_row += 1
                    else:
                        print("Guess must be 5 letters long!")

        for btn in game_buttons:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        wordle_canvas.draw(
            screen, guesses, results, current_guess, current_row, game_over
        )

        resultColor = GREEN

        if game_over:
            message = ""

            if current_row <= 6 and WordleCanvas.result_check(results[current_row - 1]):
                resultColor = GREEN
                message = "You Win!"
            else:
                resultColor = YELLOW
                message = f"Game Over. Word is: {SECRET_WORD}"

            font_message = pygame.font.Font(None, 50)

            message_surf = font_message.render(message, True, resultColor)
            message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, 95))
            screen.blit(message_surf, message_rect)

        pygame.display.flip()
        clock.tick(60)


# region pvp
def game_loop_pvp():

    btn_back = Button("Back", 20, 20, BTN_W, BTN_H, "BACK")
    btn_replay = Button("Replay", SCREEN_WIDTH - BTN_W - 20, 20, BTN_W, BTN_H, "REPLAY")
    game_buttons = [btn_back, btn_replay]

    SECRET_WORD = ""

    # p1
    current_guess1 = ""
    guesses1 = []
    results1 = []
    current_row1 = 0
    game_over1 = False

    # p2
    current_guess2 = ""
    guesses2 = []
    results2 = []
    current_row2 = 0
    game_over2 = False

    # whole game state
    game_over = False

    # player to enter letters
    active_player = random.choice([1, 2])

    def reset_game():
        nonlocal SECRET_WORD, current_guess1, guesses1, results1, current_row1, game_over1
        nonlocal current_guess2, guesses2, results2, current_row2, game_over2
        nonlocal game_over, active_player

        SECRET_WORD = random.choice(WORD_LIST).upper()
        print(f"New Secret Word: {SECRET_WORD}")

        current_guess1, guesses1, results1, current_row1, game_over1 = (
            "",
            [],
            [],
            0,
            False,
        )
        current_guess2, guesses2, results2, current_row2, game_over2 = (
            "",
            [],
            [],
            0,
            False,
        )

        game_over = False
        active_player = random.choice([1, 2])

    reset_game()

    grid_total_width, grid_total_height = WordleCanvas.get_total_dimensions(pvp=True)

    # set postion
    padding = 160
    total_area_width = 2 * grid_total_width + padding

    start_x_center = (SCREEN_WIDTH - total_area_width) // 2
    grid_start_y = 120

    grid1_start_x = start_x_center
    canvas1 = WordleCanvas(grid1_start_x, grid_start_y, pvp=True)

    grid2_start_x = start_x_center + grid_total_width + padding
    canvas2 = WordleCanvas(grid2_start_x, grid_start_y, pvp=True)

    running = True
    while running:
        screen.fill(DARK_GRAY)
        mouse_pos = pygame.mouse.get_pos()

        # event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in game_buttons:
                        action = btn.check_click(mouse_pos)

                        if action == "BACK":
                            return

                        elif action == "REPLAY":
                            reset_game()
                            canvas1.completeRow = 0
                            canvas2.completeRow = 0
                            print("PVP Game reset!")

            # keyboard
            if event.type == pygame.KEYDOWN and not game_over:

                if active_player == 1 and not game_over1:
                    current_guess = current_guess1

                elif active_player == 2 and not game_over2:
                    current_guess = current_guess2

                else:
                    continue

                key = event.key

                # -keyboard listener
                if pygame.K_a <= key <= pygame.K_z:
                    char = chr(key).upper()
                    if len(current_guess) < WORD_LENGTH:
                        current_guess += char

                # delete
                elif key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]

                # Enter
                elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:

                    if WordleCanvas.line_check(current_guess, WORD_LENGTH):
                        guess_colors = WordleCanvas.guess_check(
                            current_guess, SECRET_WORD
                        )

                        guesses = guesses1 if active_player == 1 else guesses2
                        results = results1 if active_player == 1 else results2

                        guesses.append(current_guess)
                        results.append(guess_colors)

                        is_win = WordleCanvas.result_check(guess_colors)

                        current_guess = ""
                        if active_player == 1:
                            current_guess1 = ""
                            current_row1 += 1
                            canvas1.completeRow = current_row1

                            if is_win:
                                game_over1 = True
                            elif current_row1 == MAX_GUESSES:
                                game_over1 = True

                            # switch palyer
                            active_player = 2

                        elif active_player == 2:
                            current_guess2 = ""
                            current_row2 += 1
                            canvas2.completeRow = current_row2

                            if is_win:
                                game_over2 = True
                            elif current_row2 == MAX_GUESSES:
                                game_over2 = True

                            # switch palyer
                            active_player = 1

                        # whole game state
                        if (game_over1 or game_over2) and current_row2 == current_row1:
                            game_over = True
                            print("PVP Game Over!")

                    else:
                        print(f"Guess must be {WORD_LENGTH} letters long!")

                if active_player == 1:
                    current_guess1 = current_guess
                elif active_player == 2:
                    current_guess2 = current_guess

        for btn in game_buttons:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        #  Player 1
        player1_msg = (
            "Player 1 (Active)" if active_player == 1 and not game_over else "Player 1"
        )
        player1_color = GREEN if active_player == 1 and not game_over1 else WHITE
        font_player = pygame.font.Font(None, 40)
        p1_surf = font_player.render(player1_msg, True, player1_color)
        p1_rect = p1_surf.get_rect(
            center=(canvas1.x + canvas1.total_width // 2, canvas1.y - 20)
        )
        screen.blit(p1_surf, p1_rect)

        # Player 2
        player2_msg = (
            "Player 2 (Active)" if active_player == 2 and not game_over else "Player 2"
        )
        player2_color = GREEN if active_player == 2 and not game_over2 else WHITE
        p2_surf = font_player.render(player2_msg, True, player2_color)
        p2_rect = p2_surf.get_rect(
            center=(canvas2.x + canvas2.total_width // 2, canvas2.y - 20)
        )
        screen.blit(p2_surf, p2_rect)

        # draw 2 wordle
        canvas1.draw(
            screen,
            guesses1,
            results1,
            current_guess1,
            current_row1,
            game_over1,
            canvas2.completeRow,
        )
        canvas2.draw(
            screen,
            guesses2,
            results2,
            current_guess2,
            current_row2,
            game_over2,
            canvas1.completeRow,
        )

        if game_over:

            if WordleCanvas.result_check(results1[-1]) and WordleCanvas.result_check(
                results2[-1]
            ):
                message = "Draw Game!"
                msg_color = GREEN
            elif WordleCanvas.result_check(results1[-1]):
                message = "Player 1 Wins!"
                msg_color = GREEN
            elif WordleCanvas.result_check(results2[-1]):
                message = "Player 2 Wins!"
                msg_color = GREEN
            else:
                message = f"Game Over! Word: {SECRET_WORD}"
                msg_color = WHITE

            font_final = pygame.font.Font(None, 80)
            final_surf = font_final.render(message, True, msg_color)
            final_rect = final_surf.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
            )
            screen.blit(final_surf, final_rect)

        pygame.display.flip()
        clock.tick(60)


# region run main
if __name__ == "__main__":
    while True:
        mode = main_menu()

        if mode == "SINGLE":
            game_loop_single()
        elif mode == "PVP":
            game_loop_pvp()
        elif mode == "ONLINE":
            game_loop_single_online()

        # pygame.time.delay(500)
