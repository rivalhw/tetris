import sys
import pygame
from blocks import generate_new_block, rotate_block
from game_display_mobile import draw_game, display_game_over, display_level_complete, draw_pause_overlay
from sound_manager import SoundManager


def check_collision(block, block_x, block_y, game_board):
    """检查方块是否碰撞"""
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                if (block_x + x < 0 or block_x + x >= len(game_board[0]) or
                        block_y + y >= len(game_board) or
                        (block_y + y >= 0 and game_board[block_y + y][block_x + x])):
                    return True
    return False


def get_ghost_position(block, block_x, block_y, game_board):
    """获取方块落点位置"""
    ghost_y = block_y
    while not check_collision(block, block_x, ghost_y + 1, game_board):
        ghost_y += 1
    return ghost_y


def clear_full_lines(game_board):
    """清除满行"""
    new_board = [row for row in game_board if any(cell == 0 for cell in row)]
    cleared_lines = len(game_board) - len(new_board)
    new_board = [[0] * len(game_board[0]) for _ in range(cleared_lines)] + new_board
    return new_board, cleared_lines


class TouchButton:
    """触摸按钮类"""
    def __init__(self, x, y, width, height, text, color=(60, 60, 80), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.pressed = False
        self.font = pygame.font.SysFont(None, 28)
    
    def draw(self, screen):
        # 绘制按钮背景
        color = tuple(min(255, c + 40) for c in self.color) if self.pressed else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (150, 150, 180), self.rect, 2, border_radius=8)
        
        # 绘制文字
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_touch(self, pos, touch_down):
        """处理触摸事件"""
        was_pressed = self.pressed
        if touch_down and self.rect.collidepoint(pos):
            self.pressed = True
            return True
        else:
            self.pressed = False
        return False


def start_game_mobile(screen, clock, font, small_font, level, medium_font, tiny_font, config, sound_manager=None):
    """移动端游戏主循环"""
    if sound_manager is None:
        sound_manager = SoundManager()
    
    # 初始化游戏状态
    block, color = generate_new_block()
    next_block, next_color = generate_new_block()
    block_x, block_y = 4, 0
    game_over = False
    drop_speed = max(50, 500 - (level * 40))
    last_drop_time = pygame.time.get_ticks()
    score = 0
    start_time = pygame.time.get_ticks()
    paused = False
    lines_cleared_in_level = 0
    lines_needed_for_level_up = 10
    
    game_board = [[0] * config['board_cols'] for _ in range(config['board_rows'])]
    
    # 获取屏幕尺寸
    screen_width, screen_height = screen.get_size()
    
    # 创建虚拟按键（放在屏幕底部）
    button_size = 70
    button_y = screen_height - 100
    spacing = 10
    
    # 计算按钮布局（底部居中排列）
    total_width = button_size * 5 + spacing * 4
    start_x = (screen_width - total_width) // 2
    
    buttons = {
        'left': TouchButton(start_x, button_y, button_size, button_size, "←"),
        'right': TouchButton(start_x + button_size + spacing, button_y, button_size, button_size, "→"),
        'rotate': TouchButton(start_x + (button_size + spacing) * 2, button_y, button_size, button_size, "↻"),
        'down': TouchButton(start_x + (button_size + spacing) * 3, button_y, button_size, button_size, "↓"),
        'drop': TouchButton(start_x + (button_size + spacing) * 4, button_y, button_size, button_size, "⤓", (80, 60, 60)),
    }
    
    # 暂停按钮（右上角）
    pause_button = TouchButton(screen_width - 60, 10, 50, 40, "||", (60, 60, 80))
    
    while not game_over:
        current_time = pygame.time.get_ticks()
        move_x = 0
        rotate = False
        fast_drop = False
        hard_drop = False
        touch_down = False
        touch_pos = (0, 0)
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_manager.stop_music()
                pygame.quit()
                sys.exit()
            
            # 触摸事件
            elif event.type == pygame.FINGERDOWN:
                touch_down = True
                touch_pos = (int(event.x * screen_width), int(event.y * screen_height))
            
            elif event.type == pygame.FINGERUP:
                touch_down = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                touch_down = True
                touch_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                touch_down = False
            
            # 键盘事件（保留键盘支持）
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound_manager.stop_music()
                    pygame.quit()
                    sys.exit()
                
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        sound_manager.stop_music()
                    else:
                        sound_manager.start_music()
                
                elif event.key == pygame.K_UP:
                    rotate = True
                
                elif event.key == pygame.K_DOWN:
                    fast_drop = True
                
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    hard_drop = True
                
                elif event.key == pygame.K_LEFT:
                    move_x = -1
                
                elif event.key == pygame.K_RIGHT:
                    move_x = 1
        
        # 处理触摸按钮
        if not paused:
            if buttons['left'].handle_touch(touch_pos, touch_down):
                move_x = -1
            if buttons['right'].handle_touch(touch_pos, touch_down):
                move_x = 1
            if buttons['rotate'].handle_touch(touch_pos, touch_down):
                rotate = True
            if buttons['down'].handle_touch(touch_pos, touch_down):
                fast_drop = True
            if buttons['drop'].handle_touch(touch_pos, touch_down):
                hard_drop = True
        
        # 暂停按钮
        if pause_button.handle_touch(touch_pos, touch_down):
            paused = not paused
            if paused:
                sound_manager.stop_music()
            else:
                sound_manager.start_music()
            pygame.time.wait(200)  # 防止快速连点
        
        # 处理暂停状态
        if paused:
            width, height = screen.get_size()
            draw_pause_overlay(screen, font, small_font, width, height)
            pygame.display.flip()
            clock.tick(30)
            continue
        
        # 检查游戏结束
        if any(game_board[0]):
            sound_manager.play_game_over()
            width, height = screen.get_size()
            display_game_over(screen, font, small_font, score, level)
            return False
        
        # 移动方块
        if move_x != 0:
            new_x = block_x + move_x
            if not check_collision(block, new_x, block_y, game_board):
                block_x = new_x
                sound_manager.play_move()
        
        # 旋转方块
        if rotate:
            rotated_block = rotate_block(block)
            if not check_collision(rotated_block, block_x, block_y, game_board):
                block = rotated_block
                sound_manager.play_rotate()
            else:
                # 尝试踢墙旋转
                kicks = [-1, 1, -2, 2]
                for kick in kicks:
                    if not check_collision(rotated_block, block_x + kick, block_y, game_board):
                        block_x += kick
                        block = rotated_block
                        sound_manager.play_rotate()
                        break
        
        # 硬降
        if hard_drop:
            while not check_collision(block, block_x, block_y + 1, game_board):
                block_y += 1
                score += 2
            sound_manager.play_drop()
        
        # 方块下落
        current_drop_speed = 50 if fast_drop else drop_speed
        if current_time - last_drop_time > current_drop_speed:
            new_y = block_y + 1
            if not check_collision(block, block_x, new_y, game_board):
                block_y = new_y
                if fast_drop:
                    score += 1
            else:
                # 锁定方块到棋盘
                sound_manager.play_drop()
                for y, row in enumerate(block):
                    for x, cell in enumerate(row):
                        if cell:
                            game_board[block_y + y][block_x + x] = color
                
                # 生成新方块
                block, color = next_block, next_color
                next_block, next_color = generate_new_block()
                block_x, block_y = 4, 0
                
                if check_collision(block, block_x, block_y, game_board):
                    game_over = True
                    sound_manager.play_game_over()
                    display_game_over(screen, font, small_font, score, level)
                    return False
                
                # 清除满行
                game_board, cleared_lines = clear_full_lines(game_board)
                if cleared_lines > 0:
                    line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
                    score += line_scores.get(cleared_lines, cleared_lines * 100) * level
                    lines_cleared_in_level += cleared_lines
                    sound_manager.play_clear(cleared_lines)
            
            last_drop_time = current_time
        
        # 检查是否完成当前关卡
        if lines_cleared_in_level >= lines_needed_for_level_up:
            sound_manager.play_level_up()
            width, height = screen.get_size()
            display_level_complete(screen, font, small_font, level)
            return True
        
        # 计算已玩时长
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        
        # 获取幽灵方块位置
        ghost_y = get_ghost_position(block, block_x, block_y, game_board)
        
        # 绘制游戏
        draw_game(screen, block, block_x, block_y, color, game_board, score,
                 elapsed_time, level, small_font, font, medium_font, config,
                 next_block, next_color, ghost_y, lines_cleared_in_level, lines_needed_for_level_up,
                 buttons, pause_button)
        
        pygame.display.flip()
        clock.tick(60)
    
    return False
