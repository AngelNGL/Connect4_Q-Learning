import pygame
from Connect4.AI_cpu.game_logic import (create_board, drop_piece, get_valid_moves, check_winner,
                                        is_draw, PLAYER_PIECE, CPU_PIECE, get_next_open_row, convert_board)
from Connect4.AI_cpu.agent import QLearningAgent
from Connect4.AI_cpu.train_data import QTABLE_FILES, DEFAULT_ALPHA, DEFAULT_GAMMA
from Connect4.AI_cpu.config import get_epsilon
from Connect4.UI.menus import (draw_main_menu, draw_difficulty_menu, draw_rng_menu, draw_endgame_buttons,
                               handle_menu_click, handle_endgame_click)
from Connect4.UI.theme import (BLUE, RED, GRAY, BLACK, WHITE, ROWS, COLS, CELL_SIZE,
                               WIDTH, HEIGHT, RADIUS, load_fonts)
import random


class GameUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect4")
        self.fonts = load_fonts()
        self.font = self.fonts["main"]
        self.running = True
        self.screen_state = "main_menu"

        self.board = create_board()
        self.player_turn = True
        self.game_over = False
        self.message = "Your turn"
        self.last_move = None
        self.player_wins = 0
        self.cpu_wins = 0

        self.cpu_delay_ms = 700
        self.cpu_turn_start = None

        self.animating = False
        self.animation_piece = None
        self.animation_col = None
        self.animation_target_row = None
        self.animation_y = None
        self.animation_speed = 16

        self.difficulty = "normal"
        self.temp_rng = get_epsilon()
        self.agent = None

        self.main_buttons = {
            "play": pygame.Rect(WIDTH//2 - 140, 180, 280, 70),
            "rng": pygame.Rect(WIDTH//2 - 140, 280, 280, 70),
            "exit": pygame.Rect(WIDTH//2 - 140, 380, 280, 70),
        }
        self.difficulty_buttons = {
            "easy": pygame.Rect(WIDTH//2 - 140, 160, 280, 70),
            "normal": pygame.Rect(WIDTH//2 - 140, 250, 280, 70),
            "hard": pygame.Rect(WIDTH//2 - 140, 340, 280, 70),
            "return": pygame.Rect(WIDTH//2 - 140, 430, 280, 70),
        }
        self.rng_buttons = {
            "minus": pygame.Rect(WIDTH//2 - 170, 300, 70, 70),
            "plus": pygame.Rect(WIDTH//2 + 100, 300, 70, 70),
            "save": pygame.Rect(WIDTH//2 - 140, 420, 130, 60),
            "return": pygame.Rect(WIDTH//2 + 10, 420, 130, 60),
        }
        self.endgame_buttons = {
            "play_again": pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 40, 150, 60),
            "main_menu": pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 40, 150, 60),
        }

    def load_agent(self, difficulty):
        self.difficulty = difficulty
        epsilon = get_epsilon()
        self.agent = QLearningAgent(DEFAULT_ALPHA, DEFAULT_GAMMA, epsilon)
        loaded = self.agent.load_q_table(QTABLE_FILES[difficulty])

        if loaded:
            print(f"Loading Q-table for {difficulty}")
        else:
            print(f"Error loading Q-table for {difficulty}")
        self.agent.set_epsilon(epsilon)
        return loaded

    def start_game(self, difficulty):
        loaded = self.load_agent(difficulty)
        if not loaded:
            return
        self.player_wins = 0
        self.cpu_wins = 0
        self.reset_match()
        self.screen_state = "game"

    def draw_top_bar(self, mouse_x=None):
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, CELL_SIZE))
        if not self.game_over and self.player_turn and not self.animating and mouse_x is not None:
            col = mouse_x // CELL_SIZE
            if 0 <= col < COLS:
                pygame.draw.circle(
                    self.screen, BLUE,
                    (col*CELL_SIZE + CELL_SIZE//2, CELL_SIZE//2),
                    RADIUS
                )
        text = self.font.render(self.message, True, WHITE)
        self.screen.blit(text, (20, 10))
        score_text = self.font.render(
            f"PLAYER: {self.player_wins}   CPU: {self.cpu_wins}",
            True, WHITE
        )
        self.screen.blit(score_text, (20, 45))

    def draw_board(self, mouse_pos=None):
        self.screen.fill(BLACK)
        mouse_x = mouse_pos[0] if mouse_pos else None
        self.draw_top_bar(mouse_x)

        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = (row+1) * CELL_SIZE
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))

                piece = self.board[row][col]
                color = BLACK
                if piece == PLAYER_PIECE:
                    color = BLUE
                elif piece == CPU_PIECE:
                    color = RED
                center = (x + CELL_SIZE//2, y + CELL_SIZE//2)
                pygame.draw.circle(self.screen, color, center, RADIUS)
                if self.last_move == (row, col):
                    pygame.draw.circle(self.screen, WHITE, center, RADIUS, 4)

        if self.animating:
            color = BLUE if self.animation_piece == PLAYER_PIECE else RED
            x = self.animation_col * CELL_SIZE + CELL_SIZE//2
            y = int(self.animation_y)
            pygame.draw.circle(self.screen, color, (x,y), RADIUS)

        if self.game_over and mouse_pos is not None:
            draw_endgame_buttons(self, mouse_pos)
        pygame.display.update()

    def handle_player_move(self, col):
        if self.animating:
            return
        if col not in get_valid_moves(self.board):
            self.message = "Invalid move"
            return
        row = get_next_open_row(self.board, col)
        self.start_fall_animation(col, row, PLAYER_PIECE)

    def handle_cpu_move(self):
        if self.animating or self.agent is None:
            return
        valid_moves = get_valid_moves(self.board)
        if not valid_moves:
            self.game_over = True
            self.message = "Draw!"
            return
        state = convert_board(self.board)

        col = self.agent.choose_action(state, valid_moves)
        row = get_next_open_row(self.board, col)
        self.start_fall_animation(col, row, CPU_PIECE)

    def start_fall_animation(self, col, row, piece):
        self.animating = True
        self.animation_piece = piece
        self.animation_col = col
        self.animation_target_row = row
        self.animation_y = CELL_SIZE//2

    def resolve_move_after_animation(self):
        piece = self.animation_piece
        if check_winner(self.board, piece):
            self.game_over = True
            if piece == PLAYER_PIECE:
                self.player_wins += 1
                self.message = "You win!"
            else:
                self.cpu_wins += 1
                self.message = "CPU wins!"
            return
        if is_draw(self.board):
            self.game_over = True
            self.message = "Draw!"
            return
        if piece == PLAYER_PIECE:
            self.player_turn = False
            self.message = "CPU's turn"
            self.cpu_turn_start = pygame.time.get_ticks()
        else:
            self.player_turn = True
            self.message = "Your turn"
            self.cpu_turn_start = None

    def update_animation(self):
        if not self.animating:
            return
        target_y = (self.animation_target_row+1)*CELL_SIZE + CELL_SIZE//2
        self.animation_y += self.animation_speed
        if self.animation_y >= target_y:
            self.animation_y = target_y
            drop_piece(self.board, self.animation_col, self.animation_piece)
            self.last_move = (self.animation_target_row, self.animation_col)
            self.animating = False
            self.resolve_move_after_animation()

    def reset_match(self):
        self.board = create_board()
        self.player_turn = random.choice([True, False])
        self.game_over = False
        self.last_move = None

        self.animating = False
        self.animation_piece = None
        self.animation_col = None
        self.animation_target_row = None
        self.animation_y = None
        self.cpu_turn_start = None

        if self.player_turn:
            self.message = "You start!"
        else:
            self.message = "CPU starts!"
            self.cpu_turn_start = pygame.time.get_ticks()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.screen_state in ("main_menu", "difficulty_menu", "rng_menu"):
                        handle_menu_click(self, event.pos)
                    elif self.screen_state == "game":
                        if self.game_over:
                            handle_endgame_click(self, event.pos)
                        elif self.player_turn  and not self.animating:
                            col = event.pos[0] // CELL_SIZE
                            self.handle_player_move(col)

            if self.screen_state == "game":
                if not self.game_over and not self.player_turn and not self.animating:
                    if self.cpu_turn_start is not None:
                        now = pygame.time.get_ticks()
                        if now - self.cpu_turn_start >= self.cpu_delay_ms:
                            self.handle_cpu_move()
                self.update_animation()
                self.draw_board(mouse_pos)

            elif self.screen_state == "main_menu":
                draw_main_menu(self, mouse_pos)
            elif self.screen_state == "difficulty_menu":
                draw_difficulty_menu(self, mouse_pos)
            elif self.screen_state == "rng_menu":
                draw_rng_menu(self, mouse_pos)

            clock.tick(60)
        pygame.quit()
