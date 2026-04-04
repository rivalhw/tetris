"""
Android APK 打包辅助脚本
在 Windows 上可以通过以下方式打包：

方法1: 使用 WSL + Buildozer
方法2: 使用 Docker
方法3: 在线打包服务
"""
import os
import sys
import subprocess


def check_wsl():
    """检查 WSL 是否可用"""
    try:
        result = subprocess.run(['wsl', '--list'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def install_wsl():
    """安装 WSL"""
    print("正在安装 WSL...")
    subprocess.run(['wsl', '--install', '-d', 'Ubuntu'], check=False)
    print("WSL 安装完成，请重启电脑后再次运行此脚本")


def setup_buildozer():
    """在 WSL 中设置 Buildozer 环境"""
    setup_script = '''
#!/bin/bash
set -e

echo "更新软件包列表..."
sudo apt update

echo "安装依赖..."
sudo apt install -y python3-pip python3-venv git unzip openjdk-17-jdk \
    autoconf automake libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

echo "安装 Buildozer..."
pip3 install --user buildozer cython

echo "环境设置完成！"
'''
    with open('setup_wsl.sh', 'w') as f:
        f.write(setup_script)
    
    print("在 WSL 中运行设置脚本...")
    subprocess.run(['wsl', 'bash', 'setup_wsl.sh'])


def build_apk():
    """构建 APK"""
    # 复制移动端文件为主入口
    build_script = '''
#!/bin/bash
set -e

cd /mnt/{drive}/git/tetris

# 备份原文件
cp main.py main.py.bak
cp game_logic.py game_logic.py.bak
cp game_display.py game_display.py.bak

# 使用移动端版本
cp main_mobile.py main.py
cp game_logic_mobile.py game_logic.py
cp game_display_mobile.py game_display.py

echo "开始构建 APK..."
~/.local/bin/buildozer android debug

# 恢复原文件
mv main.py.bak main.py
mv game_logic.py.bak game_logic.py
mv game_display.py.bak game_display.py

echo "构建完成！APK 位于 bin/ 目录"
'''.format(drive=os.path.splitdrive(os.getcwd())[0].replace(':', '').lower())
    
    with open('build_apk.sh', 'w') as f:
        f.write(build_script)
    
    print("开始构建 APK...")
    subprocess.run(['wsl', 'bash', 'build_apk.sh'])


def main():
    print("=" * 50)
    print("Tetris Android 打包工具")
    print("=" * 50)
    
    if not check_wsl():
        print("WSL 未安装。")
        choice = input("是否安装 WSL? (y/n): ")
        if choice.lower() == 'y':
            install_wsl()
        else:
            print("请手动安装 WSL 或使用其他打包方式")
            return
    
    print("\n选择操作:")
    print("1. 设置 Buildozer 环境")
    print("2. 构建 APK")
    print("3. 完整流程（设置+构建）")
    
    choice = input("\n请输入选项 (1-3): ")
    
    if choice == '1':
        setup_buildozer()
    elif choice == '2':
        build_apk()
    elif choice == '3':
        setup_buildozer()
        build_apk()
    else:
        print("无效选项")


if __name__ == '__main__':
    main()
