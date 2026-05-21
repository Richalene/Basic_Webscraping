@echo off
echo ====================================
echo   Starlink Data Scraper
echo ====================================
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [SETUP] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        echo         Make sure Python is installed and on your PATH.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created!
    echo.
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment active!
echo.

REM Install requirements
echo [SETUP] Installing required packages...
pip install pandas selenium
if errorlevel 1 (
    echo [ERROR] pip install failed. Check your internet connection.
    pause
    exit /b 1
)
echo [OK] Requirements installed!
echo.

start chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\Mary\AppData\Local\Temp\chrome_debug" https://starlink.com

REM Check Chrome debugging port
echo [CHECK] Checking if Chrome remote debugging is reachable...
curl -s http://127.0.0.1:9222/json >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Chrome remote debugging port 9222 does not appear to be open.
    echo.
    echo           Start Chrome with this command first:
    echo           chrome.exe --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome_debug"
    echo.
    echo           Then re-run this script.
    pause
    exit /b 1
)
echo [OK] Chrome debugging port is open!
echo.

REM Run the Python script
echo [RUN] Starting starlink_scraper.py...
echo ====================================
echo.
python starlink_scraper.py
if errorlevel 1 (
    echo.
    echo ====================================
    echo [ERROR] Script exited with an error ^(see above^).
    echo ====================================
) else (
    echo.
    echo ====================================
    echo [DONE] Script completed successfully!
    echo ====================================
)

pause