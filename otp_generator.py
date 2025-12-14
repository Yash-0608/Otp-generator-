import random
import time
import os
import json
import webbrowser
import pyautogui
from urllib.parse import quote

# Try to import pywhatkit, handle if not installed
try:
    import pywhatkit
    HAS_PYWHATKIT = True
except ImportError:
    HAS_PYWHATKIT = False

DATA_FILE = "users.json"

class OTPSystem:
    def __init__(self):
        self.active_otps = {} # Map phone -> otp
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_users(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.users, f, indent=4)

    def generate_otp(self) -> str:
        """Generates a random 4-digit OTP."""
        return str(random.randint(1000, 9999))

    def send_otp(self, phone_number: str):
        """Generates an OTP and sends it via WhatsApp Desktop (Free Version)."""
        otp = self.generate_otp()
        self.active_otps[phone_number] = otp
        
        # Message content
        message = f"Thanks for showing interest in Netzeal. Your OTP is {otp}"
        
        print(f"\n[System] Sending OTP to {phone_number} via WhatsApp (Free)...")
        
        import webbrowser
        import pyautogui
        from urllib.parse import quote
        
        try:
            # Ensure number has + prefix for protocol
            if not phone_number.startswith('+'):
                formatted_phone = f"+{phone_number}"
            else:
                formatted_phone = phone_number
            
            # Create the Protocol URL for WhatsApp
            # This triggers the default installed WhatsApp Desktop app
            url = f"whatsapp://send?phone={formatted_phone}&text={quote(message)}"
            
            print("[System] Triggering WhatsApp Desktop Application...")
            webbrowser.open(url)
            
            # Wait for the application to open and the chat to load
            print("[System] Waiting for WhatsApp to load (10s)...")
            time.sleep(10) 
            
            # Press Enter to send
            print("[System] Sending message (Attempt 1: Enter)...")
            pyautogui.press('enter')
            time.sleep(1.0)
            
            print("[System] Sending message (Attempt 2: Enter)...")
            pyautogui.press('enter')
            time.sleep(1.0)

            # Fallback for some systems
            print("[System] Sending message (Attempt 3: Ctrl+Enter)...")
            pyautogui.hotkey('ctrl', 'enter')
            
            print("[System] Message sent action completed.")
            
        except Exception as e:
            print(f"[System] Error interaction with WhatsApp: {e}")
            print(f"[System] (Fallback) Your OTP is: {otp}")

    def verify_otp(self, phone_number: str, user_otp: str) -> bool:
        """Verifies if the entered OTP matches the sent one."""
        if phone_number in self.active_otps:
            if self.active_otps[phone_number] == user_otp:
                # OTP verified, remove it to prevent reuse
                del self.active_otps[phone_number]
                return True
        return False

    def user_exists(self, phone_number: str) -> bool:
        return phone_number in self.users

    def register_user(self, phone_number: str, password: str):
        self.users[phone_number] = password
        self.save_users()

    def verify_password(self, phone_number: str, password: str) -> bool:
        """Verifies the password for the specific user."""
        if phone_number in self.users:
            return self.users[phone_number] == password
        return False

def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    # Command Line Interface for testing the Backend
    system = OTPSystem()
    
    clrscr()
    print("=== Secure Access System ===")
    
    # 1. Input Phone
    phone = input("Enter your phone number (No spaces, include country code e.g. 919999999999): ").strip()
    
    # 2. Send OTP
    system.send_otp(phone)
    
    # 3. Enter OTP
    print("\n--- OTP Verification ---")
    otp_input = input("Enter the 4-digit OTP received: ").strip()
    
    if system.verify_otp(phone, otp_input):
        print("\nOTP Verified! Please proceed.")
        
        # 4. Check User Status
        if system.user_exists(phone):
            # Login
            print("\n--- Password Login ---")
            password_input = input("Enter Password: ")
            if system.verify_password(phone, password_input):
                print("\nACCESS GRANTED")
            else:
                print("\n[!] Access Denied")
        else:
            # Register
            print("\n--- Create Password ---")
            password_input = input("Create a new Password: ")
            system.register_user(phone, password_input)
            print("\nUser Registered & Access Granted!")
            
    else:
        print("\n[!] Access Denied: Incorrect OTP")
