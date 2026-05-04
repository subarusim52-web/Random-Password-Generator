import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.root.geometry("600x550")

        self.history_file = "password_history.json"
        self.history = self.load_history()

        # Переменные настроек
        self.length_var = tk.IntVar(value=12)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_numbers = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        self.create_widgets()
        self.populate_history()

    def create_widgets(self):
        # Фрейм настроек
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)

        # Длина пароля
        length_frame = ttk.Frame(settings_frame)
        length_frame.pack(fill=tk.X, pady=5)
        ttk.Label(length_frame, text="Длина пароля:").pack(side=tk.LEFT)
        
        self.length_label = ttk.Label(length_frame, text=str(self.length_var.get()))
        self.length_label.pack(side=tk.RIGHT, padx=5)

        self.length_slider = ttk.Scale(length_frame, from_=4, to=64, orient=tk.HORIZONTAL, 
                                       variable=self.length_var, command=self.update_length_label)
        self.length_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)

        # Чекбоксы символов
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(options_frame, text="A-Z", variable=self.use_uppercase).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="a-z", variable=self.use_lowercase).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="0-9", variable=self.use_numbers).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="!@#$%", variable=self.use_symbols).pack(side=tk.LEFT, padx=5)

        # Фрейм генерации
        gen_frame = ttk.Frame(self.root, padding=10)
        gen_frame.pack(fill=tk.X, padx=10, pady=5)

        self.result_entry = ttk.Entry(gen_frame, font=("Courier", 14), justify="center")
        self.result_entry.pack(fill=tk.X, pady=5)

        ttk.Button(gen_frame, text="Сгенерировать", command=self.generate_password).pack(pady=5)

        # Фрейм истории
        history_frame = ttk.LabelFrame(self.root, text="История генераций", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(history_frame, columns=("date", "password"), show="headings")
        self.tree.heading("date", text="Дата и время")
        self.tree.heading("password", text="Пароль")
        self.tree.column("date", width=150, anchor=tk.CENTER)
        self.tree.column("password", width=350, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_length_label(self, event=None):
        # Преобразуем значение ползунка в целое число
        length = int(self.length_var.get())
        self.length_var.set(length)
        self.length_label.config(text=str(length))

    def generate_password(self):
        length = self.length_var.get()
        
        # Проверка длины (минимальная/максимальная)
        if not (4 <= length <= 64):
            messagebox.showerror("Ошибка", "Длина пароля должна быть от 4 до 64 символов.")
            return

        chars = ""
        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_lowercase.get():
            chars += string.ascii_lowercase
        if self.use_numbers.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Генерация пароля
        password = "".join(random.choice(chars) for _ in range(length))
        
        # Обновление поля результата
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)

        # Сохранение в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({"date": timestamp, "password": password})
        self.save_history()
        
        # Обновление таблицы (добавляем в начало списка)
        self.tree.insert("", 0, values=(timestamp, password))

    def populate_history(self):
        for item in reversed(self.history):
            self.tree.insert("", tk.END, values=(item["date"], item["password"]))

    def load_history(self):
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()