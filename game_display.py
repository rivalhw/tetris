import pygame
from game_init import load_fonts

# game_display.py
# game_display.py
def draw_game(screen, block, block_x, block_y, color, game_board):
    # 背景渐变
    for y in range(600):
        gradient_value = min(255, y // 2)  # 确保颜色值在 0 到 255 之间
        gradient_color = (0, 0, gradient_value)
        pygame.draw.line(screen, gradient_color, (0, y), (300, y))
    
    # 绘制游戏棋盘
    for y, row in enumerate(game_board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, pygame.Rect(x * 30, y * 30, 30, 30))
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x * 30, y * 30, 30, 30), 1)  # 白色边框

    # 绘制当前方块
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, pygame.Rect((block_x + x) * 30, (block_y + y) * 30, 30, 30))
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((block_x + x) * 30, (block_y + y) * 30, 30, 30), 1)  # 白色边框


def display_game_over(screen):
    font, small_font, large_font, medium_font = load_fonts()  # 使用加载的字体
    game_over_text = large_font.render("游戏结束", True, (255, 0, 0))  # 确保显示中文
    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (50, 250))  # 居中显示
    pygame.display.flip()
    pygame.time.wait(2000)  # 等待2秒钟后退出游戏

