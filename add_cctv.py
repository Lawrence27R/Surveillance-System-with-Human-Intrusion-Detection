import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.font as tkFont
import tkinter.ttk as ttk

class AddCCTVSection(tk.Frame):
    def __init__(self, master, conn, cursor):
        super().__init__(master, bg="#232831")
        self.conn = conn
        self.cursor = cursor

        self.create_cctv_form()
        self.create_cctv_table()
        self.load_cctv_table()

    def create_cctv_form(self):
        form_frame = tk.Frame(self, bg="#232831")
        form_frame.pack(side=tk.LEFT, padx=20, pady=20, anchor="w")

        tk.Label(form_frame, text="CCTV Number:", font=('Century Gothic', 12), bg="#232831", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="CCTV IP Address:", font=('Century Gothic', 12), bg="#232831", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.cctv_number_entry = tk.Entry(form_frame, font=('Century Gothic', 12))
        self.cctv_ip_entry = tk.Entry(form_frame, font=('Century Gothic', 12))

        self.cctv_number_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.cctv_ip_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        add_button = tk.Button(form_frame, text="Add CCTV", command=self.add_cctv, font=('Century Gothic', 12), bg="#4CAF50", fg="white")
        add_button.grid(row=2, column=0, columnspan=2, pady=(10, 20))  # Add more space to the bottom

    def create_cctv_table(self):
        table_frame = tk.Frame(self, bg="#232831")
        table_frame.pack(side=tk.LEFT, padx=(20, 20), pady=20, anchor="w")

        columns = ("CCTV Number", "CCTV IP Address")
        self.cctv_treeview = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.cctv_treeview.grid(row=0, column=0, columnspan=2, sticky="nsew")

        for col in columns:
            self.cctv_treeview.heading(col, text=col, command=lambda c=col: self.sort_cctv_table(c))

        self.cctv_treeview.column("CCTV Number", width=150)
        self.cctv_treeview.column("CCTV IP Address", width=200)

        delete_button = tk.Button(table_frame, text="Delete", command=self.delete_cctv, font=('Century Gothic', 12), bg="#FF6347", fg="white")
        delete_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))  # Add more space to the top

    def sort_cctv_table(self, column):
        items = [(self.cctv_treeview.set(item, column), item) for item in self.cctv_treeview.get_children("")]
        items.sort()
        for index, (value, item) in enumerate(items):
            self.cctv_treeview.move(item, "", index)

    def add_cctv(self):
        cctv_number = self.cctv_number_entry.get()
        cctv_ip = self.cctv_ip_entry.get()

        if not cctv_number or not cctv_ip:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        self.cursor.execute(f"INSERT INTO cctv (cctv_number, cctv_ip) VALUES ('{cctv_number}', '{cctv_ip}')")
        self.conn.commit()
        self.load_cctv_table()

        self.cctv_number_entry.delete(0, tk.END)
        self.cctv_ip_entry.delete(0, tk.END)

    def load_cctv_table(self):
        try:
            # Clear existing entries in the Treeview
            self.cctv_treeview.delete(*self.cctv_treeview.get_children())

            # Fetch all entries directly in the Treeview insertion
            self.cursor.execute("SELECT cctv_number, cctv_ip FROM cctv")
            cctv_entries = self.cursor.fetchall()

            # Modify the returned dictionary with names as keys and IP addresses as values
            cctv_data = {f"{entry[0]}": entry[1] for entry in cctv_entries}

            for name, ip_address in cctv_data.items():
                self.cctv_treeview.insert("", tk.END, values=(name, ip_address))

            return cctv_data

        except Exception as e:
            print(f"Error loading CCTV table: {e}")
            return None


    def delete_cctv(self):
        selected_item = self.cctv_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a CCTV entry to delete.")
            return

        result = messagebox.askyesno("Delete CCTV", "Are you sure you want to delete the selected CCTV entry?")
        if result:
            cctv_number = self.cctv_treeview.item(selected_item, "values")[0]
            self.cursor.execute(f"DELETE FROM cctv WHERE cctv_number = '{cctv_number}'")
            self.conn.commit()
            self.load_cctv_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = AddCCTVSection(root, None, None)  # Pass None, None for conn and cursor for testing
    root.mainloop()