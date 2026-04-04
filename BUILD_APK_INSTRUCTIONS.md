# APK 构建说明

## 快速开始

### 方法一：双击批处理文件（最简单）

1. **右键点击 `build_apk.bat`** → **以管理员身份运行**
2. 按提示操作即可

### 方法二：PowerShell 命令行

1. **右键点击 PowerShell** → **以管理员身份运行**
2. 执行命令：
```powershell
cd C:\git\tetris
.\build_apk.ps1
```

## 首次运行说明

### 如果从未安装过 WSL

脚本会自动安装 WSL + Ubuntu，需要：
1. **重启电脑**（安装完成后必须重启）
2. 重启后**再次运行脚本**开始构建

### 构建过程

- **首次构建**：约 30-60 分钟（需要下载 Android SDK/NDK）
- **后续构建**：约 5-10 分钟
- **输出位置**：`bin/tetris_mobile-1.0.0-*.apk`

## 安装到手机

1. 将生成的 APK 文件复制到手机
2. 在手机设置中允许"安装未知来源应用"
3. 点击 APK 文件安装
4. 运行游戏

## 文件说明

| 文件 | 用途 |
|------|------|
| `build_apk.bat` | Windows 批处理入口 |
| `build_apk.ps1` | PowerShell 脚本 |
| `build_tetris_wsl.sh` | WSL 中的构建脚本 |
| `buildozer.spec` | APK 打包配置 |

## 常见问题

### Q: 提示"无法运行脚本"
**解决**：确保以管理员身份运行 PowerShell

### Q: 构建失败
**解决**：
```bash
# 在 WSL 中手动清理
wsl ~/.local/bin/buildozer android clean
# 然后重新运行脚本
```

### Q: 找不到 APK 文件
**解决**：检查 `bin/` 目录，文件名格式为 `tetris_mobile-1.0.0-*.apk`

## 系统要求

- Windows 10/11
- 管理员权限
- 约 10GB 可用磁盘空间
- 良好的网络连接
- WSL 功能已启用

## 替代方案

如果打包困难，可以使用 **Pydroid 3** 直接在手机上运行：
1. 应用商店安装 Pydroid 3
2. 安装 pygame：`pip install pygame`
3. 打开 `main_mobile.py` 运行
