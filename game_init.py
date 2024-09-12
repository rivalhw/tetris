# 字体路径根据操作系统进行选择
import sys
import pygame


def load_fonts():
    if sys.platform.startswith("darwin"):  # MacOS
        font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    elif sys.platform.startswith("win"):  # Windows
        font_path = "C:/Windows/Fonts/simhei.ttf"  # 使用SimHei字体，支持中文
    else:
        font_path = None  # 其他系统不指定字体路径

    if font_path:
        font = pygame.font.Font(font_path, 36)
        small_font = pygame.font.Font(font_path, 18)  # 较小字体
        large_font = pygame.font.Font(font_path, 72)  # 大字体
        medium_font = pygame.font.Font(font_path, 48)  # 中等字体
    else:
        font = pygame.font.SysFont(None, 36)  # 使用默认系统字体
        small_font = pygame.font.SysFont(None, 18)  # 较小字体
        large_font = pygame.font.SysFont(None, 72)  # 大字体
        medium_font = pygame.font.SysFont(None, 48)  # 中等字体

    return font, small_font, large_font, medium_font



def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("大伟说AI：俄罗斯方块 - 10关挑战")
    
    font, small_font, large_font, medium_font = load_fonts()  # 加载所有需要的字体
    clock = pygame.time.Clock()
    return screen, clock, font
