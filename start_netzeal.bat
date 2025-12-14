@echo off
echo Starting Netzeal Secure Access System...
echo Note: Please ensure WhatsApp Desktop is instaled and logged in.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not found in your PATH.
    pause
    exit /b
)

REM Install dependencies if needed (optional check, but good for first run)
REM pip install pywhatkit pyautogui >nul 2>&1

REM Run the GUI
python otp_gui.py

pause
