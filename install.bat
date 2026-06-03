@echo off
chcp 65001 >nul
title LM Studio 简体中文汉化
echo.
echo  LM Studio 简体中文汉化补丁
echo  ============================
echo.
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3
    echo        https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python 已就绪
echo.
echo 正在应用汉化...
python "%~dp0patch_lmstudio.py"
if %errorlevel% neq 0 (
    echo.
    echo [错误] 汉化失败
    pause
    exit /b 1
)
echo.
echo 重启 LM Studio 即可看到中文界面
echo 还原英文: python patch_lmstudio.py --restore
echo.
pause
