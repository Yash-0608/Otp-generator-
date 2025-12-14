# Netzeal Secure Access System

A secure OTP-based authentication system built with Python. 
It sends One-Time Passwords (OTPs) via WhatsApp Desktop automation and features a GUI for user login and registration.

## Features
- **OTP Generation**: Random 4-digit security code.
- **WhatsApp Integration**: Sends OTPs directly to your WhatsApp using the Desktop App (Free).
- **User Persistence**: Saves registered users and passwords locally.
- **Graphical Interface**: Clean steps for Phone entry, OTP verification, and Password Login/Register.

## Requirements
- Python 3.x
- WhatsApp Desktop Application (Installed and Logged in)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/netzeal-otp-system.git
   cd netzeal-otp-system
   ```
2. Install dependencies:
   ```bash
   pip install pywhatkit pyautogui
   ```

## Usage
Double-click `start_netzeal.bat` to run the application.

OR run manually:
```bash
python otp_gui.py
```

## How it Works
1. Enter your Phone Number.
2. Receive OTP on WhatsApp.
3. Verify OTP.
4. **New User**: Create a password.
5. **Existing User**: Enter your password to login.
