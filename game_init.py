import sys
import os
import pygame


def find_chinese_font():
    """查找系统中可用的中文字体"""
    # Windows 常见中文字体路径
    windows_fonts = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/simkai.ttf",
        "C:/Windows/Fonts/simfang.ttf",
    ]
    
    # MacOS 常见中文字体路径
    mac_fonts = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    
    # Linux 常见中文字体路径
    linux_fonts = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    
    if sys.platform.startswith("win"):
        font_list = windows_fonts
    elif sys.platform.startswith("darwin"):
        font_list = mac_fonts
    else:
        font_list = linux_fonts
    
    # 检查字体文件是否存在且可用
    for font_path in font_list:
        if os.path.exists(font_path):
            try:
                test_font = pygame.font.Font(font_path, 20)
                # 测试渲染中文字符
                test_surface = test_font.render("测试", True, (255, 255, 255))
                if test_surface.get_width() > 10:  # 确保渲染成功
                    return font_path
            except:
                continue
    
    return None


def load_fonts():
    """加载游戏字体"""
    # 尝试找到中文字体
    chinese_font_path = find_chinese_font()
    
    if chinese_font_path:
        try:
            font = pygame.font.Font(chinese_font_path, 32)
            small_font = pygame.font.Font(chinese_font_path, 20)
            large_font = pygame.font.Font(chinese_font_path, 64)
            medium_font = pygame.font.Font(chinese_font_path, 48)
            tiny_font = pygame.font.Font(chinese_font_path, 16)
            return font, small_font, large_font, medium_font, tiny_font
        except:
            pass
    
    # 回退到系统字体
    try:
        font = pygame.font.SysFont("microsoftyahei", 32)
        small_font = pygame.font.SysFont("microsoftyahei", 20)
        large_font = pygame.font.SysFont("microsoftyahei", 64)
        medium_font = pygame.font.SysFont("microsoftyahei", 48)
        tiny_font = pygame.font.SysFont("microsoftyahei", 16)
    except:
        font = pygame.font.SysFont(None, 36)
        small_font = pygame.font.SysFont(None, 24)
        large_font = pygame.font.SysFont(None, 72)
        medium_font = pygame.font.SysFont(None, 48)
        tiny_font = pygame.font.SysFont(None, 18)
    
    return font, small_font, large_font, medium_font, tiny_font


# 全局配置
GAME_CONFIG = {
    'cell_size': 32,           # 每个格子的大小
    'board_cols': 10,          # 棋盘列数
    'board_rows': 20,          # 棋盘行数
    'sidebar_width': 200,      # 侧边栏宽度
    'padding': 40,             # 边距
}


def calculate_window_size():
    """计算窗口大小"""
    cfg = GAME_CONFIG
    board_width = cfg['board_cols'] * cfg['cell_size'] + cfg['padding'] * 2
    board_height = cfg['board_rows'] * cfg['cell_size'] + cfg['padding'] * 2
    
    # 确保窗口足够高
    if board_height < 700:
        board_height = 700
    
    window_width = board_width + cfg['sidebar_width']
    window_height = board_height
    
    return window_width, window_height, board_width, board_height


def initialize_game():
    """初始化游戏"""
    pygame.init()
    
    # 计算窗口大小
    window_width, window_height, board_width, board_height = calculate_window_size()
    
    # 设置窗口大小
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("俄罗斯方块 - 经典升级版")
    
    # 加载字体
    font, small_font, large_font, medium_font, tiny_font = load_fonts()
    
    # 创建时钟
    clock = pygame.time.Clock()
    
    # 设置窗口图标
    try:
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        colors = [(0, 255, 255), (255, 255, 0), (255, 0, 0), (0, 255, 0)]
        for i, color in enumerate(colors):
            pygame.draw.rect(icon, color, ((i % 2) * 16, (i // 2) * 16, 14, 14))
        pygame.display.set_icon(icon)
    except:
        pass
    
    return screen, clock, font, small_font, large_font, medium_font, tiny_font, GAME_CONFIG


def show_start_screen(screen, font, medium_font, small_font):
    """显示开始界面"""
    width, height = screen.get_size()
    
    # 渐变背景
    for y in range(height):
        ratio = y / height
        r = int(20 * (1 - ratio) + 10 * ratio)
        g = int(20 * (1 - ratio) + 10 * ratio)
        b = int(40 * (1 - ratio) + 30 * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
    
    # 标题 - 使用英文避免字体问题
    title = medium_font.render("TETRIS", True, (255, 215, 0))
    title_rect = title.get_rect(center=(width // 2, height // 3))
    screen.blit(title, title_rect)
    
    # 副标题
    subtitle = font.render("俄罗斯方块", True, (200, 200, 255))
    sub_rect = subtitle.get_rect(center=(width // 2, height // 3 + 60))
    screen.blit(subtitle, sub_rect)
    
    # 操作说明
    instructions = [
        "Controls:",
        "Left/Right  Move",
        "Up          Rotate",
        "Down        Soft Drop",
        "Shift       Hard Drop",
        "Space       Pause",
        "ESC         Exit"
    ]
    
    y_pos = height // 2
    for i, text in enumerate(instructions):
        if i == 0:
            line = small_font.render(text, True, (255, 215, 0))
        else:
            line = small_font.render(text, True, (200, 200, 200))
        line_rect = line.get_rect(center=(width // 2, y_pos))
        screen.blit(line, line_rect)
        y_pos += 32
    
    # 提示
    hint = small_font.render("Press any key to start...", True, (100, 255, 100))
    hint_rect = hint.get_rect(center=(width // 2, height - 100))
    screen.blit(hint, hint_rect)
    
    pygame.display.flip()
    
    # 等待按键
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                waiting = False
        pygame.time.wait(50)
