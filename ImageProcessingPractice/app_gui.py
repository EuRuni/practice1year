import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import cv2
import image_utils as iu

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        self.image = None
        self.original_image = None

        self.canvas = tk.Label(self.root)
        self.canvas.pack()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Загрузить изображение", command=self.load_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Сделать снимок", command=self.capture_image).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="В оттенки серого", command=self.to_grayscale).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Показать фильтр RGB", command=self.open_rgb_filter_window).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Повернуть изображение", command=self.open_rotate_window).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Нарисовать прямоугольник", command=self.open_rectangle_window).grid(row=0, column=5, padx=5)
        tk.Button(btn_frame, text="Сбросить изображение", command=self.reset_image).grid(row=0, column=6, padx=5)
        tk.Button(btn_frame, text="Выйти", command=self.root.quit).grid(row=0, column=7, padx=5)

    def load_image(self):
        self.image = iu.select_image()
        if self.image is not None:
            self.original_image = self.image.copy()
            self.show_image(self.image)

    def capture_image(self):
        self.image = iu.capture_from_webcam()
        if self.image is not None:
            self.original_image = self.image.copy()
            self.show_image(self.image)

    def to_grayscale(self):
        if self.original_image is None:
            messagebox.showerror("Ошибка", "Сначала загрузите изображение.")
            return
        self.image = iu.convert_to_grayscale(self.original_image)
        self.show_image(self.image)

    def open_rgb_filter_window(self):
        if self.original_image is None:
            messagebox.showerror("Ошибка", "Сначала загрузите изображение.")
            return

        win = tk.Toplevel(self.root)
        win.title("Выбор фильтра RGB")
        tk.Button(win, text="Красный канал", command=lambda: self.apply_channel(win, 'R')).pack(padx=10, pady=5)
        tk.Button(win, text="Зеленый канал", command=lambda: self.apply_channel(win, 'G')).pack(padx=10, pady=5)
        tk.Button(win, text="Синий канал", command=lambda: self.apply_channel(win, 'B')).pack(padx=10, pady=5)

    def apply_channel(self, window, channel):
        if self.original_image is None:
            messagebox.showerror("Ошибка", "Нет исходного изображения для применения фильтра.")
            return
        channel_img = iu.get_channel_image(self.original_image, channel)
        if channel_img is not None:
            self.image = channel_img
            self.show_image(self.image)
            window.destroy()
        else:
            messagebox.showerror("Ошибка", "Неверный канал.")

    def open_rotate_window(self):
        if self.image is None:
            messagebox.showerror("Ошибка", "Сначала загрузите изображение.")
            return

        angle = simpledialog.askfloat("Поворот", "Введите угол поворота (в градусах):", parent=self.root)
        if angle is not None:
            self.image = iu.rotate_image(self.image, angle)
            self.show_image(self.image)

    def open_rectangle_window(self):
        if self.image is None:
            messagebox.showerror("Ошибка", "Сначала загрузите изображение.")
            return

        win = tk.Toplevel(self.root)
        win.title("Введите координаты прямоугольника")

        labels = ["x1:", "y1:", "x2:", "y2:"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        def draw():
            try:
                x1, y1, x2, y2 = [int(e.get()) for e in entries]
                self.image = iu.draw_rectangle(self.image, x1, y1, x2, y2)
                self.show_image(self.image)
                win.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите целые числа для координат.")

        tk.Button(win, text="Нарисовать", command=draw).grid(row=4, column=0, columnspan=2, pady=10)

    def reset_image(self):
        if self.original_image is None:
            messagebox.showerror("Ошибка", "Нет изображения для сброса.")
            return
        self.image = self.original_image.copy()
        self.show_image(self.image)

    def show_image(self, img_cv):
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.canvas.config(image=img_tk)
        self.canvas.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
