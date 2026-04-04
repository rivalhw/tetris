import random

# 定义所有方块形状和对应的颜色
# 使用更鲜艳的颜色，并添加发光效果的配色
shapes_colors = [
    ([[1, 1, 1, 1]], (0, 255, 255)),      # I形状 - 青色
    ([[1, 1], [1, 1]], (255, 255, 0)),     # O形状 - 黄色
    ([[1, 1, 0], [0, 1, 1]], (255, 0, 0)), # Z形状 - 红色
    ([[0, 1, 1], [1, 1, 0]], (0, 255, 0)), # S形状 - 绿色
    ([[1, 1, 1], [0, 1, 0]], (128, 0, 255)), # T形状 - 紫色
    ([[1, 1, 1], [1, 0, 0]], (255, 165, 0)), # L形状 - 橙色
    ([[1, 1, 1], [0, 0, 1]], (0, 100, 255))  # J形状 - 蓝色
]

# 方块名称，用于显示
shape_names = ['I', 'O', 'Z', 'S', 'T', 'L', 'J']


def generate_new_block():
    shape, color = random.choice(shapes_colors)
    return shape, color


def generate_specific_block(index):
    """生成指定类型的方块"""
    shape, color = shapes_colors[index % len(shapes_colors)]
    return shape, color


def rotate_block(block):
    return [list(row) for row in zip(*block[::-1])]  # 顺时针旋转90度


def get_block_preview(block, color, size=25):
    """获取方块预览图像的描述"""
    return {
        'shape': block,
        'color': color,
        'width': len(block[0]) * size,
        'height': len(block) * size
    }
