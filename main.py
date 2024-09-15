import tkinter as tk
from tkinter import *
from tkinter import ttk


# Retourne le nombre de cellules vivantes
def get_alive_cells_around(nearby_cells: []) -> int:
    count = 0
    for cell in Cell.instances:
        if cell.pos in nearby_cells:
            if cell.is_alive:
                count += 1
    return count


# Passe toutes les cell de la grid sur dead
def reset_grid():
    for instance in Cell.instances:
        instance.kill()


# Définit les cellules voisines de celle renseignée en paramètre
def cells_around(cell) -> []:
    # Liste des décalages correspondant aux voisins (gauche, droite, haut, bas et diagonales)
    deltas = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    # Listes des potentielles cellules voisines (peut contenir des cellules inexistantes, qui seraient hors grid)
    potential_cells_around = [tuple(pos_x - pos_y for pos_x, pos_y in zip(cell.pos, delta)) for delta in deltas]
    # Ne conserve que les cellules réellement présentes sur la grid
    cells_around_array = [cell for cell in potential_cells_around if all(0 <= pos <= 19 for pos in cell)]

    return cells_around_array


# Lance un tour de jeu
def run_round():
    become_alive = []  # cellules qui deviendront vivantes
    become_dead = []  # cellules qui deviendront mortes
    # Check les cellules vivantes de la grille
    for cell in Cell.instances:
        nearby_cells = cells_around(cell)  # cellules voisines
        alive_cells_around = get_alive_cells_around(nearby_cells)  # nombre de cellules voisines vivantes

        if alive_cells_around == 3:
            become_alive.append(cell)
        elif alive_cells_around == 2:
            pass
        else:
            become_dead.append(cell)

    for cell in become_alive:
        cell.live()
    for cell in become_dead:
        cell.kill()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Le jeu de la vie")
        self.geometry("800x600")

        # Config bouton Quitter
        self.button_quit = ttk.Button(self, text="Quitter")
        self.button_quit['command'] = self.destroy
        self.button_quit.grid(column=5, row=0)

        # Config button run
        self.button_run = ttk.Button(self, text='Démarrer')
        self.button_run['command'] = run_round
        self.button_run.grid(column=5, row=2)

        # Config bouton Reset grille
        self.button_reset = ttk.Button(self, text="Réinitialiser")
        self.button_reset['command'] = reset_grid
        self.button_reset.grid(column=5, row=1)


class MainFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.grid()


class MainGrid(ttk.Frame):

    def __init__(self, container):
        size_grid = 400
        super().__init__(container)
        self.canvas = Canvas(container, width=size_grid, height=size_grid, background='gray')
        self.canvas.grid()

        # Créé la grille et l'a remplie de cellules mortes
        for i in range(0, size_grid, 20):
            for j in range(0, size_grid, 20):
                self.canvas.create_rectangle(i, j, (i + 20), (j + 20), width=1)
                self.canvas.create_window(i + 10, j + 10, window=Cell(self.canvas,
                                                                      is_alive=False,
                                                                      pos_x=int(i/20),  # renseigne la position
                                                                      pos_y=int(j/20)))  # de la cellule sur la grille


class Cell(ttk.Frame):

    # Liste des cellules se trouvant sur la grid
    instances = []

    def __init__(self, container, is_alive, pos_x, pos_y):
        super().__init__(container)

        self.instances.append(self)
        self.is_alive = is_alive
        self.config(width=19)  # largeur
        self.config(height=19)  # hauteur
        self.posX = pos_x  # position en x
        self.posY = pos_y  # position en x
        self.pos = (pos_x, pos_y)  # position
        self.bind("<Button-1>", self.on_click_cell)  # Associe clic gauche sur la cellule
        self.update_state()

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
    def kill(self):
        self.is_alive = False
        self.update_state()

    # Passe l'état d'une cellule sur alive
    def live(self):
        self.is_alive = True
        self.update_state()

    # Déclenché au clic sur une cellule
    def on_click_cell(self, event):
        print('Position cellule', self.posX, self.posY)
        self.toggle_state()


if __name__ == "__main__":
    app = App()
    frame = MainFrame(app)
    grid = MainGrid(frame)
    app.mainloop()
