import tkinter
from tkinter import *
from tkinter import ttk


def reset_grid():
    pass
# Inverse la couleur d'une cellule lors du click
def change_color_cell(event):
    print(event.widget['style'])
    if event.widget['style'] == 'CellG.TFrame':
        event.widget.config(style='CellB.TFrame')
    else:
        event.widget.config(style='CellG.TFrame')


total_cells = []


class CellAlive(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        print(self.widgetName)
        self.style = 'CellB.TFrame'


# Methode d'une cellule et bind du click mouse1
def cell():
    c = ttk.Frame(canvas, width=19, height=19, class_='CellAlive')
    c.bind("<Button-1>", on_click)
    total_cells.append(c)
    return c


# Methode lors du click mouse1 sur une cellule
def on_click(event):
    change_color_cell(event)


root = Tk()
root.title('Le jeu de la vie')

# Initialisation de la grille principale
mainframe = ttk.Frame(root)
mainframe.grid()

# Bouton Quitter
btn_quit = ttk.Button(mainframe, text="Quitter", command=root.destroy)
btn_quit.grid(column=1, row=0)

# Bouton Reset de la grille
btn_reset = ttk.Button(mainframe, text="Réinitialiser", command=reset_grid)
btn_reset.grid(column=1, row=1)

# Initialisation du canvas
canvas = Canvas(mainframe, width=400, height=400, background='gray')
canvas.grid()

# Style de cellule
cell_style_grey = ttk.Style()
cell_style_grey.configure('CellG.TFrame', background='grey')
cell_style_black = ttk.Style()
cell_style_black.configure('CellB.TFrame', background='black')


# Dessine les lignes (horizontale et verticale) de la grille
# Instancie les cellules de la grille
for i in range(0, 400, 20):
    for j in range(0, 400, 20):
        canvas.create_rectangle(i, j, (i+20), (j+20), width=1)
        canvas.create_window(i+10, j+10, window=cell())


root.mainloop()
