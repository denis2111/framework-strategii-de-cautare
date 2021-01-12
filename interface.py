import tkinter as tk
from tkinter.ttk import *
import time


class Application(tk.Frame):
    """
    1 - wall
    0 - path
    2 - exit
    3 - start
    """

    def __init__(self, size=35):
        tk.Frame.__init__(self)

        self.start_cell = None
        self.exit_cell = None
        self.size = size
        self.color = 'black'

    def start(self):
        self.grid()
        self.create_styles()
        self.maze_window()

    def create_widgets(self):
        print(1)

    def maze_window(self):
        self.width_label = Label(self, text="Width:", style='W.TLabel')
        self.width_label.grid(row=0, column=0)
        self.width_entry = tk.Entry(self)
        self.width_entry.insert(0, '13')
        self.width_entry.grid(row=0, column=1)
        self.height_label = Label(self, text="Height:", style='W.TLabel')
        self.height_label.grid(row=0, column=2)
        self.height_entry = tk.Entry(self)
        self.height_entry.insert(0, '13')
        self.height_entry.grid(row=0, column=3)

        self.button_draw = Button(self, text="Draw maze", style='W.TButton', command=self.draw_maze)
        self.button_draw.grid(row=0, column=4, pady=20, padx=20)

        self.button_wall = Button(self, text="Select wall", style='W.TButton', command=lambda: self.get_color(1))
        self.button_wall.grid(row=1, column=1, pady=20, padx=20)
        self.button_start = Button(self, text="Select start", style='W.TButton', command=lambda: self.get_color(2))
        self.button_start.grid(row=1, column=2, pady=20, padx=20)
        self.button_exit = Button(self, text="Select exit", style='W.TButton', command=lambda: self.get_color(3))
        self.button_exit.grid(row=1, column=3, pady=20, padx=20)

        self.choosen_algorithm = tk.StringVar(self)
        self.choosen_algorithm.set("BKT")
        self.algorithm = tk.OptionMenu(self, self.choosen_algorithm, "BKT", "BFS", "DFS", "Random", "Bidirectional", "Greedy",
                                       "Hill-Climbing")
        self.algorithm.config(width=20, font=('Lato', 12, 'bold'), foreground='#bb99ff')
        self.algorithm.grid(row=3, column=2)
        self.button_play = Button(self, style='W.TButton', text="Play", command=self.play)
        self.button_play.grid(row=4, column=2, pady=20, padx=20)

        self.draw_maze()
        # self.solve_maze()

    def draw_maze(self):
        self.maze_width = int(self.width_entry.get())
        self.maze_height = int(self.height_entry.get())
        self.maze = [[0 for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        width = self.maze_width * self.size
        height = self.maze_height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.grid(row=2, column=1, columnspan=3, pady=20)

        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
                x0 = j * self.size
                y0 = i * self.size
                x1 = x0 + self.size
                y1 = y0 + self.size
                self.canvas.create_rectangle(x0, y0, x1, y1, width=1, tags="cell", fill="white", outline="#bb99ff")
        self.canvas.tag_bind("cell", "<Button-1>", self.clicked)

    def clicked(self, event):

        cell_number = event.widget.find_closest(event.x, event.y)[0]
        if cell_number % self.maze_width == 0:
            row = cell_number // self.maze_width - 1
            col = self.maze_width - 1
        else:
            row = cell_number // self.maze_width
            col = cell_number % self.maze_width - 1
        print("clicked", row, col)
        if self.maze[row][col] == 0:
            self.canvas.itemconfigure(cell_number, fill=self.color, width=0)
            if self.color == 'black':
                self.maze[row][col] = 1
            elif self.color == 'green':
                if self.exit_cell:
                    self.maze[self.exit_cell[0]][self.exit_cell[1]] = 0
                    ci = self.exit_cell[0] * self.maze_width + self.exit_cell[1] + 1
                    self.canvas.itemconfigure(ci, fill='white', width=1)
                self.maze[row][col] = 2  # exit
                self.exit_cell = (row, col)
            elif self.color == 'red':
                if self.start_cell:
                    self.maze[self.start_cell[0]][self.start_cell[1]] = 0
                    ci = self.start_cell[0] * self.maze_width + self.start_cell[1] + 1
                    self.canvas.itemconfigure(ci, fill='white', width=1)
                self.maze[row][col] = 3  # start
                self.start_cell = (row, col)
        elif self.maze[row][col] == 1:
            self.canvas.itemconfigure(cell_number, fill='white', width=1)
            self.maze[row][col] = 0

    # def solve_maze(self):
    #     si, sj = self.start_cell
    #     fi, fj = self.exit_cell
    #     self.path = solveMaze(self.maze, self.maze_height, self.maze_width, si, sj, fi, fj, self)[1]

    def play(self):
        print(self.choosen_algorithm.get())

    def move_cell(self, row, col):
        self.canvas.delete(self.cell)
        x0 = col * self.size
        y0 = row * self.size
        x1 = x0 + self.size
        y1 = y0 + self.size
        self.cell = self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill='red')

        self.update()
        time.sleep(.5)

        self.check_status()

    def get_cell_coords(self):
        position = self.canvas.coords(self.cell)
        x = int(position[0] // self.size)
        y = int(position[1] // self.size)
        return x, y

    def check_status(self):
        print("check for: ", self.get_cell_coords())
        if self.exit_cell == self.get_cell_coords():
            print("Finished")

    def get_color(self, x):
        if x == 1:
            self.color = 'black'
        elif x == 2:
            self.color = 'red'
        elif x == 3:
            self.color = 'green'
        else:
            self.color = 'white'

    def create_styles(self):
        style = Style()
        style.configure('W.TButton', font=('Lato', 12, 'bold'), background='#bb99ff', foreground='#bb99ff')
        style.configure('W.TButton', padding=4, borderwidth=10)
        style.configure('W.TLabel', font=('Lato', 12, 'bold'), foreground='#bb99ff')


if __name__ == '__main__':
    app = Application()
    app.start()
    app.master.title('Maze game')
    app.mainloop()
