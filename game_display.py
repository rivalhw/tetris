import pygame
from game_init import load_fonts

def draw_game(screen, block, block_x, block_y, color, game_board):
    screen.fill((0, 0, 0))  # 清屏

    # 绘制游戏棋盘
    for y, row in enumerate(game_board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, pygame.Rect(x * 30, y * 30, 30, 30))

    # 绘制当前方块
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, pygame.Rect((block_x + x) * 30, (block_y + y) * 30, 30, 30))




def display_game_over(screen):
    font, small_font, large_font, medium_font = load_fonts()  # 使用加载的字体
    game_over_text = large_font.render("游戏结束", True, (255, 0, 0))  # 确保显示中文
    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (50, 250))  # 居中显示
    pygame.display.flip()
    pygame.time.wait(2000)  # 等待2秒钟后退出游戏

