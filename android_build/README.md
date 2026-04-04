# Android 打包指南

## 方法 1：使用 Buildozer（推荐）

### 在 Linux/WSL 上打包

1. **安装 WSL**（Windows 用户）
   ```powershell
   wsl --install -d Ubuntu
   ```

2. **在 WSL 中安装依赖**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv git unzip openjdk-17-jdk
   ```

3. **安装 Buildozer**
   ```bash
   pip3 install buildozer cython
   ```

4. **运行打包命令**
   ```bash
   cd /mnt/c/git/tetris  # 替换为你的项目路径
   buildozer android debug
   ```

5. **获取 APK**
   打包完成后，APK 文件位于：`bin/tetris_mobile-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`

### 打包配置

已创建 `buildozer.spec` 配置文件，包含：
- 应用名称：Tetris Mobile
- 竖屏模式
- 触屏权限
- Android API 33

## 方法 2：使用 Docker

```bash
docker run -it --rm \
  -v $(pwd):/home/user/app \
  -v ~/.buildozer:/home/user/.buildozer \
  kivy/buildozer android debug
```

## 方法 3：使用 Pydroid 3（无需打包）

在手机上安装 Pydroid 3 应用，直接运行 Python 代码。

## 移动端特性

- 虚拟按键控制（← → ↻ ↓ ⤓）
- 触屏支持
- 适配手机屏幕尺寸
- 竖屏模式

## 文件说明

- `main_mobile.py` - 移动端主程序
- `game_logic_mobile.py` - 移动端游戏逻辑（含触屏控制）
- `game_display_mobile.py` - 移动端渲染
