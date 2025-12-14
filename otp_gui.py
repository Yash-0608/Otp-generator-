import tkinter as tk
from tkinter import messagebox
import threading
from otp_generator import OTPSystem

class OTPApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Netzeal Secure Access System")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Initialize Backend
        self.system = OTPSystem()
        
        # State variables
        self.phone_number = ""
        
        # Configure Styles (Basic)
        self.configure(bg="#f0f2f5")
        self.header_font = ("Helvetica", 16, "bold")
        self.normal_font = ("Helvetica", 12)
        
        # Container for frames
        self.container = tk.Frame(self, bg="#f0f2f5")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initialize Frames
        self.frames = {}
        for F in (PhonePage, OTPPage, PasswordPage, SuccessPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("PhonePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        # Reset specific frame inputs if needed
        if hasattr(frame, "on_show"):
            frame.on_show()

    def run_backend_task(self, task_func, callback=None):
        """Runs a backend task in a separate thread to keep UI responsive."""
        def wrapper():
            result = task_func()
            if callback:
                # Schedule callback on main thread
                self.after(0, lambda: callback(result))
        
        threading.Thread(target=wrapper, daemon=True).start()

class Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff", bd=2, relief="groove")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        pass

class PhonePage(Page):
    def create_widgets(self):
        # Logo or Title
        tk.Label(self, text="Step 1: Identification", font=self.controller.header_font, bg="white", fg="#008069").pack(pady=(40, 20))
        
        tk.Label(self, text="Enter your Phone Number:", font=self.controller.normal_font, bg="white").pack(pady=5)
        
        self.phone_entry = tk.Entry(self, font=self.controller.normal_font, width=25, justify="center")
        self.phone_entry.pack(pady=10)
        self.phone_entry.insert(0, "91") # Pre-fill country code
        
        self.status_label = tk.Label(self, text="", fg="gray", bg="white", font=("Arial", 9))
        self.status_label.pack(pady=5)

        self.btn = tk.Button(self, text="Send OTP", command=self.send_otp, bg="#008069", fg="white", font=self.controller.normal_font, width=15)
        self.btn.pack(pady=20)

    def send_otp(self):
        phone = self.phone_entry.get().strip()
        if not phone or len(phone) < 10:
            messagebox.showerror("Error", "Please enter a valid phone number.")
            return
        
        self.controller.phone_number = phone
        self.status_label.config(text="Opening WhatsApp... Check your app!", fg="#008069")
        self.btn.config(state="disabled", text="Sending...")
        
        # Run send_otp in background so UI doesn't freeze
        self.controller.run_backend_task(
            lambda: self.controller.system.send_otp(phone),
            self.on_sent
        )

    def on_sent(self, _):
        self.btn.config(state="normal", text="Send OTP")
        self.status_label.config(text="")
        self.controller.show_frame("OTPPage")

class OTPPage(Page):
    def create_widgets(self):
        tk.Label(self, text="Step 2: Verification", font=self.controller.header_font, bg="white", fg="#008069").pack(pady=(40, 20))
        
        self.lbl_instruction = tk.Label(self, text="Enter the 4-digit OTP:", font=self.controller.normal_font, bg="white")
        self.lbl_instruction.pack(pady=5)
        
        self.otp_entry = tk.Entry(self, font=("Courier", 24, "bold"), width=6, justify="center")
        self.otp_entry.pack(pady=15)
        
        tk.Button(self, text="Verify OTP", command=self.verify, bg="#008069", fg="white", font=self.controller.normal_font, width=15).pack(pady=20)
        
        tk.Button(self, text="Back", command=lambda: self.controller.show_frame("PhonePage"), bg="white", fg="gray", bd=0).pack()

    def on_show(self):
        self.otp_entry.delete(0, tk.END)
        self.otp_entry.focus_set()
        self.lbl_instruction.config(text=f"OTP sent to {self.controller.phone_number}")

    def verify(self):
        otp = self.otp_entry.get().strip()
        if self.controller.system.verify_otp(self.controller.phone_number, otp):
             # Determine mode: Login or Register
             if self.controller.system.user_exists(self.controller.phone_number):
                 self.controller.frames["PasswordPage"].set_mode("login")
             else:
                 self.controller.frames["PasswordPage"].set_mode("register")
                 
             self.controller.show_frame("PasswordPage")
        else:
             messagebox.showerror("Failed", "Incorrect OTP. Please try again.")

class PasswordPage(Page):
    def create_widgets(self):
        self.lbl_title = tk.Label(self, text="Step 3: Authentication", font=self.controller.header_font, bg="white", fg="#008069")
        self.lbl_title.pack(pady=(40, 20))
        
        self.lbl_instruction = tk.Label(self, text="Enter System Password:", font=self.controller.normal_font, bg="white")
        self.lbl_instruction.pack(pady=5)
        
        self.pass_entry = tk.Entry(self, font=self.controller.normal_font, width=25, show="*", justify="center")
        self.pass_entry.pack(pady=10)
        
        self.btn_action = tk.Button(self, text="Login", command=self.submit, bg="#008069", fg="white", font=self.controller.normal_font, width=15)
        self.btn_action.pack(pady=20)
        
        self.mode = "login"

    def set_mode(self, mode):
        self.mode = mode
        if mode == "login":
            self.lbl_title.config(text="Step 3: Login")
            self.lbl_instruction.config(text="Enter your Password:")
            self.btn_action.config(text="Login")
        else:
            self.lbl_title.config(text="Step 3: Registration")
            self.lbl_instruction.config(text="Create a new Password:")
            self.btn_action.config(text="Set Password")

    def on_show(self):
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.focus_set()

    def submit(self):
        pwd = self.pass_entry.get()
        if not pwd:
            messagebox.showwarning("Warning", "Password cannot be empty")
            return

        phone = self.controller.phone_number
        
        if self.mode == "login":
            if self.controller.system.verify_password(phone, pwd):
                self.controller.show_frame("SuccessPage")
            else:
                messagebox.showerror("Access Denied", "Incorrect Password.")
        else:
            # Registration Mode
            self.controller.system.register_user(phone, pwd)
            messagebox.showinfo("Success", "Password set successfully!")
            self.controller.show_frame("SuccessPage")

class SuccessPage(Page):
    def create_widgets(self):
        # Green Background
        self.config(bg="#25D366") 
        
        tk.Label(self, text="✔", font=("Arial", 60), bg="#25D366", fg="white").pack(pady=(80, 10))
        tk.Label(self, text="ACCESS GRANTED", font=("Arial", 20, "bold"), bg="#25D366", fg="white").pack(pady=10)
        tk.Label(self, text="Welcome to Netzeal System", font=("Arial", 12), bg="#25D366", fg="white").pack(pady=5)
        
        tk.Button(self, text="Exit", command=self.controller.quit, bg="white", fg="#25D366", font=("Arial", 12, "bold"), width=15).pack(pady=50)


if __name__ == "__main__":
    app = OTPApplication()
    app.mainloop()
