import tkinter as tk
from tkinter import Entry, Button, StringVar, Toplevel

class ChangePasswordWindow(tk.Toplevel):
    new_password = None
    confirm_new_password = None

    def __init__(self, master, change_password_callback):
        super().__init__(master)
        self.title("Change Password")
        self.geometry("400x200")
        self.configure(bg="#232831")

        self.old_password_label = tk.Label(self, text="Old Password: ", font=('Century Gothic', 12), bg="#232831", fg="white")
        self.old_password_label.pack()

        self.old_password_entry = Entry(self, show="*", font=('Century Gothic', 12))
        self.old_password_entry.pack()

        self.new_password_label = tk.Label(self, text="New Password: ", font=('Century Gothic', 12), bg="#232831", fg="white")
        self.new_password_label.pack()

        self.new_password_entry = Entry(self, show="*", font=('Century Gothic', 12))
        self.new_password_entry.pack()

        self.confirm_new_password_label = tk.Label(self, text="Confirm New Password: ", font=('Century Gothic', 12), bg="#232831", fg="white")
        self.confirm_new_password_label.pack()

        self.confirm_new_password_entry = Entry(self, show="*", font=('Century Gothic', 12))
        self.confirm_new_password_entry.pack()

        self.change_password_button = Button(self, text="Change Password", command=change_password_callback, font=('Century Gothic', 12))
        self.change_password_button.pack()

    @classmethod
    def get_new_password(cls):
        return cls.new_password

    @classmethod
    def get_confirm_new_password(cls):
        return cls.confirm_new_password
