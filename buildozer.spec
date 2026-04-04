[app]
# 应用标题
title = Tetris Mobile

# 包名
package.name = tetris_mobile

# 包域名
package.domain = org.example

# 主程序文件
source.dir = .

# 包含的文件
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,ttc,mp3,wav

# 版本号
version = 1.0.0

# 依赖项
requirements = python3,pygame,pygame-ce

# 应用图标（如果有的话）
#icon.filename = icon.png

# 是否为触屏设备
fullscreen = 0
orientation = portrait

# Android API 设置
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a

# 权限
android.permissions = INTERNET, VIBRATE

# 额外选项
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
