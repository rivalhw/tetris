import random

# 定义所有方块形状和对应的颜色
shapes_colors = [
    ([[1, 1, 1, 1]], (0, 255, 255)),   # Cyan for I shape
    ([[1, 1], [1, 1]], (255, 255, 0)), # Yellow for O shape
    ([[1, 1, 0], [0, 1, 1]], (0, 0, 255)), # Blue for Z shape
    ([[0, 1, 1], [1, 1, 0]], (255, 0, 0)), # Red for S shape
    ([[1, 1, 1], [0, 1, 0]], (0, 255, 0)), # Green for T shape
    ([[1, 1, 1], [1, 0, 0]], (255, 165, 0)), # Orange for L shape
    ([[1, 1, 1], [0, 0, 1]], (128, 0, 128))  # Purple for J shape
]

def generate_new_block():
    shape, color = random.choice(shapes_colors)
    return shape, color


# 旋转方块
def rotate_block(block):
    return [list(row) for row in zip(*block[::-1])]
