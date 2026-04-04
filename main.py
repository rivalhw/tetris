import pygame
from game_init import initialize_game, show_start_screen
from game_logic import start_game
from game_display import display_game_over
from sound_manager import SoundManager


def main():
    # 初始化游戏
    screen, clock, font, small_font, large_font, medium_font, tiny_font, config = initialize_game()
    
    # 初始化音效管理器
    sound_manager = SoundManager()
    
    # 显示开始界面
    show_start_screen(screen, font, medium_font, small_font)
    
    # 开始背景音乐
    sound_manager.start_music()
    
    # 游戏主循环
    level = 1
    running = True
    total_score = 0
    
    while running and level <= 10:
        # 开始当前关卡
        level_complete = start_game(screen, clock, font, small_font, level, 
                                     medium_font, tiny_font, config, sound_manager)
        
        if level_complete:
            level += 1
        else:
            running = False
    
    # 停止音乐并显示游戏结束
    sound_manager.stop_music()
    display_game_over(screen, large_font, small_font, total_score, level)
    
    # 清理
    pygame.quit()


if __name__ == "__main__":
    main()
