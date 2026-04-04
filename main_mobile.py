"""
Tetris Mobile Version for Android
使用 pygame 和 buildozer 打包成 APK
"""
import pygame
import sys
from game_init import initialize_game, show_start_screen
from game_logic_mobile import start_game_mobile
from game_display_mobile import display_game_over
from sound_manager import SoundManager


def main():
    # 初始化 Pygame
    pygame.init()
    
    # 设置手机屏幕尺寸（竖屏）
    screen_width = 480
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetris Mobile")
    
    # 移动端配置
    mobile_config = {
        'cell_size': 26,           # 适合手机屏幕的格子大小
        'board_cols': 10,
        'board_rows': 20,
        'sidebar_width': 100,
        'padding': 20,
    }
    
    # 加载字体
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    large_font = pygame.font.SysFont(None, 56)
    medium_font = pygame.font.SysFont(None, 40)
    tiny_font = pygame.font.SysFont(None, 18)
    
    # 尝试加载中文字体
    try:
        import os
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                font = pygame.font.Font(fp, 32)
                small_font = pygame.font.Font(fp, 20)
                large_font = pygame.font.Font(fp, 56)
                medium_font = pygame.font.Font(fp, 40)
                tiny_font = pygame.font.Font(fp, 18)
                break
    except:
        pass
    
    clock = pygame.time.Clock()
    
    # 初始化音效
    sound_manager = SoundManager()
    
    # 显示开始界面
    # 绘制开始界面
    width, height = screen.get_size()
    for y in range(height):
        ratio = y / height
        r = int(20 * (1 - ratio) + 10 * ratio)
        g = int(20 * (1 - ratio) + 10 * ratio)
        b = int(40 * (1 - ratio) + 30 * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
    
    title = medium_font.render("TETRIS", True, (255, 215, 0))
    title_rect = title.get_rect(center=(width // 2, height // 3))
    screen.blit(title, title_rect)
    
    subtitle = font.render("Mobile Edition", True, (200, 200, 255))
    sub_rect = subtitle.get_rect(center=(width // 2, height // 3 + 50))
    screen.blit(subtitle, sub_rect)
    
    hint = small_font.render("Touch screen to start...", True, (100, 255, 100))
    hint_rect = hint.get_rect(center=(width // 2, height - 150))
    screen.blit(hint, hint_rect)
    
    # 显示虚拟按键说明
    controls = [
        "Controls:",
        "← → : Move",
        "↻ : Rotate",
        "↓ : Soft Drop",
        "⤓ : Hard Drop",
        "|| : Pause"
    ]
    y_pos = height // 2
    for text in controls:
        line = small_font.render(text, True, (200, 200, 200))
        line_rect = line.get_rect(center=(width // 2, y_pos))
        screen.blit(line, line_rect)
        y_pos += 28
    
    pygame.display.flip()
    
    # 等待触摸开始
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                waiting = False
        pygame.time.wait(50)
    
    # 开始背景音乐
    sound_manager.start_music()
    
    # 游戏主循环
    level = 1
    running = True
    total_score = 0
    
    while running and level <= 10:
        level_complete = start_game_mobile(screen, clock, font, small_font, level,
                                           medium_font, tiny_font, mobile_config, sound_manager)
        
        if level_complete:
            level += 1
        else:
            running = False
    
    # 停止音乐并显示游戏结束
    sound_manager.stop_music()
    display_game_over(screen, large_font, small_font, total_score, level)
    
    pygame.quit()


if __name__ == "__main__":
    main()
