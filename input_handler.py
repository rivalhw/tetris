import pygame

move_delay = 150  # 每次移动的时间间隔（毫秒）
last_move_time = 0  # 记录上次移动的时间

def handle_input():
    keys = pygame.key.get_pressed()
    move_x = 0
    rotate = False
    fast_drop = False

    if keys[pygame.K_LEFT]:
        move_x = -1
    elif keys[pygame.K_RIGHT]:
        move_x = 1
    if keys[pygame.K_UP]:
        rotate = True
    if keys[pygame.K_DOWN]:
        fast_drop = True

    return move_x, rotate, fast_drop
