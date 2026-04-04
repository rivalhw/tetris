# Android 版本构建指南

## 概述

已为项目添加移动端支持，包括：
- 虚拟按键控制（← → ↻ ↓ ⤓ ||）
- 触屏操作支持
- 适配手机屏幕尺寸（480x800 竖屏）

## 运行方式

### 方式 1: PC 上测试移动端版本

```bash
python main_mobile.py
```

使用鼠标点击虚拟按键进行控制。

### 方式 2: 手机上使用 Pydroid 3（最简单）

1. 在 Google Play 安装 **Pydroid 3** 应用
2. 安装 pygame 依赖（Pydroid 3 内置 pip）
3. 复制项目文件到手机
4. 在 Pydroid 3 中打开 `main_mobile.py` 运行

### 方式 3: 打包成 APK

#### 准备环境（Windows + WSL）

1. **安装 WSL (Windows Subsystem for Linux)**
   ```powershell
   wsl --install -d Ubuntu
   ```
   安装后重启电脑。

2. **在 WSL 中安装依赖**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv git unzip openjdk-17-jdk \
       autoconf automake libtool pkg-config zlib1g-dev libncurses5-dev \
       cmake libffi-dev libssl-dev
   ```

3. **安装 Buildozer**
   ```bash
   pip3 install --user buildozer cython
   ```

#### 构建 APK

在项目目录下运行：

```bash
# 进入 WSL
wsl

# 进入项目目录
cd /mnt/c/git/tetris  # 根据实际路径调整

# 构建 APK（首次需要较长时间下载依赖）
~/.local/bin/buildozer android debug
```

构建完成后，APK 文件位于 `bin/tetris_mobile-1.0.0-*.apk`

#### 自动化脚本

也可运行辅助脚本：
```bash
python android_build/build_for_android.py
```

### 方式 4: 使用 Docker 打包

如果已安装 Docker：

```bash
docker run -it --rm \
  -v $(pwd):/home/user/app \
  -v ~/.buildozer:/home/user/.buildozer \
  kivy/buildozer android debug
```

## 移动端文件说明

| 文件 | 说明 |
|------|------|
| `main_mobile.py` | 移动端主程序入口 |
| `game_logic_mobile.py` | 移动端游戏逻辑（含触屏控制） |
| `game_display_mobile.py` | 移动端渲染（适配小屏幕） |
| `buildozer.spec` | Buildozer 打包配置 |

## 控制说明

### 虚拟按键
- **←** : 左移
- **→** : 右移  
- **↻** : 旋转
- **↓** : 软降（加速下落）
- **⤓** : 硬降（瞬间落底）
- **||** : 暂停

### 手势（预留）
- 向左滑动：左移
- 向右滑动：右移
- 向上滑动：旋转
- 向下滑动：软降
- 双击：硬降

## 注意事项

1. **首次打包耗时**：首次运行 buildozer 会自动下载 Android SDK/NDK，可能需要 30 分钟以上。

2. **存储空间**：确保有至少 10GB 可用空间。

3. **网络连接**：打包过程需要从网络下载依赖。

4. **APK 安装**：生成的 APK 是调试版本，需要在手机设置中允许"安装未知来源应用"。

## 故障排除

### 构建失败
```bash
# 清理并重新构建
buildozer android clean
buildozer android debug
```

### 权限问题
```bash
# 确保有执行权限
chmod +x android_build/*.sh
```

### 依赖缺失
```bash
# 安装所有可能需要的依赖
sudo apt install -y build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev \
    zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev \
    libreadline-dev libncursesw5-dev libffi-dev uuid-dev libffi-dev
```
