@echo off
setlocal enabledelayedexpansion
title NeuraSelf-UwU Setup
cd /d "%~dp0"
chcp 65001 >nul

set "PYTHON_VER=3.10.11"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VER%/python-%PYTHON_VER%-amd64.exe"

color 0B
echo.
echo  [SYSTEM] Initializing NeuraSelf-UwU Auto-Setup...
echo.

py -3.10 --version >nul 2>&1
if !errorlevel! neq 0 (
    echo  [!] Python 3.10 not found. Starting Auto-Installation...
    echo  [#] Downloading Python Installer...
    curl -L -o py_inst.exe %PYTHON_URL%
    if !errorlevel! neq 0 (
        echo  [X] Download failed. Please install Python 3.10 manually.
        pause
        exit /b 1
    )
    echo  [#] Installing Python - quiet mode...
    start /wait py_inst.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del py_inst.exe
    echo  [OK] Python installation completed.
) else (
    echo  [OK] Python 3.10 already installed.
)

echo  [#] Upgrading pip...
py -3.10 -m pip install --upgrade pip --quiet 

echo  [#] Installing project requirements...
py -3.10 -m pip install -r requirements.txt --progress-bar on
if !errorlevel! neq 0 (
    echo  [X] Failed to install dependencies. Check your connection.
    pause
    exit /b 1
)

echo  [OK] Environment is ready.
echo.
echo =======================================================
echo     SETUP COMPLETE! HOW WOULD YOU LIKE TO PROCEED?
echo =======================================================
echo.
echo  [1] Configure Accounts Now
echo  [2] Start NeuraSelf Directly
echo  [3] Exit
echo.

set /p choice=" Selection (1-3): "

if "%choice%"=="1" (
    py -3.10 config_helper.py
) else if "%choice%"=="2" (
    py -3.10 neura.py
) else (
    echo  [!] Exiting setup. Run neura.py later to start.
    exit /b 0
)

pause
