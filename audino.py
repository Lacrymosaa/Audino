import tkinter as tk
from tkinter import filedialog
import playlist_generator
import recommendations

class AudinoApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Audino")
        self.master.iconbitmap("imgs/audino.ico")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.genre_label = tk.Label(self, text="Gênero:")
        self.genre_label.grid(row=0, column=0)
        self.genre_entry = tk.Entry(self)
        self.genre_entry.grid(row=0, column=1)

        self.duration_label = tk.Label(self, text="Duração (minutos):")
        self.duration_label.grid(row=1, column=0)
        self.duration_entry = tk.Entry(self)
        self.duration_entry.grid(row=1, column=1)

        self.popularity_label = tk.Label(self, text="Popularidade:")
        self.popularity_label.grid(row=2, column=0)
        self.popularity_entry = tk.Entry(self)
        self.popularity_entry.grid(row=2, column=1)

        self.generate_button = tk.Button(self, text="Gerar Playlist", command=self.generate_playlist)
        self.generate_button.grid(row=3, column=1)

        self.quit_button = tk.Button(self, text="Sair", command=self.master.destroy)
        self.quit_button.grid(row=3, column=0)

        self.recommendations_label = tk.Label(self, text="Coloque apenas a duração -->")
        self.recommendations_label.grid(row=4, column=0)
        self.recommendations_button = tk.Button(self, text="Recomendados", command=self.generate_with_recommendations)
        self.recommendations_button.grid(row=4, column=1)

    def generate_playlist(self):
        genre = self.genre_entry.get()
        duration = int(self.duration_entry.get())
        popularity = int(self.popularity_entry.get())
        playlist_generator.generate_playlist(genre, duration, popularity)

    def generate_with_recommendations(self):
        duration = int(self.duration_entry.get())
        recommendations.generate_with_recommendations(duration)

root = tk.Tk()
app = AudinoApp(master=root)
app.mainloop()