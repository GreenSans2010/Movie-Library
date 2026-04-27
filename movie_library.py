import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("750x500")

        self.movies = self.load_movies()

        # Поля ввода
        tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_title = tk.Entry(root, width=30)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_genre = tk.Entry(root, width=30)
        self.entry_genre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_year = tk.Entry(root, width=30)
        self.entry_year.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_rating = tk.Entry(root, width=30)
        self.entry_rating.grid(row=3, column=1, padx=5, pady=5)

        btn_add = tk.Button(root, text="Добавить фильм", command=self.add_movie)
        btn_add.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.grid(row=5, column=0, columnspan=2, pady=5)

        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side="left", padx=5)
        self.filter_genre = tk.Entry(filter_frame, width=15)
        self.filter_genre.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Применить", command=self.filter_movies).pack(side="left", padx=5)

        tk.Label(filter_frame, text="Фильтр по году:").pack(side="left", padx=5)
        self.filter_year = tk.Entry(filter_frame, width=15)
        self.filter_year.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Очистить фильтры", command=self.clear_filters).pack(side="left", padx=5)

        # Таблица с фильмами
        self.tree = ttk.Treeview(root, columns=("Название", "Жанр", "Год", "Рейтинг"), show="headings")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.column("Название", width=200)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=80)
        self.tree.column("Рейтинг", width=80)
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=6, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        root.grid_rowconfigure(6, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.refresh_table()

    def load_movies(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_movies(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def validate_year(self, year_str):
        try:
            year = int(year_str)
            return 1900 <= year <= 2026
        except:
            return False

    def validate_rating(self, rating_str):
        try:
            rating = float(rating_str)
            return 0 <= rating <= 10
        except:
            return False

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()

        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        if not self.validate_year(year_str):
            messagebox.showerror("Ошибка", "Год должен быть числом от 1900 до 2026")
            return

        if not self.validate_rating(rating_str):
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return

        year = int(year_str)
        rating = float(rating_str)

        self.movies.append({
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        })
        self.save_movies()
        self.clear_inputs()
        self.refresh_table()

    def clear_inputs(self):
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def refresh_table(self, filtered_movies=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        movies_to_show = filtered_movies if filtered_movies is not None else self.movies
        for movie in movies_to_show:
            self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def filter_movies(self):
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()

        filtered = self.movies[:]
        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]
        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_int]
            except:
                messagebox.showerror("Ошибка", "Год в фильтре должен быть числом")
                return
        self.refresh_table(filtered)

    def clear_filters(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
