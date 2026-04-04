#!/bin/bash
set -e

echo "========================================"
echo "Tetris Android 构建脚本"
echo "========================================"

# 获取项目路径（从命令行传入）
PROJECT_PATH="${1:-/mnt/c/git/tetris}"
cd "$PROJECT_PATH"

echo "项目路径: $PROJECT_PATH"

# 检查并安装依赖
echo ""
echo "检查依赖..."
if ! command -v buildozer &> /dev/null; then
    echo "安装 Buildozer..."
    sudo apt update
    sudo apt install -y python3-pip python3-venv git unzip openjdk-17-jdk \
        autoconf automake libtool pkg-config zlib1g-dev libncurses5-dev \
        cmake libffi-dev libssl-dev
    pip3 install --user buildozer cython
fi

echo ""
echo "准备移动端文件..."
# 备份原文件
[ -f main.py.bak ] || cp main.py main.py.bak
[ -f game_logic.py.bak ] || cp game_logic.py game_logic.py.bak
[ -f game_display.py.bak ] || cp game_display.py game_display.py.bak

# 使用移动端版本
cp main_mobile.py main.py
cp game_logic_mobile.py game_logic.py
cp game_display_mobile.py game_display.py

echo ""
echo "开始构建 APK..."
echo "注意：首次构建需要下载 Android SDK/NDK，可能需要 30-60 分钟"
echo "请保持网络连接..."
echo ""

# 构建 APK
if ! ~/.local/bin/buildozer android debug 2>&1; then
    echo ""
    echo "构建失败，尝试清理后重新构建..."
    ~/.local/bin/buildozer android clean
    ~/.local/bin/buildozer android debug 2>&1
fi

echo ""
echo "恢复原始文件..."
mv main.py.bak main.py
mv game_logic.py.bak game_logic.py
mv game_display.py.bak game_display.py

echo ""
echo "========================================"
echo "构建完成！"
echo "APK 位置: bin/tetris_mobile-1.0.0-*.apk"
echo "========================================"
