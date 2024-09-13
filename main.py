import pygame
from game_init import initialize_game
from game_logic import start_game
from game_display import display_game_over

def main():
    screen, clock, font, small_font, large_font, medium_font = initialize_game()
    level = 1
    running = True

    while running and level <= 10:
        level_complete = start_game(screen, clock, font, small_font, level)
        if level_complete:
            level += 1
        else:
            running = False

    display_game_over(screen, font)


if __name__ == "__main__":
    main()
