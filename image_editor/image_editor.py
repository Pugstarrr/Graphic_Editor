from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, window):
        self.window = window
        self.window.title("Фото редактор")
        self.window.config(bg="#FFFFFF") 
        self.canvas = Canvas(self.window, width=400, height=400, bg="#F5F5F5")
        self.canvas.pack(fill=BOTH, expand=True, padx=20, pady=20) 
        self.image_file = None
        self.image = None
        self.image_tk = None
        self.undo_stack = []
        self.redo_stack = []
        # кнопки
        open_icon = ImageTk.PhotoImage(Image.open("buttons/open.png"))
        self.open_button = Button(self.window, image=open_icon, command=self.open_image, bd=0)
        self.open_button.image = open_icon
        self.open_button.pack(side=LEFT, padx=10, pady=5)

        undo_icon = ImageTk.PhotoImage(Image.open("buttons/undo.png"))
        self.undo_button = Button(self.window, image=undo_icon, command=self.undo, bd=0)
        self.undo_button.image = undo_icon
        self.undo_button.pack(side=LEFT, padx=10, pady=5)

        redo_icon = ImageTk.PhotoImage(Image.open("buttons/redo.png"))
        self.redo_button = Button(self.window, image=redo_icon, command=self.redo, bd=0)
        self.redo_button.image = redo_icon
        self.redo_button.pack(side=LEFT, padx=10, pady=5)
        
        save_icon = ImageTk.PhotoImage(Image.open("buttons/save.png"))
        self.save_button = Button(self.window, image=save_icon, command=self.save_image, bd=0)
        self.save_button.image = save_icon
        self.save_button.pack(side=LEFT, padx=10, pady=5)



        rotate_icon = ImageTk.PhotoImage(Image.open("buttons/rotate.png"))
        self.rotate_button = Button(self.window, image=rotate_icon, command=self.rotate_image, bd=0)
        self.rotate_button.image = rotate_icon
        self.rotate_button.pack(side=LEFT, padx=10, pady=5)

        flip_icon = ImageTk.PhotoImage(Image.open("buttons/flip.png"))
        self.flip_button = Button(self.window, image=flip_icon, command=self.flip_image, bd=0)
        self.flip_button.image = flip_icon
        self.flip_button.pack(side=LEFT, padx=10, pady=5)

        black_white_icon = ImageTk.PhotoImage(Image.open("buttons/black_white.png"))
        self.black_and_white_button = Button(self.window, image=black_white_icon, command=self.black_and_white_image, bd=0)
        self.black_and_white_button.image = black_white_icon
        self.black_and_white_button.pack(side=LEFT, padx=10, pady=5)

        crop_icon = ImageTk.PhotoImage(Image.open("buttons/crop.png"))
        self.crop_button = Button(self.window, image=crop_icon, command=self.crop_image, bd=0)
        self.crop_button.image = crop_icon
        self.crop_button.pack(side=LEFT, padx=10, pady=5)

        add_text_icon = ImageTk.PhotoImage(Image.open("buttons/add_text.png"))
        self.add_text_button = Button(self.window, image=add_text_icon, command=self.add_text, bd=0)
        self.add_text_button.image = add_text_icon
        self.add_text_button.pack(side=LEFT, padx=10, pady=5)




    def open_image(self):
        # открытие изображения
        
        filename = filedialog.askopenfilename(title="Выберите файл",
                                              filetypes=(("jpeg файлы", "*.jpg"), ("png файлы", "*.png")))
        if filename:
            self.undo_stack.append(self.image.copy() if self.image else None)  
            self.redo_stack.clear()
            self.image_file = filename
            self.image = Image.open(filename)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

    def save_image(self):
        # Сох файл

        if self.image_file and self.image:
            defaultextension = ""
            filetype = ""
            selectedtype = self.image_file.split('.')[-1]
            if selectedtype.lower() == "jpg" or selectedtype.lower() == "jpeg":
                defaultextension = ".jpg"
                filetype = (("JPEG файлы", "*.jpg"),)
            elif selectedtype.lower() == "png":
                defaultextension = ".png"
                filetype = (("PNG файлы", "*.png"),)
            else:
                defaultextension = ".jpg"
                filetype = (("JPEG файлы", "*.jpg"), ("PNG файлы", "*.png"), ("Все файлы", "*.*"))
            filename = filedialog.asksaveasfilename(initialdir="/", title="Сохранить файл как",defaultextension=defaultextension,
                                                    filetypes=filetype)
            if filename:
                if self.image.mode == 'RGBA':
                    self.image = self.image.convert('RGB')
                elif self.image.mode == 'P':
                    self.image = self.image.convert('RGB')
                if filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    self.image.save(filename, 'JPEG', quality=90)
                elif filename.endswith('.png'):
                    self.image.save(filename, 'PNG')
                else:
                    messagebox.showerror("Ошибка!", "Неподдерживаемый формат")


    def perform_resize(self, width_percent, height_percent):
        # масштабирование изображения
        if self.image:
            self.undo_stack.append(self.image.copy())
            width = int(self.image.width * width_percent / 100)
            height = int(self.image.height * height_percent / 100)
            self.image = self.image.resize((width, height))
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

    def rotate_image(self):
        # поворот изображения
        if self.image:
            self.undo_stack.append(self.image.copy())
            self.redo_stack.clear()
            self.image = self.image.rotate(90)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

    def flip_image(self):
        #  зеркальное отражение
        if self.image:
            self.undo_stack.append(self.image.copy())
            self.redo_stack.clear()
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

    def black_and_white_image(self):
        # черно-белое фото
        if self.image:
            self.undo_stack.append(self.image.copy())
            self.redo_stack.clear()
            self.image = self.image.convert('L')
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

    def crop_image(self):
        # обрезка размера
        if self.image:
            self.undo_stack.append(self.image.copy())
            self.redo_stack.clear()
            self.canvas.bind("<Button-1>", self.start_crop)

    def start_crop(self, event):
        # начало операции
        self.crop_coords = [event.x, event.y]
        self.canvas.bind("<B1-Motion>", self.draw_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

    def draw_crop(self, event):
        # рисование
        if hasattr(self, "crop_rectangle"):
            self.canvas.delete(self.crop_rectangle)
        x0, y0 = self.crop_coords
        x1, y1 = event.x, event.y
        self.crop_rectangle = self.canvas.create_rectangle(x0, y0, x1, y1, outline="red")

    def end_crop(self, event):
        # определение размера
        x0, y0 = self.crop_coords
        x1, y1 = event.x, event.y
        crop_region = (x0, y0, x1, y1)
        cropped_image = self.image.crop(crop_region)
        self.image = cropped_image
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
        self.canvas.delete(self.crop_rectangle)
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def add_text(self):
        # добавление надписей
        if self.image:
            self.undo_stack.append(self.image.copy())
            self.redo_stack.clear()
            self.canvas.bind("<Button-1>", self.add_text_callback)

    def add_text_callback(self, event):
        # определение позиции для текста
        text_window = Toplevel()
        text_window.geometry("300x250")
        text_label = Label(text_window, text="Введите текст надписи")
        text_label.pack()
        text_entry = Entry(text_window)
        text_entry.pack()

        # выбор цвета текста и размера шрифта
        font_color_label = Label(text_window, text="Цвет текста")
        font_color_label.pack()
        self.font_color = StringVar()
        self.font_color.set("white")
        font_color_menu = OptionMenu(text_window, self.font_color, "white", "black", "red", "green", "blue")
        font_color_menu.pack()

        font_size_label = Label(text_window, text="Размер шрифта")
        font_size_label.pack()
        self.font_size = StringVar()
        self.font_size.set("12")
        font_size_menu = OptionMenu(text_window, self.font_size, "10", "12", "14", "16", "20", "24", "30")
        font_size_menu.pack()

        add_button = Button(text_window, text="Добавить надпись",
                            command=lambda: self.perform_add_text(text_entry.get(), event))
        add_button.pack()

    def perform_add_text(self, text, event):
        # добавление надписи
        if self.image:
            self.undo_stack.append(self.image.copy())
            self.redo_stack.clear()
            x, y = event.x, event.y
            font_color = self.font_color.get()
            font_size = int(self.font_size.get())
            self.canvas.create_text(x, y, text=text, fill=font_color, font=("Arial", font_size))


    def undo(self): # отмена действия
        if self.undo_stack:
            self.redo_stack.append(self.image.copy() if self.image else None)
            self.image = self.undo_stack.pop()
            if self.image:
                self.image_tk = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
            else:
                self.canvas.delete("all")

    def redo(self): # восстановление действия
        if self.redo_stack:
            self.undo_stack.append(self.image.copy() if self.image else None)
            self.image = self.redo_stack.pop()
            if self.image:
                self.image_tk = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
            else:
                self.canvas.delete("all")



root = Tk()
editor = ImageEditor(root)
root.mainloop()
