@echo off
chcp 65001 >nul
echo ========================================
echo Tetris Windows 可执行文件打包工具
echo ========================================
echo.

REM 检查 PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
)

echo 正在打包...

REM 打包 PC 版本
pyinstaller --clean --onefile --windowed --name "Tetris" ^
    --add-data "blocks.py;." ^
    --add-data "game_display.py;." ^
    --add-data "game_logic.py;." ^
    --add-data "game_init.py;." ^
    --add-data "game_end.py;." ^
    --add-data "sound_manager.py;." ^
    main.py

if errorlevel 1 (
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo 可执行文件位于: dist\Tetris.exe
echo ========================================
pause
