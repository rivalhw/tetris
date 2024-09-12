import pygame
from game_init import initialize_game
from game_logic import start_game
from game_display import display_game_over

def main():
    screen, clock, font = initialize_game()  # 初始化游戏
    level = 1
    running = True

    while running and level <= 10:  # 总共10关
        level_complete = start_game(screen, clock, font, level)
        if level_complete:
            level += 1
        else:
            running = False

    display_game_over(screen, font)

if __name__ == "__main__":
    main()
