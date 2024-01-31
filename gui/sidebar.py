from PIL import Image, ImageTk
import tkinter as tk

class Sidebar(tk.Frame):
    def __init__(self, master, show_username_callback, change_main_content_callback):
        super().__init__(master, bg="#21252b")

        self.master = master
        self.show_username_callback = show_username_callback
        self.change_main_content_callback = change_main_content_callback

        self.create_sidebar_labels()

    def create_sidebar_labels(self):
        logo_paths = {
            "Home": "images/icons/cil-home.png",
            "New Registration": "images/icons/icons8-add-administrator-18.png",
            "Add CCTV": "images/icons/icons8-add-camera-18.png",
            "Add Details": "images/icons/icons8-registration-18.png",
            "REC & LOGS": "images/icons/icons8-recording-18.png",
        }

        for item, logo_path in logo_paths.items():
            logo_image = self.load_and_resize_image(logo_path, width=20, height=20)
            label = tk.Label(
                self,
                text=item,
                image=logo_image,
                compound="left",
                font=('Century Gothic', 12),
                bg="#21252b",
                fg="white",
                padx=16,
                pady=20,
                anchor="w",
            )
            label.image = logo_image
            label.bind("<Button-1>", lambda event, item=item: self.change_main_content_callback(item))
            label.pack(side=tk.TOP, fill=tk.X)

    def show_username(self, username):
        self.username_label.config(text=f"Username: {username}")

    def load_and_resize_image(self, image_path, width=None, height=None):
        try:
            original_image = Image.open(image_path)
            if width and height:
                resized_image = original_image.resize((width, height), Image.LANCZOS)
                return ImageTk.PhotoImage(resized_image)
            else:
                return ImageTk.PhotoImage(original_image)
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    sidebar = Sidebar(root, None, None)
    sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    root.mainloop()
