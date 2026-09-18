@echo off
chcp 65001 >nul
cd /d "%~dp0"
title QQ-Codex Bridge

echo ========================================
echo   QQ-Codex Bridge ^(QQ官方API直连^)
echo ========================================
echo.

:: 找 Python
set "PY="

:: 1. Codex 运行时 Python
set "CP=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%CP%" set "PY=%CP%" & goto :gotpy

:: 2. 系统 Python
where python >nul 2>nul && (python -c "" 2>nul && set "PY=python" & goto :gotpy)

echo [错误] 未找到可用 Python！请安装 Python 3.10+
pause & exit /b 1

:gotpy
echo [OK] Python: %PY%

:: 安装依赖
echo [1/2] 检查依赖...
"%PY%" -m pip install -r requirements.txt -q 2>nul

:: 创建必要目录
if not exist "temp" mkdir temp

:: 启动
echo [2/2] 启动 Bridge...
echo.
"%PY%" bridge.py

pause
