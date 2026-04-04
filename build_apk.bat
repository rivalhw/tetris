@echo off
chcp 65001 >nul
title Tetris APK 构建工具
echo ========================================
echo    Tetris Android APK 构建工具
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo 需要管理员权限！
    echo 请以管理员身份运行此脚本。
    echo.
    echo 操作方法：
    echo 1. 右键点击此文件
    echo 2. 选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

:: 检查 WSL
echo 检查 WSL 状态...
wsl --list --quiet >nul 2>&1
if errorlevel 1 (
    echo.
    echo WSL 未安装，正在安装 WSL + Ubuntu...
    echo 这将需要几分钟时间，完成后需要重启电脑。
    echo.
    pause
    
    wsl --install -d Ubuntu --no-launch
    
    echo.
    echo ========================================
    echo WSL 安装完成！
    echo 请重启电脑后再次运行此脚本
    echo ========================================
    pause
    exit /b 0
)

echo WSL 已安装
echo.

:: 获取项目路径
set "PROJECT_PATH=%CD%"
echo 项目路径: %PROJECT_PATH%
echo.

echo 即将开始构建 APK
echo 注意：首次构建需要 30-60 分钟下载依赖
echo 请确保网络连接正常
echo.
pause

:: 执行 PowerShell 脚本
powershell -ExecutionPolicy Bypass -File "build_apk.ps1"

pause
