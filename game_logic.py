# game_logic.py
import pygame
from blocks import generate_new_block, rotate_block
from game_display import draw_game
from game_display import display_game_over  # 导入游戏结束显示函数

# 检查方块是否超出边界或与其他方块发生冲突
def check_collision(block, block_x, block_y, game_board):
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                if (block_x + x < 0 or block_x + x >= len(game_board[0]) or
                        block_y + y >= len(game_board) or
                        game_board[block_y + y][block_x + x]):
                    return True
    return False

def clear_full_lines(game_board):
    new_board = [row for row in game_board if any(cell == 0 for cell in row)]
    cleared_lines = len(game_board) - len(new_board)
    new_board = [[0] * len(game_board[0]) for _ in range(cleared_lines)] + new_board
    return new_board, cleared_lines

def start_game(screen, clock, font, level):
    block, color = generate_new_block()  # 生成方块
    block_x, block_y = 4, 0  # 方块初始位置
    game_over = False
    drop_speed = 500 - (level * 40)  # 随着关卡提升，方块下落速度增加
    last_drop_time = pygame.time.get_ticks()

    game_board = [[0] * 10 for _ in range(20)]  # 创建游戏的10x20棋盘

    # 游戏主循环
    while not game_over:
        move_x = 0
        rotate = False
        fast_drop = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_x = -1
                elif event.key == pygame.K_RIGHT:
                    move_x = 1
                elif event.key == pygame.K_UP:
                    rotate = True
                elif event.key == pygame.K_DOWN:
                    fast_drop = True

        # 检查游戏是否满了
        if any(game_board[0]):  # 第一行有方块表示满了
            display_game_over(screen)
            return False  # 结束游戏

        # 尝试移动方块
        new_x = block_x + move_x
        if not check_collision(block, new_x, block_y, game_board):
            block_x = new_x

        # 旋转方块
        if rotate:
            rotated_block = rotate_block(block)
            # 检查旋转后的方块是否会超出边界或碰撞
            if not check_collision(rotated_block, block_x, block_y, game_board):
                block = rotated_block
            else:
                # 尝试左移一格再旋转
                if not check_collision(rotated_block, block_x - 1, block_y, game_board):
                    block_x -= 1
                    block = rotated_block
                # 尝试右移一格再旋转
                elif not check_collision(rotated_block, block_x + 1, block_y, game_board):
                    block_x += 1
                    block = rotated_block

        # 方块下落逻辑
        current_time = pygame.time.get_ticks()
        if current_time - last_drop_time > (drop_speed if not fast_drop else 50):
            new_y = block_y + 1
            if not check_collision(block, block_x, new_y, game_board):
                block_y = new_y
            else:
                # 方块到底，锁定方块到棋盘
                for y, row in enumerate(block):
                    for x, cell in enumerate(row):
                        if cell:
                            game_board[block_y + y][block_x + x] = color
                block, color = generate_new_block()
                block_x, block_y = 4, 0
                if check_collision(block, block_x, block_y, game_board):
                    game_over = True  # 无法生成新的方块，游戏结束
                game_board, _ = clear_full_lines(game_board)  # 清除已填满的行

            last_drop_time = current_time

        # 绘制游戏
        draw_game(screen, block, block_x, block_y, color, game_board)
        pygame.display.flip()

        # 更新每帧
        clock.tick(60)  # 增加帧率，提高流畅性

    return True
