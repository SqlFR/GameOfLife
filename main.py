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

        # Config button run
        self.button_run = ttk.Button(self, text='Démarrer')
        self.button_run['command'] = self.run_round
        self.button_run.grid(column=1, row=2)

        # Config bouton Reset grille
        self.button_reset = ttk.Button(self, text="Réinitialiser")
        self.button_reset['command'] = self.reset_grid
        self.button_reset.grid(column=1, row=1)

    # Définit les cellules voisines de celle renseignée en paramètre
    def cells_around(self, cell) -> []:
        # Liste des décalages correspondant aux voisins (gauche, droite, haut, bas et diagonales)
        deltas = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        # Listes des potentielles cellules voisines (peut contenir des cellules inexistantes, qui seraient hors grid)
        potential_cells_around = [tuple(pos_x - pos_y for pos_x, pos_y in zip(cell.pos, delta)) for delta in deltas]
        # Ne conserve que les cellules réellement présentes sur la grid
        cells_around = [cell for cell in potential_cells_around if all(0 <= pos <= 19 for pos in cell)]

        return cells_around

    # Retourne le nombre de cellules vivantes
    def get_alive_cells_around(self, nearby_cells: []) -> int:
        count = 0
        for cell in Cell.instances:
            if cell.pos in nearby_cells:
                if cell.is_alive:
                    count += 1
        return count

    # Retourne le nombre de cellules mortes
    def get_dead_cells_around(self, nearby_cells: []) -> int:
        count = 0
        for cell in Cell.instances:
            if cell.pos in nearby_cells:
                if not cell.is_alive:
                    count += 1
        return count

    # Lance un tour de jeu
    def run_round(self):
        # Check les cellules vivantes de la grille
        become_alive = []
        become_dead = []
        for cell in Cell.instances:
            nearby_cells = self.cells_around(cell)
            if cell.is_alive:
                print('Cellules voisines', nearby_cells)
            alive_cells_around = self.get_alive_cells_around(nearby_cells)
            print('Cellules vivantes :', alive_cells_around)
            dead_cells_around = self.get_dead_cells_around(nearby_cells)
            #print('Cellules mortes :', dead_cells_around)

            if cell.is_alive:
                if alive_cells_around == 3:
                    become_alive.append(cell)

                elif 2 < alive_cells_around > 3:
                    become_dead.append(cell)
                else:
                    become_dead.append(cell)
            if not cell.is_alive:
                if alive_cells_around == 3:
                    become_alive.append(cell)

        for cell in become_alive:
            cell.live()
        for cell in become_dead:
            cell.kill()


    # Passe toutes les cell de la grid sur dead
    def reset_grid(self):
        for instance in Cell.instances:
            instance.kill()


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

        # Créé la grille et l'a remplie de cellule morte
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
