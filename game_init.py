import sys
import pygame

def load_fonts():
    if sys.platform.startswith("darwin"):  # MacOS
        font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    elif sys.platform.startswith("win"):  # Windows
        font_path = "C:/Windows/Fonts/simhei.ttf"
    else:
        font_path = None  # 其他系统不指定字体路径

    if font_path:
        font = pygame.font.Font(font_path, 36)
        small_font = pygame.font.Font(font_path, 18)
        large_font = pygame.font.Font(font_path, 72)
        medium_font = pygame.font.Font(font_path, 48)
    else:
        font = pygame.font.SysFont(None, 36)
        small_font = pygame.font.SysFont(None, 18)
        large_font = pygame.font.SysFont(None, 72)
        medium_font = pygame.font.SysFont(None, 48)

    return font, small_font, large_font, medium_font

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("大伟说AI：俄罗斯方块 - 过关挑战")

    font, small_font, large_font, medium_font = load_fonts()
    clock = pygame.time.Clock()
    return screen, clock, font, small_font, large_font, medium_font
