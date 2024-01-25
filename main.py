import tkinter as tk
from tkinter import Frame, Button, Label
from tkinter import Grid
import random
import settings
import utils
import ctypes
import sys


root = tk.Tk()
root.configure(bg="black")
root.geometry(f'{settings.width}x{settings.height}')
root.title("MindSweeper Game")
root.resizable(True, True)

top_frame = Frame(
    root,
    bg="black",
    width=settings.width,
    height=utils.height_prct(25)
)
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg ="black",
    fg =  "white",
    text= "MineSweeper Game",
    font= ('Arial Black', 40)
)
game_title.place(
    x=utils.width_prct(8), y=30
)

left_frame = Frame(
    root,
    bg="black",
    width=utils.width_prct(18),
    height=utils.height_prct(75)
)
left_frame.place(x=0, y=utils.height_prct(25))

center_frame = Frame(
    root,
    bg="black",
    width=utils.width_prct(80),
    height=utils.height_prct(80)
)
center_frame.place(x=utils.width_prct(18), y=utils.height_prct(25))

class Cell:
    all = []
    cell_count =  settings.cell_count
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate=False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        Cell.all.append(self)

    def Click(self, location):
        btn1 = Button(
            location,
            width = 2,
            height = 1,
            bg="white"
        )
        btn1.bind('<Button-1>', self.left_click_actions)
        btn1.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn1
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{settings.cell_count}",
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    def Grid(self, **kwargs):
        self.cell_btn_object.grid(**kwargs)
       #btn1.pack()

    def left_click_actions(self, event):
        #print(self)
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mine_length==0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
        self.show_cell()
        if Cell.cell_count == settings.mines_count:
            ctypes.windll.user32.MessageBoxW(0,'Congratulations you have won the game', 'Game Over', 2)


        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self,x,y):
        for cell in Cell.all:
            if cell.x ==x and cell.y ==y:
                return cell
        pass
    @property
    def surrounded_cells(self):
        cells = [
        self.get_cell_by_axis(self.x - 1, self.y - 1),
        self.get_cell_by_axis(self.x - 1, self.y),
        self.get_cell_by_axis(self.x - 1, self.y + 1),
        self.get_cell_by_axis(self.x, self.y - 1),
        self.get_cell_by_axis(self.x + 1, self.y - 1),
        self.get_cell_by_axis(self.x + 1, self.y),
        self.get_cell_by_axis(self.x + 1, self.y + 1),
        self.get_cell_by_axis(self.x, self.y + 1)
    ]
        surrounded_cells = [cell for cell in cells if cell is not None]
        return surrounded_cells
    @property
    def surrounded_cells_mine_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine :
                counter = counter + 1
        return counter
    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mine_length)
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            self.cell_btn_object.configure(
                bg="SystemButtonFace"
            )
        # Mark the cell as opened (Use is as the last line of this method)
        self.is_opened = True
    def show_mine(self):
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0,'You clicked on a mine', 'Game Over', 2)
        sys.exit()

    def right_click_actions(self,event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg="orange"
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_candidate = False
    @staticmethod
    def randomize_mine():
        pick_cells = random.sample(Cell.all, settings.mines_count)
        #print(pick_cells)
        for pick_cell in pick_cells:
            pick_cell.is_mine = True
        pass
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        cell_obj = Cell(x,y)
        cell_obj.Click(center_frame)  # Use center_frame as the location
        cell_obj.Grid(column=x, row=y)
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(
    x=0, y= utils.height_prct(18)
)
Cell.randomize_mine()

# Run the window
root.mainloop()
