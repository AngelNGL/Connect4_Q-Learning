import pygame
from Connect4.AI_cpu.config import get_epsilon, set_epsilon
from Connect4.UI.theme import BLUE, RED, GRAY, WHITE, BLACK, WIDTH

def draw_button(screen, rect, text, font, mouse_pos,
                bg_color=GRAY, hover_color=BLUE, text_color=WHITE):
    color = hover_color if rect.collidepoint(mouse_pos) else bg_color
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, rect, 3, border_radius=12)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_main_menu(game, mouse_pos):
    game.screen.fill(BLACK)
    title = game.fonts["title"].render("CONNECT 4", True, WHITE)
    game.screen.blit(title, title.get_rect(center=(WIDTH//2, 90)))

    draw_button(game.screen, game.main_buttons["play"], "PLAY", game.fonts["button"], mouse_pos)
    draw_button(game.screen, game.main_buttons["rng"], "SET RNG", game.fonts["button"], mouse_pos)
    draw_button(game.screen, game.main_buttons["exit"], "EXIT", game.fonts["button"], mouse_pos)
    pygame.display.update()

def draw_difficulty_menu(game, mouse_pos):
    game.screen.fill(BLACK)
    title = game.fonts["title"].render("SELECT DIFFICULTY", True, WHITE)
    game.screen.blit(title, title.get_rect(center=(WIDTH//2, 90)))

    draw_button(game.screen, game.difficulty_buttons["easy"], "EASY", game.fonts["button"], mouse_pos)
    draw_button(game.screen, game.difficulty_buttons["normal"], "NORMAL", game.fonts["button"], mouse_pos)
    draw_button(game.screen, game.difficulty_buttons["hard"], "HARD", game.fonts["button"], mouse_pos)
    draw_button(game.screen, game.difficulty_buttons["return"], "RETURN", game.fonts["button"], mouse_pos)
    pygame.display.update()

def draw_rng_menu(game, mouse_pos):
    game.screen.fill(BLACK)
    title = game.fonts["title"].render("SET RNG", True, WHITE)
    game.screen.blit(title, title.get_rect(center=(WIDTH//2, 90)))

    info = game.fonts["small"].render("CPU RANDOM MOVE CHANCE", True, WHITE)
    game.screen.blit(info, info.get_rect(center=(WIDTH//2, 160)))
    value_text = game.fonts["title"].render(f"{game.temp_rng:.2f}", True, RED)
    game.screen.blit(value_text, value_text.get_rect(center=(WIDTH//2, 260)))

    draw_button(game.screen, game.rng_buttons["minus"], "-", game.fonts["button"], mouse_pos)
    draw_button(game.screen, game.rng_buttons["plus"], "+", game.fonts["button"], mouse_pos)
    draw_button(game.screen, game.rng_buttons["save"], "SAVE", game.fonts["button"], mouse_pos)
    draw_button(game.screen, game.rng_buttons["return"], "RETURN", game.fonts["button"], mouse_pos)
    pygame.display.update()

def handle_menu_click(game, pos):
    if game.screen_state == "main_menu":
        if game.main_buttons["play"].collidepoint(pos):
            game.screen_state = "difficulty_menu"
        elif game.main_buttons["rng"].collidepoint(pos):
            game.temp_rng = get_epsilon()
            game.screen_state = "rng_menu"
        elif game.main_buttons["exit"].collidepoint(pos):
            game.running = False

    elif game.screen_state == "difficulty_menu":
        if game.difficulty_buttons["easy"].collidepoint(pos):
            game.start_game("easy")
        elif game.difficulty_buttons["normal"].collidepoint(pos):
            game.start_game("normal")
        elif game.difficulty_buttons["hard"].collidepoint(pos):
            game.start_game("hard")
        elif game.difficulty_buttons["return"].collidepoint(pos):
            game.screen_state = "main_menu"

    elif game.screen_state == "rng_menu":
        if game.rng_buttons["minus"].collidepoint(pos):
            game.temp_rng = max(0.0, round(game.temp_rng - 0.05, 2))
        elif game.rng_buttons["plus"].collidepoint(pos):
            game.temp_rng = min(1.0, round(game.temp_rng + 0.05, 2))
        elif game.rng_buttons["save"].collidepoint(pos):
            set_epsilon(game.temp_rng)
            game.screen_state = "main_menu"
        elif game.rng_buttons["return"].collidepoint(pos):
            game.screen_state = "main_menu"

def draw_endgame_buttons(game, pos):
    play_rect = game.endgame_buttons["play_again"]
    menu_rect = game.endgame_buttons["main_menu"]
    play_color = BLUE if play_rect.collidepoint(pos) else GRAY
    menu_color = RED if menu_rect.collidepoint(pos) else GRAY

    pygame.draw.rect(game.screen, play_color, play_rect, border_radius=12)
    pygame.draw.rect(game.screen, WHITE, play_rect, 3, border_radius=12)
    pygame.draw.rect(game.screen, menu_color, menu_rect, border_radius=12)
    pygame.draw.rect(game.screen, WHITE, menu_rect, 3, border_radius=12)

    play_text = game.fonts["button"].render("PLAY AGAIN", True, WHITE)
    menu_text = game.fonts["button"].render("MAIN MENU", True, WHITE)

    game.screen.blit(play_text, play_text.get_rect(center=play_rect.center))
    game.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

def handle_endgame_click(game, pos):
    if game.endgame_buttons["play_again"].collidepoint(pos):
        game.reset_match()
    elif game.endgame_buttons["main_menu"].collidepoint(pos):
        game.player_wins = 0
        game.cpu_wins = 0
        game.screen_state = "main_menu"
        game.message = "Your turn"
