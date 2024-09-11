import tkinter as tk
from tkinter import *
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Le jeu de la vie")
        self.geometry("800x600")

        # Config bouton Quitter
        self.button_quit = ttk.Button(self, text="Quitter")
        self.button_quit['command'] = self.destroy
        self.button_quit.grid(column=1, row=0)

        # Config bouton Reset grille
        self.button_reset = ttk.Button(self, text="Réinitialiser")
        self.button_reset['command'] = self.reset_grid
        self.button_reset.grid(column=1, row=1)

    # Passe toutes les cell de la grid sur dead
    def reset_grid(self):
        print('Fonction reset call')
        for instance in Cell.instances.values():
            instance.kill_cell()

class MainFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.grid()


class MainGrid(ttk.Frame):

    def __init__(self, container):
        size_grid = 200
        super().__init__(container)
        self.canvas = Canvas(container, width=size_grid, height=size_grid, background='gray')
        self.canvas.grid()

        # Créé la grille et l'a remplie de cellule morte
        for i in range(0, size_grid, 20):
            for j in range(0, size_grid, 20):
                self.canvas.create_rectangle(i, j, (i + 20), (j + 20), width=1)
                self.canvas.create_window(i + 10, j + 10, window=Cell(self.canvas, is_alive=False))


class Cell(ttk.Frame):

    # Liste des cellules se trouvant sur la grid
    instances = {}

    def __init__(self, container, is_alive):
        super().__init__(container)

        self.instances[self.winfo_id()] = self
        self.is_alive = is_alive
        self.config(width=19)  # largeur de la cellule
        self.config(height=19)  # hauteur de la cellule
        self.bind("<Button-1>", self.on_click_cell)
        self.update_state()

    # Supprime la cellule du tableau si elle est supprimé de la grid
    def __del__(self):
        del self.instances[self]

    # Configure la cellule selon son état
    def update_state(self):
        # Styles de cellule
        cell_style = ttk.Style()
        cell_style.configure('CellB.TFrame', background='black')
        cell_style.configure('CellG.TFrame', background='grey')

        if self.is_alive:
            self.config(style='CellB.TFrame')
        else:
            self.config(style='CellG.TFrame')

    # Inverse l'état de la cellule (alive/dead)
    def toggle_state(self):
        self.is_alive = not self.is_alive
        self.update_state()

    # Passe l'état d'une cellule sur dead
    def kill_cell(self):
        self.is_alive = False
        self.update_state()

    # Passe l'état d'une cellule sur alive
    def live_cell(self):
        self.is_alive = True
        self.update_state()
    
    # Déclenché au clic sur une cellule
    def on_click_cell(self, event):
        print(self.winfo_id())
        for cell in Cell.instances:
            if cell == (self.winfo_id() - 1):
                print('cell - 1', cell)
            elif cell == (self.winfo_id() + 1):
                print('cell + 1', cell)
            elif cell == (self.winfo_id() - 10):
                print('cell - 10', cell)
        self.toggle_state()


if __name__ == "__main__":
    app = App()
    frame = MainFrame(app)
    grid = MainGrid(frame)
    app.mainloop()
