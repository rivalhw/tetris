import pygame
from game_init import load_fonts

def draw_game(screen, block, block_x, block_y, color, game_board, score, elapsed_time, level, small_font):
    # 背景渐变
    for y in range(600):
        gradient_value = min(255, y // 2)
        gradient_color = (0, 0, gradient_value)
        pygame.draw.line(screen, gradient_color, (0, y), (300, y))

    # 绘制游戏棋盘
    for y, row in enumerate(game_board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, pygame.Rect(x * 30, y * 30, 30, 30))
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x * 30, y * 30, 30, 30), 1)

    # 绘制当前方块
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, pygame.Rect((block_x + x) * 30, (block_y + y) * 30, 30, 30))
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((block_x + x) * 30, (block_y + y) * 30, 30, 30), 1)

    # 绘制得分
    score_text = small_font.render(f"得分: {score}", True, (255, 255, 255))
    screen.blit(score_text, (200, 10))

    # 绘制已玩时长
    time_text = small_font.render(f"时间: {elapsed_time} 秒", True, (255, 255, 255))
    screen.blit(time_text, (200, 30))

    # 绘制当前关卡数
    level_text = small_font.render(f"关卡: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))

def display_game_over(screen, font):
    game_over_text = font.render("游戏结束", True, (255, 0, 0))
    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (50, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
