import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import os
import mysql_db
from change_password import ChangePasswordWindow
from navbar import NavigationBar
from rec_and_logs import RecAndLogsSection
from new_registration import NewRegistrationSection
from add_details import AddDetailsSection
from add_cctv import AddCCTVSection
from sidebar import Sidebar
from homecontent import HomeContent

class Homepage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Surveillance System with Human Intrusion Detection")
        self.master.geometry("1400x720+0+0")

        style = ThemedStyle(self.master)
        style.set_theme("arc")

        self.configure(bg="#232831")

        self.navbar = NavigationBar(self)
        self.navbar.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0) 

        self.sidebar_frame = tk.Frame(self, bg="#21252b", bd=2, relief=tk.SUNKEN)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.sidebar = Sidebar(self, self.show_username, self.change_main_content)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        tk.Frame(self.sidebar_frame, width=2, bg="#21252b").pack(side=tk.LEFT, fill=tk.Y)

        self.main_content = tk.Frame(self, bg="#232831")
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.pack(fill=tk.BOTH, expand=True)

        self.conn, self.cursor = mysql_db.initialize_connection()
        self.logged_in_email = "rootuser@gmail.com"

        self.rec_and_logs_section = RecAndLogsSection(self.main_content)
        self.new_registration_section = NewRegistrationSection(self.main_content)
        self.add_details_section = AddDetailsSection(self.main_content)

        self.home_content = HomeContent(self.main_content)
        self.current_section = None  # Initialize current_section to None

        self.show_section(self.home_content)  # Show home_content by default

    def show_username(self):
        self.cursor.execute(f"SELECT email FROM users WHERE email = '{self.logged_in_email}'")
        result = self.cursor.fetchone()
        if result:
            self.sidebar.show_username(result[0])
        else:
            self.sidebar.show_username("Username not found")

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
            self.show_section(AddCCTVSection(self.main_content, self.conn, self.cursor))
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

if __name__ == "__main__":
    root = tk.Tk()
    app = Homepage(root)
    root.mainloop()
