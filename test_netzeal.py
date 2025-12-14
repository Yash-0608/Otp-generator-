from otp_generator import OTPSystem
import os

def run_test():
    print("=== NETZEAL OTP SYSTEM TEST (SMS Simulation Mode) ===")
    
    # 1. Setup
    target_phone = "9325981115"
    expected_password = "rishu@1234"
    
    system = OTPSystem()
    
    print(f"[TEST] Phone: {target_phone}")
    
    # Check if user exists before we start
    is_existing = system.user_exists(target_phone)
    if is_existing:
        print("[TEST] User ALREADY exists in database. We will test LOGIN flow.")
    else:
        print("[TEST] User is NEW. We will test REGISTRATION flow.")

    # 2. Send OTP
    print("\n[TEST] Initiating OTP Send (SMS)...")
    system.send_otp(target_phone)
    
    # 3. Verify OTP
    # Cheat to get the active OTP because we are in simulation mode or don't have the phone
    if target_phone in system.active_otps:
        generated_otp = system.active_otps[target_phone]
        print(f"[TEST] Received OTP (internal check): {generated_otp}")
        
        if system.verify_otp(target_phone, generated_otp):
             print("[TEST] OTP Verification Successful.")
             
             # 4. Authentication Flow
             if is_existing:
                 # Test Login
                 print(f"[TEST] Attempting login with expected password: '{expected_password}'")
                 if system.verify_password(target_phone, expected_password):
                     print("[TEST] >>> SUCCESS: LOGIN ACCESS GRANTED <<<")
                 else:
                     print("[TEST] >>> FAILED: Password incorrect <<<")
             else:
                 # Test Registration
                 print(f"[TEST] Registering new password: '{expected_password}'")
                 system.register_user(target_phone, expected_password)
                 print("[TEST] >>> SUCCESS: REGISTRATION COMPLETED <<<")

        else:
             print("[TEST] OTP Verification Failed.")
    else:
        print("[TEST] Error: No OTP found for phone.")

if __name__ == "__main__":
    run_test()
