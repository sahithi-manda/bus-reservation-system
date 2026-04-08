import customtkinter as ctk
from tkinter import messagebox
from core.auth_manager import register_user, authenticate_user

# Set appearance mode and color theme for a premium look
ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AuthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bus Reservation System - Authentication")
        self.geometry("600x580")
        self.minsize(600, 580)

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        # Main frame to hold Login or Register frames
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        self.login_frame = LoginFrame(self.main_frame, self.show_register_frame, self.on_login_success)
        self.register_frame = RegisterFrame(self.main_frame, self.show_login_frame)

        # Start with login frame
        self.show_login_frame()

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True, padx=40, pady=40)

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True, padx=40, pady=20)

    def on_login_success(self, username):
        try:
            from gui.dashboard import DashboardWindow
        except ImportError as e:
            if "tkcalendar" in str(e):
                from tkinter import messagebox
                messagebox.showerror("Missing Dependency", "Please install tkcalendar!\nOpen terminal and run: pip install tkcalendar")
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", f"Failed to load Dashboard:\n{e}")
            return
            
        # Hide the authentication window
        self.withdraw()
        
        # Define the logout behavior to bring AuthWindow back
        def handle_logout():
            self.deiconify()
            self.login_frame.password_entry.delete(0, 'end')
            
        # Launch Dashboard as a Toplevel window attached to the main Auth app
        self.dashboard = DashboardWindow(self, username, handle_logout)
        
        # If user forcefully closes the dashboard window (X button), safely kill the entire application
        self.dashboard.protocol("WM_DELETE_WINDOW", self.destroy)


from core.utils import get_logo_image

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, switch_to_register_callback, login_success_callback):
        super().__init__(parent)
        self.switch_to_register = switch_to_register_callback
        self.login_success = login_success_callback

        # Center Yatra Logo
        self.logo_img = get_logo_image(size=(220, 80))
        if self.logo_img:
            self.title_label = ctk.CTkLabel(self, text="", image=self.logo_img)
        else:
            self.title_label = ctk.CTkLabel(self, text="Bus Reservation System", font=ctk.CTkFont(size=26, weight="bold"))
        self.title_label.pack(pady=(30, 5))
        self.subtitle_label = ctk.CTkLabel(self, text="Login to your account", font=ctk.CTkFont(size=14), text_color="gray")
        self.subtitle_label.pack(pady=(0, 20))

        # Username
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=280, height=45)
        self.username_entry.pack(pady=12)

        # Password
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=280, height=45)
        self.password_entry.pack(pady=12)

        # Login Button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.handle_login, width=280, height=45,
                                          font=ctk.CTkFont(size=15, weight="bold"),
                                          fg_color="#e21a22", hover_color="#c1181e")
        self.login_button.pack(pady=25)

        # Switch to Register
        self.switch_label = ctk.CTkLabel(self, text="Don't have an account?", text_color="gray")
        self.switch_label.pack(pady=(10, 0))
        self.switch_button = ctk.CTkButton(self, text="Register Here", fg_color="transparent", 
                                           text_color="#e21a22", hover_color=("gray90", "gray20"),
                                           command=self.switch_to_register)
        self.switch_button.pack()

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        success, message = authenticate_user(username, password)
        if success:
            # Clear entries
            self.password_entry.delete(0, 'end')
            self.login_success(username)
        else:
            messagebox.showerror("Login Failed", message)


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, switch_to_login_callback):
        super().__init__(parent)
        self.switch_to_login = switch_to_login_callback

        # Logo / Title
        self.logo_img = get_logo_image(size=(180, 60))
        if self.logo_img:
            self.title_label = ctk.CTkLabel(self, text="", image=self.logo_img)
        else:
            self.title_label = ctk.CTkLabel(self, text="Create New Account", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 15))

        # Username
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=280, height=40)
        self.username_entry.pack(pady=10)

        # Email
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=280, height=40)
        self.email_entry.pack(pady=10)

        # Phone Number
        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Phone Number", width=280, height=40)
        self.phone_entry.pack(pady=10)

        # Password
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=280, height=40)
        self.password_entry.pack(pady=10)

        # Confirm Password
        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*", width=280, height=40)
        self.confirm_password_entry.pack(pady=10)

        # Register Button
        self.register_button = ctk.CTkButton(self, text="Register", command=self.handle_register, width=280, height=45,
                                             font=ctk.CTkFont(size=14, weight="bold"),
                                             fg_color="#e21a22", hover_color="#c1181e")
        self.register_button.pack(pady=20)

        # Switch to Login
        self.switch_label = ctk.CTkLabel(self, text="Already have an account?", text_color="gray")
        self.switch_label.pack(pady=(5, 0))
        self.switch_button = ctk.CTkButton(self, text="Login Here", fg_color="transparent", 
                                           text_color="#e21a22", hover_color=("gray90", "gray20"),
                                           command=self.switch_to_login)
        self.switch_button.pack()

    def handle_register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        phone_number = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_password_entry.get().strip()

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        success, message = register_user(username, email, phone_number, password)
        if success:
            messagebox.showinfo("Success", "Account created successfully! You can now login.")
            # Clear fields
            self.username_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.phone_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            self.switch_to_login()
        else:
            messagebox.showerror("Registration Failed", message)
