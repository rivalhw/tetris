# Tetris APK 构建脚本
# 运行方式: 右键 PowerShell -> 以管理员身份运行，然后执行 .\build_apk.ps1

Write-Host "========================================" -ForegroundColor Green
Write-Host "   Tetris Android APK 构建工具" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "需要管理员权限！请以管理员身份运行 PowerShell" -ForegroundColor Red
    Write-Host "右键点击 PowerShell -> 以管理员身份运行" -ForegroundColor Yellow
    Read-Host "按 Enter 键退出"
    exit 1
}

# 检查 WSL
Write-Host "检查 WSL 状态..." -ForegroundColor Gray
try {
    $wslCheck = wsl --list --quiet 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "WSL not installed"
    }
    Write-Host "WSL 已安装" -ForegroundColor Green
} catch {
    Write-Host "WSL 未安装，正在安装..." -ForegroundColor Yellow
    Write-Host "这将安装 WSL + Ubuntu，完成后需要重启电脑" -ForegroundColor Yellow
    Read-Host "按 Enter 键开始安装，或按 Ctrl+C 取消"
    
    wsl --install -d Ubuntu --no-launch
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "WSL 安装完成！" -ForegroundColor Green
    Write-Host "请重启电脑后再次运行此脚本" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Green
    Read-Host "按 Enter 键退出"
    exit
}

# 获取项目路径
$projectPath = (Get-Location).Path -replace '\\', '/'
$drive = (Get-Location).Drive.Name.ToLower()
$wslPath = "/mnt/$drive$($projectPath.Substring(2))"

Write-Host ""
Write-Host "项目路径: $wslPath" -ForegroundColor Gray
Write-Host ""
Write-Host "即将开始构建 APK" -ForegroundColor Cyan
Write-Host "首次构建需要 30-60 分钟下载依赖，请耐心等待" -ForegroundColor Yellow
Write-Host ""
Read-Host "按 Enter 键开始构建，或按 Ctrl+C 取消"

# 复制 bash 脚本到临时目录并执行
$tempScript = "$env:TEMP\build_tetris.sh"
Copy-Item "build_tetris_wsl.sh" $tempScript -Force

# 在 WSL 中执行构建
$wslTempPath = "/mnt/$drive/$($env:TEMP.Substring(3).Replace('\', '/').Replace('Users', 'users').Replace('AppData', 'appdata').Replace('Local', 'local').Replace('Temp', 'temp'))"

Write-Host ""
Write-Host "正在启动 WSL 构建..." -ForegroundColor Green
wsl bash "$wslTempPath/build_tetris.sh" "$wslPath"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "构建脚本执行完毕!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 检查 APK 是否生成
$apkFiles = Get-ChildItem -Path "bin\*.apk" -ErrorAction SilentlyContinue
if ($apkFiles) {
    Write-Host ""
    Write-Host "APK 文件已生成:" -ForegroundColor Green
    foreach ($apk in $apkFiles) {
        Write-Host "  - $($apk.Name)" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "安装步骤:" -ForegroundColor Cyan
    Write-Host "1. 将 bin/ 目录中的 APK 文件复制到手机" -ForegroundColor White
    Write-Host "2. 在手机上允许'安装未知来源应用'" -ForegroundColor White
    Write-Host "3. 安装并运行" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "未找到 APK 文件，请检查 bin/ 目录或查看构建日志" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "按 Enter 键退出"
