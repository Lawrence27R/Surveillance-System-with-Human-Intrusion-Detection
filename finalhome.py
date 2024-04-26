import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv
from gui.mysql_db import DatabaseHandler
from gui.forgot_password import ForgotPasswordWindow
from gui.change_password import ChangePasswordWindow
from gui.navbar import NavigationBar
from gui.rec_and_logs import RecAndLogsSection
from gui.new_registration import NewRegistrationSection
from gui.add_details import AddDetailsSection
from gui.add_cctv import AddCCTVSection
from gui.sidebar import Sidebar
from gui.homecontent import HomeContent

load_dotenv()

class Homepage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Surveillance System with Human Intrusion Detection")
        self.master.geometry("1400x720+80+100")

        style = ThemedStyle(self.master)
        style.set_theme("arc")

        self.configure(bg="#232831")

        self.navbar = NavigationBar(self)
        self.navbar.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0) 

        self.sidebar_frame = tk.Frame(self, bg="#21252b", relief=tk.SUNKEN)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.sidebar = Sidebar(self, self.change_main_content)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        tk.Frame(self.sidebar_frame, width=2, bg="#21252b").pack(side=tk.LEFT, fill=tk.Y)

        self.main_content = tk.Frame(self, bg="#232831")
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.pack(fill=tk.BOTH, expand=True)

        # CCTV Table Section
        self.database = DatabaseHandler()
        self.conn, self.cursor = self.database.initialize_connection()
        self.add_cctv_section = AddCCTVSection(self.main_content, self.conn, self.cursor)
        self.logged_in_email = "rootuser@gmail.com"

        # Other sections
        self.rec_and_logs_section = RecAndLogsSection(self.main_content)
        self.new_registration_section = NewRegistrationSection(self.main_content)
        self.add_details_section = AddDetailsSection(self.main_content)

        # Home section
        self.home_content = HomeContent(self.main_content, self.add_cctv_section, self.intrusion_detector)
        self.current_section = None  # Initialize current_section to None

        self.show_section(self.home_content)  # Show home_content by default

    def open_change_password_window(self):
        ChangePasswordWindow(self, self.change_password)

    def change_password(self):
        old_password = self.logged_in_email
        new_password = ChangePasswordWindow.get_new_password()
        confirm_new_password = ChangePasswordWindow.get_confirm_new_password()

        if new_password == confirm_new_password:
            self.cursor.execute(f"UPDATE users SET password = '{new_password}' WHERE email = '{self.logged_in_email}' AND password = '{old_password}'")
            self.conn.commit()
            messagebox.showinfo("Password Changed", "Password has been changed successfully.")
        else:
            messagebox.showerror("Error", "New password and confirm password do not match.")

    def logout(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.master.destroy()

    def load_and_resize_image(self, image_path, width=None, height=None, resampling=Image.LANCZOS):
        try:
            original_image = Image.open(image_path)
            if width and height:
                resized_image = original_image.resize((width, height), resampling)
                return ImageTk.PhotoImage(resized_image)
            else:
                return ImageTk.PhotoImage(original_image)
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

    def change_main_content(self, item):
        if item == "REC & LOGS":
            self.show_section(self.rec_and_logs_section)
        elif item == "New Registration":
            self.show_section(self.new_registration_section)
        elif item == "Add Details":
            self.show_section(self.add_details_section)
        elif item == "Add CCTV":
            self.show_section(self.add_cctv_section)
        elif item == "Home":
            self.show_section(self.home_content)
        else:
            self.hide_current_section()

    def show_section(self, section):
        if self.current_section:
            self.current_section.pack_forget()
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.current_section = section

    def hide_current_section(self):
        if self.current_section:
            self.current_section.pack_forget()
            self.current_section = None

class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Surveillance System with Human Intrusion Detection")
        self.master.geometry("1400x720+80+100")
        self.master.withdraw()
        self.db = DatabaseHandler()

        self.conn, self.cursor = self.db.initialize_connection()  
        style = ThemedStyle(self.master)
        style.set_theme("arc")

        self.configure(bg="#232831")

        frame = tk.Frame(self, width=380, height=450, bg="#2E3B4E", bd=2, relief="solid", borderwidth=5)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="Log into your Account", font=('Century Gothic', 20), bg="#2E3B4E", fg="white").place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.entry1 = ttk.Entry(frame, font=("Helvetica", 12), width=28)
        self.entry1.place(relx=0.5, rely=0.38, anchor=tk.CENTER, height=35, bordermode="inside")
        self.add_placeholder(self.entry1, "Username")

        self.entry2 = ttk.Entry(frame, show="*", font=("Helvetica", 12), width=28)
        self.entry2.place(relx=0.5, rely=0.55, anchor=tk.CENTER, height=35, bordermode="inside")
        self.add_placeholder(self.entry2, "Password")

        show_password_button = ttk.Checkbutton(frame, text="Show Password", command=self.toggle_password_visibility)
        show_password_button.place(relx=0.70, rely=0.64, anchor=tk.CENTER)

        forgot_password_label = tk.Label(frame, text="Forgot Password?", font=('Century Gothic', 12), bg="#2E3B4E", fg="white", cursor="hand2")
        forgot_password_label.place(relx=0.66, rely=0.71, anchor=tk.CENTER)
        forgot_password_label.bind("<Button-1>", lambda event: self.forgot_password())

        self.error_label = tk.Label(frame, text="", font=('Helvetica', 12), fg="red", bg="#2E3B4E")
        self.error_label.place(relx=0.5, rely=0.86, anchor=tk.CENTER)

        login_button = tk.Button(frame, text="Login", command=self.submit, font=('Helvetica', 12), width=22, foreground="#2E3B4E", background="#4CAF50")
        login_button.place(relx=0.5, rely=0.80, height=38, anchor=tk.CENTER)

        self.after(50, self.show_window)
        self.pack(fill=tk.BOTH, expand=True)

    def show_window(self):
        self.master.deiconify()
        self.master.update_idletasks()
        self.master.resizable(True, True)

    def add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, entry, placeholder))

    def on_entry_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(show="*" if placeholder == "Password" else "")
            entry["style"] = "TEntry"

    def on_entry_focus_out(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(show="" if placeholder == "Password" else "*")
            entry["style"] = "Placeholder.TEntry"

    def toggle_password_visibility(self):
        current_state = self.entry2.cget("show")
        self.entry2["show"] = "" if current_state == "*" else "*"

    def submit(self):
        data = {}
        data["email"] = self.entry1.get()
        data["password"] = self.entry2.get()

        if self.db.login(data):
            print("Successful Login")
            self.destroy_current_window()
            self.after(1, self.show_homepage_delayed)  # Adjust the delay as needed
        else:
            self.error_label.config(text="Invalid username/password")

    def show_homepage_delayed(self):
        Homepage(self.master)

    def forgot_password(self):
        self.master.withdraw()
        ForgotPasswordWindow(self.master, self)

    def destroy_current_window(self):
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
