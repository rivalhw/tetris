import random

# 定义所有方块形状和对应的颜色
# blocks.py
shapes_colors = [
    ([[1, 1, 1, 1]], (173, 216, 230)),   # I形状使用浅蓝色
    ([[1, 1], [1, 1]], (255, 223, 186)), # O形状使用浅黄色
    ([[1, 1, 0], [0, 1, 1]], (100, 149, 237)), # Z形状使用浅蓝色
    ([[0, 1, 1], [1, 1, 0]], (240, 128, 128)), # S形状使用浅红色
    ([[1, 1, 1], [0, 1, 0]], (144, 238, 144)), # T形状使用浅绿色
    ([[1, 1, 1], [1, 0, 0]], (255, 165, 0)),   # L形状使用橙色
    ([[1, 1, 1], [0, 0, 1]], (221, 160, 221))  # J形状使用紫色
]


def generate_new_block():
    shape, color = random.choice(shapes_colors)
    return shape, color

# blocks.py
def rotate_block(block):
    return [list(row) for row in zip(*block[::-1])]  # 顺时针旋转90度

