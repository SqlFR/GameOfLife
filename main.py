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

    @staticmethod
    def reset_grid(self):
        for cell in Cell.instances:
            cell.kill_cell()


class MainFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.grid()


class MainGrid(ttk.Frame):

    def __init__(self, container):
        size_grid = 500
        super().__init__(container)
        self.canvas = Canvas(container, width=size_grid, height=size_grid, background='gray')
        self.canvas.grid()

        for i in range(0, size_grid, 20):
            for j in range(0, size_grid, 20):
                self.canvas.create_rectangle(i, j, (i + 20), (j + 20), width=1)
                self.canvas.create_window(i + 10, j + 10, window=Cell(self.canvas, is_alive=False))


class Cell(ttk.Frame):

    instances = []

    def __init__(self, container, is_alive):
        super().__init__(container)

        self.instances.append(self)
        self.is_alive = is_alive
        self.config(width=19)
        self.config(height=19)
        self.bind("<Button-1>", self.on_click)
        self.update_state()

    def __del__(self):
        self.instances.remove(self)

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

    def toggle_state(self):
        # Change l'état de la cellule
        self.is_alive = not self.is_alive
        self.update_state()

    def kill_cell(self):
        self.is_alive = False
        self.update_state()

    def live_cell(self):
        self.is_alive = True
        self.update_state()

    def on_click(self, event):
        self.toggle_state()


if __name__ == "__main__":
    app = App()
    frame = MainFrame(app)
    grid = MainGrid(frame)
    app.mainloop()
