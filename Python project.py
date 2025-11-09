import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import math


class PhotoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Gallery & Collage Maker")
        self.root.geometry("1000x750")
        self.root.config(bg="#F3F8FF")

        self.image_list = []
        self.index = 0
        self.selected_paths = []
        self.collage_limit = 12  # limit the number of photos in collage

        self.home_page()

    # ================= HOME PAGE =================
    def home_page(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to Photo App ", font=("Arial Rounded MT Bold", 26),
                 bg="#F3F8FF", fg="#333").pack(pady=80)

        tk.Button(self.root, text=" Open Photo Gallery", command=self.gallery_page,
                  bg="#8FD6E1", font=("Arial", 14), width=25, height=2, relief="ridge").pack(pady=20)

        tk.Button(self.root, text=" Open Collage Maker", command=self.collage_page,
                  bg="#9EE493", font=("Arial", 14), width=25, height=2, relief="ridge").pack(pady=20)

    # ================= GALLERY PAGE =================
    def gallery_page(self):
        self.clear_window()
        self.image_list = []
        self.index = 0

        tk.Label(self.root, text="📸 Photo Gallery", font=("Arial Rounded MT Bold", 22),
                 bg="#F3F8FF", fg="#333").pack(pady=10)

        self.img_label = tk.Label(self.root, bg="#F3F8FF")
        self.img_label.pack(pady=15)

        btn_frame = tk.Frame(self.root, bg="#F3F8FF")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Open Folder", width=15, command=self.open_folder, bg="#9EE493").grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Previous", width=10, command=self.prev_image, bg="#8FD6E1").grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Next", width=10, command=self.next_image, bg="#8FD6E1").grid(row=0, column=2, padx=10)

        tk.Button(self.root, text="⬅ Back to Home", command=self.home_page, bg="#FCA3CC").pack(pady=15)

    def open_folder(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.image_list = [os.path.join(folder, f) for f in os.listdir(folder)
                               if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.index = 0
            if self.image_list:
                self.show_image()

    def show_image(self):
        if self.image_list:
            img_path = self.image_list[self.index]
            img = Image.open(img_path)
            # Keep original aspect ratio
            w, h = img.size
            scale = min(800 / w, 600 / h, 1)
            img = img.resize((int(w * scale), int(h * scale)))
            self.tk_img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.tk_img)
            self.root.title(f"Gallery - {os.path.basename(img_path)}")

    def next_image(self):
        if self.image_list:
            self.index = (self.index + 1) % len(self.image_list)
            self.show_image()

    def prev_image(self):
        if self.image_list:
            self.index = (self.index - 1) % len(self.image_list)
            self.show_image()

    # ================= COLLAGE PAGE =================
    def collage_page(self):
        self.clear_window()

        tk.Label(self.root, text=" Collage Maker", font=("Arial Rounded MT Bold", 22),
                 bg="#F3F8FF", fg="#333").pack(pady=10)

        tk.Button(self.root, text="Select Images", width=15, command=self.create_collage, bg="#9EE493").pack(pady=5)
        tk.Button(self.root, text="Save Collage", width=15, command=self.save_collage, bg="#8FD6E1").pack(pady=5)

        self.limit_label = tk.Label(self.root, text=f"Selected: 0 / {self.collage_limit}",
                                    font=("Arial", 12), bg="#F3F8FF", fg="#555")
        self.limit_label.pack(pady=5)

        self.collage_frame = tk.Frame(self.root, bg="#E9F1FA")
        self.collage_frame.pack(pady=15)

        tk.Button(self.root, text="⬅ Back to Home", command=self.home_page, bg="#FCA3CC").pack(pady=15)

    def create_collage(self):
        for widget in self.collage_frame.winfo_children():
            widget.destroy()

        file_paths = filedialog.askopenfilenames(
            title="Select Images for Collage",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )

        if not file_paths:
            return

        self.selected_paths = list(file_paths)[:self.collage_limit]  # apply limit

        count = len(self.selected_paths)
        self.limit_label.config(text=f"Selected: {count} / {self.collage_limit}")

        # Display collage thumbnails
        for i, path in enumerate(self.selected_paths):
            img = Image.open(path)
            img.thumbnail((150, 150))
            tk_img = ImageTk.PhotoImage(img)

            lbl = tk.Label(self.collage_frame, image=tk_img, bg="#E9F1FA")
            lbl.image = tk_img
            lbl.grid(row=i // 4, column=i % 4, padx=10, pady=10)

    def save_collage(self):
        if not self.selected_paths:
            messagebox.showwarning("No Images", "Please select images first!")
            return

        images = [Image.open(p) for p in self.selected_paths]
        count = len(images)
        cols = min(4, math.ceil(math.sqrt(count)))
        rows = math.ceil(count / cols)

        width = max(img.width for img in images)
        height = max(img.height for img in images)
        collage_width = cols * width
        collage_height = rows * height

        collage_img = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))

        for i, img in enumerate(images):
            x = (i % cols) * width
            y = (i // cols) * height
            collage_img.paste(img.resize((width, height)), (x, y))

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")],
                                                 title="Save Collage As")
        if save_path:
            collage_img.save(save_path)
            messagebox.showinfo("Saved", f"Collage saved successfully!\n{save_path}")

    # ================= HELPER =================
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Run App
root = tk.Tk()
app = PhotoApp(root)
root.mainloop()

