import pygame
from game_init import load_fonts, calculate_window_size, GAME_CONFIG

# 颜色定义
COLORS = {
    'bg_top': (15, 15, 35),
    'bg_bottom': (5, 5, 20),
    'grid_line': (40, 40, 60),
    'border': (80, 80, 120),
    'border_glow': (120, 120, 180),
    'text_white': (255, 255, 255),
    'text_gold': (255, 215, 0),
    'text_cyan': (0, 255, 255),
    'panel_bg': (25, 25, 40, 220),
}


def draw_3d_block(surface, x, y, size, color, alpha=255):
    """绘制3D效果的方块"""
    temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 基础颜色
    base_color = color + (alpha,)
    
    # 高光颜色（更亮）
    highlight = tuple(min(255, c + 80) for c in color) + (alpha,)
    # 阴影颜色（更暗）
    shadow = tuple(max(0, c - 80) for c in color) + (alpha,)
    
    # 主方块
    pygame.draw.rect(temp_surface, base_color, (0, 0, size, size))
    
    # 高光（左上角）- 斜角效果
    points_high = [(0, 0), (size, 0), (size - 4, 4), (4, 4), (4, size - 4), (0, size)]
    pygame.draw.polygon(temp_surface, highlight, points_high)
    
    # 阴影（右下角）- 斜角效果
    points_shadow = [(size, size), (size, 0), (size - 4, 4), (size - 4, size - 4), (4, size - 4), (0, size)]
    pygame.draw.polygon(temp_surface, shadow, points_shadow)
    
    # 内芯（正常颜色）
    inner_size = size - 8
    pygame.draw.rect(temp_surface, base_color, (4, 4, inner_size, inner_size))
    
    # 内边框高光
    pygame.draw.rect(temp_surface, (255, 255, 255, 80), (4, 4, inner_size, inner_size), 1)
    
    surface.blit(temp_surface, (x, y))


def draw_gradient_background(screen, width, height):
    """绘制渐变背景"""
    # 基础渐变
    for y in range(height):
        ratio = y / height
        r = int(COLORS['bg_top'][0] * (1 - ratio) + COLORS['bg_bottom'][0] * ratio)
        g = int(COLORS['bg_top'][1] * (1 - ratio) + COLORS['bg_bottom'][1] * ratio)
        b = int(COLORS['bg_top'][2] * (1 - ratio) + COLORS['bg_bottom'][2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
    
    # 绘制星星
    star_positions = [(50, 40), (150, 80), (250, 50), (350, 90), (100, 120)]
    for i, (sx, sy) in enumerate(star_positions):
        brightness = 150 + (i * 20) % 105
        size = 1 + (i % 3)
        pygame.draw.circle(screen, (brightness, brightness, 220), (sx, sy), size)


def draw_game_board(screen, game_board, config, offset_x, offset_y):
    """绘制游戏棋盘"""
    cell_size = config['cell_size']
    rows = len(game_board)
    cols = len(game_board[0])
    
    board_width = cols * cell_size
    board_height = rows * cell_size
    
    # 绘制棋盘背景
    board_rect = pygame.Rect(offset_x - 4, offset_y - 4, board_width + 8, board_height + 8)
    pygame.draw.rect(screen, (15, 15, 25), board_rect, border_radius=4)
    pygame.draw.rect(screen, COLORS['border'], board_rect, 2, border_radius=4)
    
    # 绘制网格线
    for i in range(cols + 1):
        x = offset_x + i * cell_size
        pygame.draw.line(screen, COLORS['grid_line'], 
                        (x, offset_y), (x, offset_y + board_height), 1)
    
    for i in range(rows + 1):
        y = offset_y + i * cell_size
        pygame.draw.line(screen, COLORS['grid_line'], 
                        (offset_x, y), (offset_x + board_width, y), 1)
    
    # 绘制已固定的方块
    for y, row in enumerate(game_board):
        for x, cell in enumerate(row):
            if cell:
                draw_3d_block(screen, 
                            offset_x + x * cell_size, 
                            offset_y + y * cell_size, 
                            cell_size, cell)


def draw_current_block(screen, block, block_x, block_y, color, config, offset_x, offset_y):
    """绘制当前移动的方块"""
    cell_size = config['cell_size']
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                draw_3d_block(screen,
                            offset_x + (block_x + x) * cell_size,
                            offset_y + (block_y + y) * cell_size,
                            cell_size, color)


def draw_ghost_block(screen, block, block_x, drop_y, color, config, offset_x, offset_y):
    """绘制方块落点预览"""
    cell_size = config['cell_size']
    ghost_color = tuple(max(0, min(255, c // 4 + 30)) for c in color)
    
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    offset_x + (block_x + x) * cell_size + 2,
                    offset_y + (drop_y + y) * cell_size + 2,
                    cell_size - 4, cell_size - 4)
                pygame.draw.rect(screen, ghost_color, rect, border_radius=3)
                pygame.draw.rect(screen, ghost_color + (150,), rect, 2, border_radius=3)


def draw_next_block_preview(screen, next_block, next_color, font, config, sidebar_x, start_y):
    """绘制下一个方块预览"""
    cell_size = 24
    panel_width = 100
    panel_height = 80
    
    # 预览面板背景
    panel_rect = pygame.Rect(sidebar_x, start_y, panel_width, panel_height)
    pygame.draw.rect(screen, (25, 25, 40), panel_rect, border_radius=6)
    pygame.draw.rect(screen, COLORS['border'], panel_rect, 2, border_radius=6)
    
    # 标题
    title = font.render("NEXT", True, COLORS['text_gold'])
    screen.blit(title, (sidebar_x + 5, start_y + 3))
    
    # 计算居中位置
    if next_block:
        block_width = len(next_block[0]) * cell_size
        block_height = len(next_block) * cell_size
        start_x = sidebar_x + (panel_width - block_width) // 2
        block_y = start_y + 28 + (panel_height - 28 - block_height) // 2
        
        for y, row in enumerate(next_block):
            for x, cell in enumerate(row):
                if cell:
                    draw_3d_block(screen,
                                start_x + x * cell_size,
                                block_y + y * cell_size,
                                cell_size, next_color)


def draw_ui_panel(screen, score, elapsed_time, level, lines_cleared, lines_needed,
                 font, small_font, sidebar_x, start_y):
    """绘制UI信息面板"""
    panel_width = 100
    
    panel_items = [
        ("LV", level, COLORS['text_gold']),
        ("SC", score, COLORS['text_cyan']),
        ("LI", f"{lines_cleared}/{lines_needed}", COLORS['text_white'])
    ]
    
    y_pos = start_y
    for label, value, color in panel_items:
        # 标签
        label_text = small_font.render(label, True, (150, 150, 170))
        screen.blit(label_text, (sidebar_x, y_pos))
        
        # 值
        value_text = font.render(str(value), True, color)
        screen.blit(value_text, (sidebar_x, y_pos + 16))
        
        y_pos += 50


def draw_pause_overlay(screen, font, small_font, width, height):
    """绘制暂停遮罩"""
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    pause_text = font.render("PAUSED", True, COLORS['text_gold'])
    text_rect = pause_text.get_rect(center=(width // 2, height // 2 - 20))
    screen.blit(pause_text, text_rect)
    
    hint_text = small_font.render("Touch || to continue", True, (200, 200, 200))
    hint_rect = hint_text.get_rect(center=(width // 2, height // 2 + 20))
    screen.blit(hint_text, hint_rect)


def draw_game(screen, block, block_x, block_y, color, game_board, score, 
              elapsed_time, level, small_font, font, medium_font, config,
              next_block=None, next_color=None, ghost_y=None, 
              lines_cleared=0, lines_needed=10, buttons=None, pause_button=None):
    """主绘制函数 - 移动端"""
    width, height = screen.get_size()
    
    # 计算布局
    padding = 20
    cell_size = config['cell_size']
    board_width = config['board_cols'] * cell_size
    
    # 棋盘位置（偏左）
    board_x = padding
    board_y = padding + 50
    
    # 侧边栏位置
    sidebar_x = board_x + board_width + 15
    
    # 绘制背景
    draw_gradient_background(screen, width, height)
    
    # 绘制标题
    title = medium_font.render("TETRIS", True, COLORS['text_gold'])
    screen.blit(title, (board_x, 10))
    
    # 绘制游戏棋盘
    draw_game_board(screen, game_board, config, board_x, board_y)
    
    # 绘制幽灵方块
    if ghost_y is not None:
        draw_ghost_block(screen, block, block_x, ghost_y, color, config, board_x, board_y)
    
    # 绘制当前方块
    draw_current_block(screen, block, block_x, block_y, color, config, board_x, board_y)
    
    # 绘制下一个方块预览
    if next_block and next_color:
        draw_next_block_preview(screen, next_block, next_color, small_font, config, sidebar_x, board_y)
    
    # 绘制UI面板
    draw_ui_panel(screen, score, elapsed_time, level, lines_cleared, lines_needed,
                  font, small_font, sidebar_x, board_y + 90)
    
    # 绘制虚拟按键
    if buttons:
        for button in buttons.values():
            button.draw(screen)
    
    # 绘制暂停按钮
    if pause_button:
        pause_button.draw(screen)


def display_game_over(screen, font, small_font, score=0, level=0):
    """显示游戏结束画面"""
    width, height = screen.get_size()
    
    for y in range(height):
        ratio = y / height
        color = (int(40 * (1 - ratio) + 10 * ratio),
                int(20 * (1 - ratio) + 10 * ratio),
                int(20 * (1 - ratio) + 20 * ratio))
        pygame.draw.line(screen, color, (0, y), (width, y))
    
    game_over_text = font.render("GAME OVER", True, (255, 80, 80))
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 60))
    screen.blit(game_over_text, text_rect)
    
    score_text = small_font.render(f"Score: {score}", True, (255, 215, 0))
    score_rect = score_text.get_rect(center=(width // 2, height // 2))
    screen.blit(score_text, score_rect)
    
    level_text = small_font.render(f"Level: {level}", True, (255, 255, 255))
    level_rect = level_text.get_rect(center=(width // 2, height // 2 + 40))
    screen.blit(level_text, level_rect)
    
    pygame.display.flip()
    pygame.time.wait(3000)


def display_level_complete(screen, font, small_font, level):
    """显示关卡完成画面"""
    width, height = screen.get_size()
    
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 100, 0, 180))
    screen.blit(overlay, (0, 0))
    
    congrats_text = font.render("LEVEL CLEAR!", True, (100, 255, 100))
    text_rect = congrats_text.get_rect(center=(width // 2, height // 2 - 30))
    screen.blit(congrats_text, text_rect)
    
    next_level_text = small_font.render(f"Next: {level + 1}", True, (255, 255, 255))
    next_rect = next_level_text.get_rect(center=(width // 2, height // 2 + 20))
    screen.blit(next_level_text, next_rect)
    
    pygame.display.flip()
    pygame.time.wait(2000)
