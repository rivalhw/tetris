# 🎮 俄罗斯方块 Tetris

一个功能完善、界面美观的俄罗斯方块游戏，支持 PC 和 Android 双平台。

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-PC%20%7C%20Android-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.8+-orange.svg)

---

## 📸 游戏截图

### PC 版本
[![PC Version](https://i.postimg.cc/qqwcjG7b/V1-0.png)](https://postimg.cc/LgqZsLLL)

### 移动端版本
支持触屏虚拟按键控制

---

## ✨ 功能特性

### 🎨 精美界面
- **3D 立体方块** - 带高光和阴影效果的方块
- **渐变星空背景** - 动态渐变背景配闪烁星星
- **幽灵方块预览** - 显示方块落点位置
- **下一个方块预览** - 提前预知即将出现的方块

### 🎵 丰富音效
- **背景音乐** - 电子风格循环节拍
- **移动音效** - 清脆短音
- **旋转音效** - 滑音效果
- **消行音效** - C大调和弦琶音
- **升级音效** - 胜利号角
- **游戏结束音效** - 悲伤下降音

### 🎮 游戏玩法
- 10 个关卡，难度递增
- 消行升级机制
- 分数系统（支持连消奖励）
- 关卡完成动画
- 暂停功能

### 📱 双平台支持
- **PC 版本** - 键盘控制，600x720 窗口
- **Android 版本** - 触屏控制，虚拟按键

---

## 🚀 快速开始

### PC 版本

#### 方式 1：直接运行（需要 Python）
```bash
# 克隆仓库
git clone https://github.com/rivalhw/tetris.git
cd tetris

# 安装依赖
pip install pygame

# 运行游戏
python main.py
```

#### 方式 2：Windows 可执行文件
下载 `dist/Tetris_PC.exe`，双击即可运行，无需安装 Python。

### Android 版本

#### 方式 1：Pydroid 3（最简单）
1. 在手机应用商店安装 **Pydroid 3**
2. 打开 Pydroid 3 → 菜单 → Pip → 安装 `pygame`
3. 将项目文件复制到手机
4. 打开 `main_mobile.py` 运行

#### 方式 2：构建 APK
运行构建脚本：
```powershell
# 右键以管理员身份运行
.\build_apk.bat
```

详细步骤见 [BUILD_ANDROID.md](BUILD_ANDROID.md)

---

## 🎮 控制说明

### PC 版本（键盘）

| 按键 | 功能 |
|------|------|
| ← | 左移一格 |
| → | 右移一格 |
| ↑ | 旋转方块 |
| ↓ | 软降（加速下落） |
| Shift | 硬降（瞬间落底） |
| 空格 | 暂停/继续 |
| ESC | 退出游戏 |

### Android 版本（触屏）

屏幕底部虚拟按键：
- **←** : 左移
- **→** : 右移
- **↻** : 旋转
- **↓** : 软降
- **⤓** : 硬降
- **||** : 暂停

---

## 📁 项目结构

```
tetris/
├── main.py                  # PC 版主程序
├── main_mobile.py           # 移动端主程序
├── game_logic.py            # PC 版游戏逻辑
├── game_logic_mobile.py     # 移动端游戏逻辑（含触屏）
├── game_display.py          # PC 版渲染
├── game_display_mobile.py   # 移动端渲染
├── game_init.py             # 游戏初始化
├── sound_manager.py         # 音效管理
├── blocks.py                # 方块定义
├── buildozer.spec           # APK 打包配置
├── build_apk.bat            # Windows APK 构建脚本
├── dist/
│   └── Tetris_PC.exe       # Windows 可执行文件
└── README.md               # 本文件
```

---

## 🛠️ 构建说明

### Windows EXE 打包
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Tetris_PC" main.py
```

### Android APK 打包
需要 Windows 10/11 + WSL (Ubuntu)：
```powershell
# 安装 WSL
wsl --install -d Ubuntu

# 重启后，在 WSL 中运行
wsl
sudo apt update
sudo apt install -y python3-pip git unzip openjdk-17-jdk
pip3 install buildozer cython

# 构建 APK
cd /mnt/c/git/tetris
buildozer android debug
```

详细指南：[BUILD_ANDROID.md](BUILD_ANDROID.md)

---

## 📝 更新日志

### V1.0 (2026-04-04)
- ✅ 全新 3D 风格界面
- ✅ 添加音效系统（背景音乐 + 游戏音效）
- ✅ 支持幽灵方块预览
- ✅ 支持下一个方块预览
- ✅ 添加关卡系统（10 关）
- ✅ 添加暂停功能
- ✅ 优化移动控制（按一次移动一格）
- ✅ 添加 Android 移动端支持
- ✅ 添加 APK 构建脚本
- ✅ 生成 Windows 可执行文件

### V0.1 (早期版本)
- 基础俄罗斯方块功能
- 简单图形界面

---

## 💡 提示

1. **首次运行 APK 构建** 需要较长时间（30-60分钟），请耐心等待
2. **Windows 版本** 需要 Windows 7 或更高版本
3. **Android 版本** 需要 Android 5.0 (API 21) 或更高版本
4. **音量控制** 可通过系统音量键调节

---

## 📄 许可证

本项目为开源项目，可自由使用和修改。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**作者**: rivalhw  
**邮箱**: rivalhw@qq.com  
**GitHub**: https://github.com/rivalhw/tetris
