@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title IP-Tracer Builder — by xdeust
color 0B

echo.
echo   ___  ____        _____
echo  ^|_ _^|^|  _ \      ^|_   _^| __ __ _  ___ ___ _ __
echo   ^| ^| ^| ^|_) ^|_____ ^| ^|^| '__/ _` ^|/ __/ _ \ '__^|
echo   ^| ^| ^|  __/_____^| ^| ^|^| ^| ^| (_` ^| (_^|  __/ ^|
echo  ^|___^|^|_^|          ^|_^|^|_^|  \__,_^|\___\___^|_^|
echo.
echo          IP-Tracer Build System — by xdeust
echo   ================================================
echo.

:: ─── Step 1: Install dependencies ───
echo   [1/4] Installing dependencies...
call :progress 0 "xdeust ^| Installing requests..."
pip install requests >nul 2>&1
call :progress 15 "xdeust ^| requests installed"

call :progress 20 "xdeust ^| Installing colorama..."
pip install colorama >nul 2>&1
call :progress 35 "xdeust ^| colorama installed"

call :progress 40 "xdeust ^| Installing pyinstaller..."
pip install pyinstaller >nul 2>&1
call :progress 60 "xdeust ^| pyinstaller installed"

echo.
echo   [+] All dependencies installed.
echo.

:: ─── Step 2: Build EXE ───
echo   [2/4] Building IP-Tracer.exe (this may take a minute)...
call :progress 65 "xdeust ^| Compiling..."

pyinstaller --onefile --console --name "IP-Tracer" ip_tracer.py
if %errorlevel% neq 0 (
    echo.
    echo   [-] ERROR: PyInstaller build failed! See messages above.
    echo.
    pause
    exit /b 1
)
call :progress 90 "xdeust ^| Build complete"

:: ─── Step 3: Cleanup ───
echo.
echo   [3/4] Cleaning up temp files...
if exist build rmdir /s /q build >nul 2>&1
if exist IP-Tracer.spec del /f /q IP-Tracer.spec >nul 2>&1
if exist __pycache__ rmdir /s /q __pycache__ >nul 2>&1
call :progress 95 "xdeust ^| Cleanup done"

:: ─── Step 4: Done ───
call :progress 100 "xdeust ^| All done!"
echo.
echo.
echo   ================================================
echo   [+] Build complete!
echo   [+] Your EXE is at: %~dp0dist\IP-Tracer.exe
echo   ================================================
echo   [*] Coded by xdeust
echo   ================================================
echo.
pause
exit /b

:: ─────────────────────────────────────────────────
:: FUNCTION: progress  (percent, message)
:: ─────────────────────────────────────────────────
:progress
setlocal enabledelayedexpansion
set /a pct=%~1
set "msg=%~2"

set /a filled=pct * 30 / 100
set /a empty=30 - filled

set "bar="
for /l %%i in (1,1,!filled!) do set "bar=!bar!█"
for /l %%i in (1,1,!empty!) do set "bar=!bar!░"

<nul set /p "=   [!bar!] %pct%%% — %msg%   "
echo.

if %pct% LSS 100 (
    ping -n 1 -w 300 127.0.0.1 >nul 2>&1
)
endlocal
exit /b
