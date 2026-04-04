# 俄罗斯方块 - Android 版本

## 📱 新增移动端支持

已为项目添加完整的 Android 手机版本支持！

## 🎯 快速开始

### 选项 1: PC 上直接运行（推荐先测试）
```bash
# 运行 PC 版本
python main.py

# 或运行移动端版本（带虚拟按键）
python main_mobile.py
```

### 选项 2: Windows 可执行文件（无需 Python）
直接双击运行：`dist/Tetris_PC.exe`

### 选项 3: Android 手机（使用 Pydroid 3）
1. 在手机应用商店下载 **Pydroid 3**
2. 将项目文件复制到手机
3. 在 Pydroid 3 中打开 `main_mobile.py` 运行

### 选项 4: 打包成 APK 安装包
详见下方 [打包 APK](#打包-apk) 章节

## 📂 项目文件说明

### PC 版本
| 文件 | 说明 |
|------|------|
| `main.py` | PC 版主程序 |
| `game_logic.py` | 游戏逻辑 |
| `game_display.py` | 渲染模块 |
| `game_init.py` | 初始化 |
| `sound_manager.py` | 音效管理 |
| `blocks.py` | 方块定义 |

### Android 版本
| 文件 | 说明 |
|------|------|
| `main_mobile.py` | 移动端主程序 |
| `game_logic_mobile.py` | 移动端逻辑（含触屏控制） |
| `game_display_mobile.py` | 移动端渲染 |
| `buildozer.spec` | APK 打包配置 |

## 🎮 控制方式

### PC 版本（键盘）
- `← →` : 左右移动
- `↑` : 旋转
- `↓` : 软降（加速下落）
- `Shift` : 硬降（瞬间落底）
- `空格` : 暂停
- `ESC` : 退出

### Android 版本（触屏）
- **←** : 左移
- **→** : 右移
- **↻** : 旋转
- **↓** : 软降
- **⤓** : 硬降
- **||** : 暂停

## 📦 打包 APK

### 前提条件
- Windows 10/11 系统
- 已安装 Python
- 约 10GB 可用磁盘空间
- 良好的网络连接

### 步骤 1: 安装 WSL (Windows Subsystem for Linux)
以管理员身份打开 PowerShell，运行：
```powershell
wsl --install -d Ubuntu
```
安装完成后**重启电脑**。

### 步骤 2: 在 WSL 中安装构建环境
重启后，打开 Ubuntu 终端，运行：
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git unzip openjdk-17-jdk \
    autoconf automake libtool pkg-config zlib1g-dev libncurses5-dev \
    cmake libffi-dev libssl-dev

pip3 install --user buildozer cython
```

### 步骤 3: 构建 APK
```bash
# 进入项目目录（根据实际路径调整）
cd /mnt/c/git/tetris

# 开始构建（首次需要 30-60 分钟下载依赖）
~/.local/bin/buildozer android debug

# 或使用辅助脚本
python3 android_build/build_for_android.py
```

构建完成后，APK 文件位于 `bin/tetris_mobile-1.0.0-arm64-v8a-debug.apk`

### 步骤 4: 安装到手机
1. 将 APK 文件传输到手机
2. 在手机上允许"安装未知来源应用"
3. 安装并运行

## 🔧 故障排除

### 构建失败
```bash
# 清理缓存重新构建
~/.local/bin/buildozer android clean
~/.local/bin/buildozer android debug
```

### 缺少依赖
```bash
# 安装所有可能需要的依赖
sudo apt install -y build-essential libsqlite3-dev sqlite3 bzip2 \
    libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev \
    libgdbm-compat-dev liblzma-dev libreadline-dev libncursesw5-dev \
    uuid-dev
```

### WSL 相关问题
```powershell
# 更新 WSL
wsl --update

# 修复 WSL
wsl --shutdown
wsl --unregister Ubuntu
wsl --install -d Ubuntu
```

## 📋 系统要求

### PC 版本
- Windows 7/8/10/11
- Python 3.8+
- 或直接使用 `Tetris_PC.exe`

### Android 版本
- Android 5.0 (API 21) 及以上
- 约 50MB 存储空间
- 支持触屏操作

## 🎨 界面预览

### PC 版本
- 窗口大小：600x720
- 键盘控制
- 音效支持

### Android 版本
- 竖屏模式：480x800
- 虚拟按键
- 触屏支持
- 适配各种手机屏幕

## 📝 注意事项

1. **首次打包耗时**：首次运行 buildozer 需要下载 Android SDK、NDK 等，耗时较长，请耐心等待。

2. **网络要求**：打包过程需要从 Google、GitHub 等网站下载依赖，请确保网络畅通。

3. **存储空间**：建议至少保留 10GB 可用空间用于构建。

4. **调试版本**：生成的 APK 是调试版本，如需发布到应用商店，需要使用发布签名。

## 🤝 需要帮助？

如果遇到问题，可以：
1. 检查 `BUILD_ANDROID.md` 详细指南
2. 运行 `python android_build/build_for_android.py` 使用辅助脚本
3. 查看 `android_build/README.md` 额外说明

## 📄 许可证

本项目为示例项目，可自由使用和修改。
