import tkinter as tk
from tkinter import ttk, messagebox
from gui.mysql_db import DatabaseHandler

class AddDetailsSection(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#232831")
        self.create_user_details_widgets()
        self.initialize_connection()
        self.fetch_details()
        

    def initialize_connection(self):
        self.database = DatabaseHandler()
        self.conn, self.cursor = self.database.initialize_connection()
        self.database.create_add_details_table(self.cursor)

    def create_user_details_widgets(self):
        add_details_label = tk.Label(self, text="ADD DETAILS", font=('Century Gothic', 16, 'bold'), bg="#232831", fg="white", pady=10)
        add_details_label.pack(side=tk.TOP, fill=tk.X)

        email_frame = tk.Frame(self, bg="#232831")
        email_frame.pack(side=tk.TOP, fill=tk.X)

        labels = ["User ID", "User Name", "Email", "Phone Number"]
        entries = []

        for i, label_text in enumerate(labels):
            label = tk.Label(email_frame, text=f"Enter {label_text}:", font=('Century Gothic', 12), bg="#232831", fg="white")
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(email_frame, font=('Century Gothic', 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        add_button = tk.Button(
            email_frame,
            text="Add Details",
            command=lambda: self.add_details([entry.get() for entry in entries]),
            bg="#1565C0",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )
        add_button.grid(row=len(labels), column=0, columnspan=2, pady=30)

        delete_button = tk.Button(
            email_frame,
            text="Delete",
            command=self.delete_selected,
            bg="#C62828",
            fg="white",
            font=("Helvetica", 12),
            relief=tk.FLAT,
        )

        delete_button.grid(row=len(labels) + 1, column=0, columnspan=2)

        tk.Label(self, text="", bg="#232831", pady=1).pack(side=tk.TOP, fill=tk.X)

        self.create_user_details_table()

    def create_user_details_table(self):
        headers = ["User ID", "User Name", "Email", "Phone Number"]

        style = ttk.Style()

        # Configure the heading style
        style.configure("Custom.Treeview.Heading", font=('Helvetica', 12, 'bold'), background="black", fieldbackground="black", foreground="black")

        # Configure the default style
        style.configure("Custom.Treeview", font=('Helvetica', 11), background="white", fieldbackground="white", foreground="black")

        self.tree = ttk.Treeview(self, style="Custom.Treeview", columns=headers, show="headings", selectmode="extended", height=10)

        for header in headers:
            self.tree.column(header, anchor="center")
            self.tree.heading(header, text=header, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.tag_configure("blue", background="blue")

        def on_checkbox_click(event):
            item = self.tree.identify("item", event.x, event.y)
            current_state = self.tree.item(item, "tags")
            new_state = "blue" if "blue" not in current_state else ""
            self.tree.item(item, tags=new_state)

        self.tree.bind("<Button-1>", on_checkbox_click)

        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tk.Label(self, text="", bg="#232831", pady=20).pack(side=tk.TOP, fill=tk.X)

    def add_details(self, details):
        try:
            user_id, user_name, email, phone_number = details[0:]

            query = """
                INSERT INTO add_details (user_id, user_name, email, phone_number)
                VALUES (%s, %s, %s, %s)
            """
            values = (user_id, user_name, email, phone_number)

            self.cursor.execute(query, values)
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error adding details to database: {e}")
            return False
        finally:
            self.fetch_details()  # Update the treeview after adding details

    def delete_selected(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            item_id = self.tree.item(item, "values")[0]  # Assuming the first column is the item ID

        try:
            query = "DELETE FROM add_details WHERE user_id = %s"
            values = (item_id,)

            self.cursor.execute(query, values)
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error deleting details from database: {e}")
            return False
        finally:
            self.fetch_details()  # Update the treeview after deleting details

    def fetch_details(self):
        try:
            self.tree.delete(*self.tree.get_children())  # Clear the existing data in the treeview

            query = "SELECT * FROM add_details"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            print(f"Error fetching details from database: {e}")

    # def delete_selected(self):
    #     selected_items = self.tree.selection()
    #     for item in selected_items:
    #         self.tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = AddDetailsSection(root)
    root.mainloop()
