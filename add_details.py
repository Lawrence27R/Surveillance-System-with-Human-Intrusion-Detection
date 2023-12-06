import tkinter as tk
from tkinter import ttk, messagebox

class AddDetailsSection(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#232831")
        self.create_user_details_widgets()

    def create_user_details_widgets(self):
        add_email_label = tk.Label(self, text="ADD DETAILS", font=('Century Gothic', 16, 'bold'), bg="#232831", fg="white", pady=10)
        add_email_label.pack(side=tk.TOP, fill=tk.X)

        email_frame = tk.Frame(self, bg="#232831")
        email_frame.pack(side=tk.TOP, fill=tk.X)

        email_id_label = tk.Label(email_frame, text="Enter user id:", font=('Century Gothic', 12), bg="#232831", fg="white")
        email_id_label.grid(row=0, column=0, padx=10, pady=5)

        email_id_entry = tk.Entry(email_frame, font=('Century Gothic', 12))
        email_id_entry.grid(row=0, column=1, padx=10, pady=5)

        user_name_label = tk.Label(email_frame, text="Enter user name:", font=('Century Gothic', 12), bg="#232831", fg="white")
        user_name_label.grid(row=1, column=0, padx=10, pady=5)

        user_name_entry = tk.Entry(email_frame, font=('Century Gothic', 12))
        user_name_entry.grid(row=1, column=1, padx=10, pady=5)

        email_label = tk.Label(email_frame, text="Enter email:", font=('Century Gothic', 12), bg="#232831", fg="white")
        email_label.grid(row=2, column=0, padx=10, pady=5)

        email_entry = tk.Entry(email_frame, font=('Century Gothic', 12))
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        phone_number_label = tk.Label(email_frame, text="Enter phone number:", font=('Century Gothic', 12), bg="#232831", fg="white")
        phone_number_label.grid(row=3, column=0, padx=10, pady=5)

        phone_number_entry = tk.Entry(email_frame, font=('Century Gothic', 12))
        phone_number_entry.grid(row=3, column=1, padx=10, pady=5)

        add_email_button = tk.Button(
            email_frame,
            text="Add Details",
            command=lambda: self.add_email(
                email_id_entry.get(),
                user_name_entry.get(),
                email_entry.get(),
                phone_number_entry.get()
            ),
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        add_email_button.grid(row=4, column=0, columnspan=2, pady=30)

        delete_button = tk.Button(
            email_frame,
            text="Delete",
            command=self.delete_selected,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        delete_button.grid(row=5, column=0, columnspan=2)

        tk.Label(self, text="", bg="#232831", pady=1).pack(side=tk.TOP, fill=tk.X)

        self.create_user_details_table()

    def create_user_details_table(self):
        headers = ["Select", "User ID", "User Name", "Email", "Phone Number"]

        style = ttk.Style()
        style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])
        style.configure("Custom.Treeview.Heading", font=('Helvetica', 12), background="blue", fieldbackground="blue", foreground="white")
        style.configure("Custom.Treeview", font=('Helvetica', 11), background="#232831", fieldbackground="#232831", foreground="white")

        self.tree = ttk.Treeview(self, style="Custom.Treeview", columns=headers, show="headings", selectmode="extended", height=10)

        for header in headers:
            self.tree.column(header, anchor="center")
            self.tree.heading(header, text=header, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.column("#0", width=50, anchor="center", stretch=tk.NO)
        self.tree.heading("#0", text="Select")

        self.tree.tag_configure("blue", background="blue")

        def on_checkbox_click(event):
            item = self.tree.identify("item", event.x, event.y)
            current_state = self.tree.item(item, "tags")
            new_state = "blue" if "blue" not in current_state else ""
            self.tree.item(item, tags=new_state)

        self.tree.bind("<Button-1>", on_checkbox_click)

        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tk.Label(self, text="", bg="#232831", pady=20).pack(side=tk.TOP, fill=tk.X)

    def add_email(self, user_id, user_name, email, phone_number):
        self.tree.insert("", "end", values=["", user_id, user_name, email, phone_number])

    def delete_selected(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = AddDetailsSection(root)
    root.mainloop()
