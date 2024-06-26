import tkinter as tk
from tkinter import Label, Menu, Toplevel
from PIL import Image, ImageTk

class NavigationBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#21252b")

        cctv_logo_path = "gui/images/icons/icons8-cctv-18.png"
        cctv_logo_resized = master.load_and_resize_image(cctv_logo_path, width=33, height=38)
        cctv_logo_label = Label(self, image=cctv_logo_resized, bg="#21252b")
        cctv_logo_label.image = cctv_logo_resized
        cctv_logo_label.pack(side=tk.LEFT, padx=8)

        self.username_label = tk.Label(self, text="", font=('Century Gothic', 12), bg="#21252b", fg="white")
        self.username_label.pack(side=tk.LEFT, expand=True)

        account_icon_path = "gui/images/icons/icons8-test-account-18.png"
        account_icon_resized = master.load_and_resize_image(account_icon_path, width=30, height=30)
        account_label = Label(self, image=account_icon_resized, bg="#21252b")
        account_label.image = account_icon_resized
        account_label.pack(side=tk.RIGHT, padx=0)

        account_menu = Menu(master.master, tearoff=0)
        account_menu.add_command(label="Username")
        account_menu.add_command(label="Change Password", command=master.open_change_password_window)
        account_menu.add_separator()
        account_menu.add_command(label="Logout", command=master.logout)

        def show_menu(event):
            account_menu.post(event.x_root, event.y_root)

        account_label.bind("<Button-1>", show_menu)

        about_us_label = tk.Label(self, text="About Us", font=('Century Gothic', 12), bg="#21252b", fg="white")
        about_us_label.pack(side=tk.RIGHT, padx=0)
        about_us_label.bind("<Button-1>", self.show_about_us)

        about_project_label = tk.Label(self, text="About Project", font=('Century Gothic', 12), bg="#21252b", fg="white")
        about_project_label.pack(side=tk.RIGHT, padx=0)
        about_project_label.bind("<Button-1>", self.show_about_project)

        self.pack(fill=tk.X, side=tk.TOP)

        cctv_logo_label.pack(side=tk.LEFT, padx=6)
        self.username_label.pack(side=tk.LEFT, expand=True, padx=0)
        account_label.pack(side=tk.RIGHT, padx=12)

    def show_about_project(self, event):
        about_project_window = Toplevel(self.master.master)
        about_project_window.title("About Project")
        about_project_label = tk.Label(about_project_window, text="Information about the project goes here.")
        about_project_label.pack(padx=20, pady=20)

    def show_about_us(self, event):
        about_us_window = Toplevel(self.master.master)
        about_us_window.title("About Us")
        about_us_label = tk.Label(about_us_window, text="Information about us goes here.")
        about_us_label.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    navbar = NavigationBar(root)
    navbar.pack(fill=tk.X, side=tk.TOP)
    root.mainloop()
