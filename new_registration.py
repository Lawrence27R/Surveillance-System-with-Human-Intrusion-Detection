import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from mysql_db import initialize_connection
import shutil
from capture_images import capture_images

class NewRegistrationSection(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#232831", padx=40, pady=20)
        self.user_id_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.data_entries = []
        self.initialize_connection()
        self.create_registration_widgets()
        self.create_table()
        self.create_train_widgets()
        self.create_delete_button()

    def initialize_connection(self):
        self.conn, self.cursor = initialize_connection()

    def create_registration_widgets(self):
        title_label = tk.Label(self, text="Register New User:", font=('Century Gothic', 16, 'bold'), bg="#232831", fg="white", pady=8)
        title_label.grid(row=0, column=0, columnspan=3, sticky="w")

        user_id_label = tk.Label(self, text="User ID:", font=('Century Gothic', 12), bg="#232831", fg="white")
        user_id_label.grid(row=1, column=0, pady=6, sticky="w")
        user_id_entry = tk.Entry(self, textvariable=self.user_id_var, font=('Century Gothic', 12))
        user_id_entry.grid(row=1, column=1, pady=6, sticky="w")

        username_label = tk.Label(self, text="Username:", font=('Century Gothic', 12), bg="#232831", fg="white")
        username_label.grid(row=2, column=0, pady=6, sticky="w")
        username_entry = tk.Entry(self, textvariable=self.username_var, font=('Century Gothic', 12))
        username_entry.grid(row=2, column=1, pady=6, padx=4, sticky="w")

        capture_button = tk.Button(
            self,
            text="Capture Images",
            command=self.capture_images,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        capture_button.grid(row=3, column=0, pady=(10, 20), sticky="w")

        or_label = tk.Label(self, text="                    OR ", font=('Century Gothic', 12), bg="#232831", fg="white")
        or_label.grid(row=3, column=1, pady=6, sticky="w")

        upload_button = tk.Button(
            self,
            text="Upload Images",
            command=self.upload_images,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        upload_button.grid(row=3, column=2, pady=(10, 20), padx=5, sticky="w")

    def create_table(self):
        headers = ["User ID", "Username"]
        self.table = ttk.Treeview(self, columns=headers, show="headings", selectmode="browse", height=11)
        for header in headers:
            self.table.heading(header, text=header)
            self.table.column(header, width=200)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.grid(row=4, column=0, columnspan=3, pady=8, sticky="w")
        scrollbar.grid(row=4, column=3, pady=8, sticky="ns")
        self.table.bind("<Delete>", self.delete_selected_entry)

    def create_delete_button(self):
        delete_button = tk.Button(
            self,
            text="Delete Entry",
            command=self.delete_selected_entry,
            bg="#C62828",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        delete_button.grid(row=5, column=0, pady=(8, 25), sticky="w")

    def create_train_widgets(self):
        train_button = tk.Button(
            self,
            text="Train Model",
            command=self.train_model,
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        train_button.grid(row=6, column=0, pady=8, sticky="w")

        training_status_label = tk.Label(self, text="Training status:", font=('Century Gothic', 12), bg="#232831", fg="white")
        training_status_label.grid(row=7, column=0, pady=4, sticky="w")

    def capture_images(self):
        user_id = self.user_id_var.get()
        username = self.username_var.get()
        if not user_id or not username:
            messagebox.showwarning("Incomplete Information", "Please enter User ID and Username.")
            return
        capture_images(user_id, username)
        self.insert_user_into_database(user_id, username)
        self.update_table()

    def insert_user_into_database(self, user_id, username):
        insert_query = "INSERT INTO newreg (user_id, username) VALUES (%s, %s)"
        self.cursor.execute(insert_query, (int(user_id), username))
        self.conn.commit()

    def update_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.data_entries = self.get_data_from_database()
        for entry in self.data_entries:
            self.table.insert("", "end", values=entry)

    def get_data_from_database(self):
        select_query = "SELECT * FROM newreg"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def delete_selected_entry(self, event=None):
        selected_item = self.table.selection()
        if selected_item:
            selected_id = selected_item[0]
            self.delete_user_from_database(selected_id)
            for i, entry in enumerate(self.data_entries):
                if entry[0] == selected_id:
                    del self.data_entries[i]
                    break
            self.update_table()

    def delete_user_from_database(self, user_id):
        folder_path = os.path.join('User_Images', f"{user_id}_{self.username_var.get()}")
        delete_query = "DELETE FROM newreg WHERE user_id = %s"
        try:
            self.cursor.execute(delete_query, (int(user_id),))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Delete Error", f"Error deleting user from the database: {str(e)}")
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)

    def upload_images(self):
        folder_path = filedialog.askdirectory(initialdir="D:/Final Year", title="Select Folder")
        if folder_path:
            os.system(f'explorer "{folder_path}"')

    def train_model(self):
        print("Training the Model")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = NewRegistrationSection(root)
    root.bind("<q>", lambda event: root.destroy())
    root.protocol("WM_DELETE_WINDOW", app.close_connection)
    root.mainloop()
