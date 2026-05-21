@echo off
echo   Starlink Data Scraper
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install requirements
echo Installing required packages...
pip install pandas selenium

echo.
echo Requirements installed!
echo.

REM Make sure Chrome with remote debugging is running
echo Make sure Chrome is running with: chrome.exe --remote-debugging-port=9222
echo.

REM Run the Python script
python starlink_scraper.py

pause