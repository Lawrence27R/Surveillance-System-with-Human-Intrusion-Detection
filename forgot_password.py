import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

class ForgotPasswordWindow(tk.Toplevel):
    def __init__(self, master, login_window):
        super().__init__(master)
        self.login_window = login_window
        self.title("Forgot Password")
        self.geometry("600x400+400+200")

        style = ThemedStyle(self)
        style.set_theme("arc")

        self.configure(bg="#2E3B4E")

        tk.Label(self, text="Enter your Username and Email", font=('Century Gothic', 16), bg="#2E3B4E", fg="white").place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.username_entry = ttk.Entry(self, font=("Helvetica", 12), width=28)
        self.username_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER, height=30, bordermode="inside")
        self.add_placeholder(self.username_entry, "Username")

        self.email_entry = ttk.Entry(self, font=("Helvetica", 12), width=28)
        self.email_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=30, bordermode="inside")
        self.add_placeholder(self.email_entry, "Email")

        send_button = tk.Button(self, text="Send", command=self.send_password_reset, font=('Helvetica', 12), width=15, foreground="white", background="#232831")
        send_button.place(relx=0.5, rely=0.7, height=30, anchor=tk.CENTER)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, entry, placeholder))

    def on_entry_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry["style"] = "TEntry"  # Apply the default style

    def on_entry_focus_out(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry["style"] = "Placeholder.TEntry"  # Apply the placeholder style

    def send_password_reset(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        # Add logic to send a password reset email (not implemented in this example)
        print(f"Send password reset for {username} to {email}")
        self.destroy()
        self.login_window.master.deiconify()

    def on_close(self):
        self.destroy()
        self.login_window.master.deiconify()
