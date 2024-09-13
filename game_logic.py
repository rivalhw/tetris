import sys
import pygame
from blocks import generate_new_block, rotate_block
from game_display import draw_game, display_game_over

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

def start_game(screen, clock, font, small_font, level):
    block, color = generate_new_block()
    block_x, block_y = 4, 0
    game_over = False
    drop_speed = max(50, 500 - (level * 40))  # 最小速度为50
    last_drop_time = pygame.time.get_ticks()
    score = 0
    start_time = pygame.time.get_ticks()
    paused = False
    lines_cleared_in_level = 0
    lines_needed_for_level_up = 10

    game_board = [[0] * 10 for _ in range(20)]

    while not game_over:
        move_x = 0
        rotate = False
        fast_drop = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    paused = not paused  # 切换暂停状态
                elif not paused:
                    if event.key == pygame.K_LEFT:
                        move_x = -1
                    elif event.key == pygame.K_RIGHT:
                        move_x = 1
                    elif event.key == pygame.K_UP:
                        rotate = True
                    elif event.key == pygame.K_DOWN:
                        fast_drop = True

        if paused:
            # 显示“游戏暂停”文本
            pause_text = font.render("游戏暂停", True, (255, 255, 255))
            screen.blit(pause_text, (80, 250))
            pygame.display.flip()
            clock.tick(5)  # 控制暂停时的帧率
            continue  # 跳过本次循环

        if any(game_board[0]):
            display_game_over(screen, font)
            return False

        # 移动方块
        new_x = block_x + move_x
        if not check_collision(block, new_x, block_y, game_board):
            block_x = new_x

        # 旋转方块
        if rotate:
            rotated_block = rotate_block(block)
            if not check_collision(rotated_block, block_x, block_y, game_board):
                block = rotated_block
            else:
                # 尝试调整位置再旋转
                if not check_collision(rotated_block, block_x - 1, block_y, game_board):
                    block_x -= 1
                    block = rotated_block
                elif not check_collision(rotated_block, block_x + 1, block_y, game_board):
                    block_x += 1
                    block = rotated_block

        # 方块下落
        current_time = pygame.time.get_ticks()
        if current_time - last_drop_time > (drop_speed if not fast_drop else 50):
            new_y = block_y + 1
            if not check_collision(block, block_x, new_y, game_board):
                block_y = new_y
            else:
                # 锁定方块到棋盘
                for y, row in enumerate(block):
                    for x, cell in enumerate(row):
                        if cell:
                            game_board[block_y + y][block_x + x] = color
                block, color = generate_new_block()
                block_x, block_y = 4, 0
                if check_collision(block, block_x, block_y, game_board):
                    game_over = True
                game_board, cleared_lines = clear_full_lines(game_board)
                if cleared_lines > 0:
                    score += cleared_lines * 10
                    lines_cleared_in_level += cleared_lines

            last_drop_time = current_time

        # 检查是否完成当前关卡
        if lines_cleared_in_level >= lines_needed_for_level_up:
            return True

        # 计算已玩时长
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # 绘制游戏
        draw_game(screen, block, block_x, block_y, color, game_board, score, elapsed_time, level, small_font)
        pygame.display.flip()

        clock.tick(60)

    return False
