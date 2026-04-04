# Tetris APK 自动构建脚本
# 需要管理员权限运行

param(
    [switch]$InstallWSL,
    [switch]$BuildOnly
)

Write-Host "========================================" -ForegroundColor Green
Write-Host "   Tetris Android APK 自动构建工具" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 检查管理员权限
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "需要管理员权限！正在重新提权运行..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -InstallWSL" -Verb RunAs
    exit
}

# 检查 WSL
$wslInstalled = $false
try {
    $wslOutput = wsl --list --quiet 2>&1
    if ($LASTEXITCODE -eq 0) {
        $wslInstalled = $true
        Write-Host "WSL 已安装" -ForegroundColor Green
    }
} catch {
    $wslInstalled = $false
}

# 安装 WSL
if (-not $wslInstalled -and -not $BuildOnly) {
    Write-Host "正在安装 WSL + Ubuntu..." -ForegroundColor Yellow
    Write-Host "这可能需要几分钟时间..." -ForegroundColor Gray
    
    wsl --install -d Ubuntu --no-launch
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "WSL 安装完成！" -ForegroundColor Green
    Write-Host "请重启电脑后再次运行此脚本" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "按任意键退出..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

if (-not $wslInstalled) {
    Write-Host "错误：WSL 未安装。请运行：wsl --install" -ForegroundColor Red
    exit 1
}

# 获取项目路径
$projectPath = (Get-Location).Path
$drive = (Get-Location).Drive.Name.ToLower()
$wslPath = "/mnt/$drive$($projectPath.Substring(2).Replace('\', '/'))"

Write-Host "项目路径: $wslPath" -ForegroundColor Gray

# 创建构建脚本
$buildScript = @"
#!/bin/bash
set -e

echo "========================================"
echo "Tetris Android 构建脚本"
echo "========================================"

# 进入项目目录
cd $wslPath

# 检查并安装依赖
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
~/.local/bin/buildozer android debug 2>&1 || {
    echo "构建失败，尝试清理后重新构建..."
    ~/.local/bin/buildozer android clean
    ~/.local/bin/buildozer android debug 2>&1
}

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
"@

$scriptPath = "$env:TEMP\build_tetris.sh"
$buildScript | Out-File -FilePath $scriptPath -Encoding UTF8

Write-Host ""
Write-Host "即将在 WSL 中开始构建..." -ForegroundColor Cyan
Write-Host "按 Enter 键继续，或按 Ctrl+C 取消" -ForegroundColor Yellow
Read-Host

# 运行构建
wsl bash "$($scriptPath.Replace('\', '/').Replace('C:', '/mnt/c').Replace('Users', 'users').Replace('AppData', 'appdata').Replace('Local', 'local').Replace('Temp', 'temp'))"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "构建脚本执行完毕!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 检查 APK 是否生成
$apkPath = "bin\tetris_mobile-1.0.0-arm64-v8a_armeabi-v7a-debug.apk"
if (Test-Path $apkPath) {
    Write-Host ""
    Write-Host "APK 文件已生成: $apkPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "安装步骤:" -ForegroundColor Cyan
    Write-Host "1. 将 APK 文件复制到手机" -ForegroundColor White
    Write-Host "2. 在手机上允许'安装未知来源应用'" -ForegroundColor White
    Write-Host "3. 安装并运行" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "APK 文件可能位于 bin/ 目录中，请检查" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
