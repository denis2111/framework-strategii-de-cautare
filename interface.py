import tkinter as tk
from tkinter.ttk import *
import time
import utils.colors as color

from problemSolver import ProblemSolver
from mazeState import MazeState


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # tk.Tk.geometry(self, "900x700")
        self._frame = None
        self.switch_frame(Menu)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class Menu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.geometry("550x550")
        self.start()

    def start(self):
        self.grid()
        self.create_styles()
        self.menu_window()

    def menu_window(self):
        self.title_label = Label(self, text="Framework for search strategies", style='W.TLabel')
        self.title_label.grid(row=0, column=2, pady=20)
        self.button_maze = Button(self, text="Maze problem", style='W.TButton',
                                  command=lambda: self.master.switch_frame(MazeInterface))
        self.button_maze.grid(row=2, column=1, pady=20, padx=20)
        self.button_other_problem = Button(self, text="Other problem", style='W.TButton',
                                           command=lambda: self.master.switch_frame(MazeInterface))
        self.button_other_problem.grid(row=2, column=3, pady=20, padx=20)

    def create_styles(self):
        style = Style()
        style.configure('W.TButton', font=('Lato', 12, 'bold'), background=color.APP, foreground=color.APP)
        style.configure('W.TButton', padding=4, borderwidth=10)
        style.configure('W.TLabel', font=('Lato', 14, 'bold'), foreground=color.APP, wraplength='250', justify='center')


class MazeInterface(tk.Frame):
    """
    1 - wall
    0 - path
    2 - exit
    3 - start
    """

    def __init__(self, master, size=20):
        tk.Frame.__init__(self, master)
        self.master = master
        self.start_cell = None
        self.exit_cell = None
        self.cell = None
        self.canvas = None
        self.solution = None
        self.keep_path = False
        self.stop_play = False
        self.algorithm = None
        self.ps = None
        self.size = size
        self.color = color.WALL
        self.master.geometry("")
        self.start()

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
        self.width_entry.insert(0, '20')
        self.width_entry.grid(row=0, column=1)
        self.height_label = Label(self, text="Height:", style='W.TLabel')
        self.height_label.grid(row=0, column=2)
        self.height_entry = tk.Entry(self)
        self.height_entry.insert(0, '20')
        self.height_entry.grid(row=0, column=3)

        self.button_draw = Button(self, text="Draw maze", style='W.TButton', command=self.draw_maze)
        self.button_draw.grid(row=0, column=4, pady=20, padx=20)

        self.button_show_path = Button(self, text="Show path", style='W.TButton', command=lambda: self.keep_solution())
        self.button_show_path.grid(row=1, column=0, pady=20, padx=20)
        self.button_wall = Button(self, text="Select wall", style='W.TButton', command=lambda: self.get_color(1))
        self.button_wall.grid(row=1, column=1, pady=20, padx=20)
        self.button_start = Button(self, text="Select start", style='W.TButton', command=lambda: self.get_color(2))
        self.button_start.grid(row=1, column=2, pady=20, padx=20)
        self.button_exit = Button(self, text="Select exit", style='W.TButton', command=lambda: self.get_color(3))
        self.button_exit.grid(row=1, column=3, pady=20, padx=20)
        self.button_clear = Button(self, text="Clear path", style='W.TButton', command=lambda: self.clear_path())
        self.button_clear.grid(row=1, column=4, pady=20, padx=20)

        self.choosen_algorithm = tk.StringVar(self)
        self.choosen_algorithm.set("BKT")
        self.algorithm = tk.OptionMenu(self, self.choosen_algorithm, "BKT", "BFS", "DFS", "random", "bidirectional",
                                       "greedy", "hill_climbing")
        self.algorithm.config(width=20, font=('Lato', 12, 'bold'), foreground=color.APP)
        self.algorithm.grid(row=3, column=2)
        self.heuristic_function_button = Button(self, style='W.TButton', text="Heuristic function",
                                                command=lambda: self.heuristic_window())
        self.heuristic_function_button.grid(row=3, column=3, pady=20, padx=20)
        self.back_button = Button(self, style='W.TButton', text="Back", command=lambda: self.master.switch_frame(Menu))
        self.back_button.grid(row=4, column=0, pady=20, padx=20)
        self.button_play = Button(self, style='W.TButton', text="Play", command=self.play)
        self.button_play.grid(row=4, column=2, pady=20, padx=20)
        self.button_stop = Button(self, style='W.TButton', text="Stop", command=self.stop)
        self.button_stop.grid(row=4, column=4, pady=20, padx=20)

        self.draw_maze()

    def draw_maze(self):
        if self.canvas:
            self.canvas.delete("all")
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
                self.canvas.create_rectangle(x0, y0, x1, y1, width=1, tags="cell", fill=color.CLEAR, outline=color.APP)
        self.canvas.tag_bind("cell", "<Button-1>", self.clicked)

    def clicked(self, event):

        cell_number = event.widget.find_closest(event.x, event.y)[0]
        if cell_number % self.maze_width == 0:
            row = cell_number // self.maze_width - 1
            col = self.maze_width - 1
        else:
            row = cell_number // self.maze_width
            col = cell_number % self.maze_width - 1
        # print("clicked", row, col)
        if self.maze[row][col] == 0:
            self.canvas.itemconfigure(cell_number, fill=self.color, width=0)
            if self.color == color.WALL:
                self.maze[row][col] = 1
            elif self.color == color.FINISH:
                if self.exit_cell:
                    self.maze[self.exit_cell[0]][self.exit_cell[1]] = 0
                    ci = self.exit_cell[0] * self.maze_width + self.exit_cell[1] + 1
                    self.canvas.itemconfigure(ci, fill=color.CLEAR, width=1)
                self.maze[row][col] = 2  # exit
                self.exit_cell = (row, col)
            elif self.color == color.START:
                if self.start_cell:
                    self.maze[self.start_cell[0]][self.start_cell[1]] = 0
                    ci = self.start_cell[0] * self.maze_width + self.start_cell[1] + 1
                    self.canvas.itemconfigure(ci, fill=color.CLEAR, width=1)
                self.maze[row][col] = 3  # start
                self.start_cell = (row, col)
                self.cell = self.start_cell
        elif self.maze[row][col] == 1:
            self.canvas.itemconfigure(cell_number, fill=color.CLEAR, width=1)
            self.maze[row][col] = 0

    def play(self):
        if self.stop_play:
            self.stop()
        self.clear_path()
        problem = MazeState(self.maze_height, self.maze_width, self.start_cell, self.start_cell, self.exit_cell,
                            self.maze)
        self.ps = ProblemSolver(problem)
        self.algorithm = self.choosen_algorithm.get()
        self.algorithm_play()

    def algorithm_play(self):
        self.canvas.tag_unbind("cell", "<Button-1>")
        if self.algorithm == "BKT":
            self.solution = self.ps.BKT()
            self.BKT_play()
        elif self.algorithm == "DFS":
            self.solution = self.ps.DFS()
            self.DFS_BFS_play()
        elif self.algorithm == "BFS":
            self.solution = self.ps.BFS()
            self.DFS_BFS_play()

        if not self.stop_play:
            self.check_final()
        self.canvas.tag_bind("cell", "<Button-1>", self.clicked)

    def BKT_play(self):
        solution = self.solution
        if solution["solution_found"]:
            visited_states = solution["visited_states"][1:-1]
        else:
            visited_states = solution["visited_states"][1:]
        for state in visited_states:
            if self.stop_play:
                break
            cell_id = state.current_position[0] * self.maze_width + state.current_position[1] + 1
            if self.canvas.itemcget(cell_id, 'fill') == color.VISITED:
                self.canvas.itemconfigure(cell_id, width=1, fill=color.CLEAR)
            else:
                self.canvas.itemconfigure(cell_id, width=1, fill=color.VISITED)
            self.update()
            time.sleep(.5)
        if solution["solution_found"]:
            self.draw_solution(solution["solution"])

    def DFS_BFS_play(self):
        solution = self.solution
        if solution["solution_found"]:
            visited_states = solution["visited_states"][1:-1]
        else:
            visited_states = solution["visited_states"][1:]
        for state in visited_states:
            if self.stop_play:
                break
            self.move_cell(state.current_position[0], state.current_position[1])
        if solution["solution_found"]:
            self.draw_solution(solution["solution"])

    def draw_solution(self, solution_states):
        for state in solution_states[1:-1]:
            # if self.stop_play:
            #     break
            cell_id = state.current_position[0] * self.maze_width + state.current_position[1] + 1
            self.canvas.itemconfigure(cell_id, width=1, fill=color.SOLUTION)

    def move_cell(self, row, col):
        if not self.keep_path and self.cell != self.start_cell:
            self.canvas.itemconfigure(self.cell, width=1, fill=color.CLEAR)
        if (row, col) != self.start_cell and (row, col) != self.exit_cell:
            self.cell = row * self.maze_width + col + 1
            if self.choosen_algorithm.get() == "bidirectional":
                if self.canvas.itemcget(self.cell, 'fill') == color.VISITED:
                    self.canvas.itemconfigure(self.cell, width=1, fill=color.COMMON)
                else:
                    self.canvas.itemconfigure(self.cell, width=1, fill=color.VISITED)
            else:
                self.canvas.itemconfigure(self.cell, width=1, fill=color.VISITED)
            self.update()
            time.sleep(.5)

    def stop(self):
        self.stop_play = not self.stop_play

    def clear_path(self):
        for i in range(self.maze_width * self.maze_height):
            if self.canvas.itemcget(i, 'fill') == color.VISITED or \
                    self.canvas.itemcget(i, 'fill') == color.COMMON or \
                    self.canvas.itemcget(i, 'fill') == color.SOLUTION:
                self.canvas.itemconfigure(i, width=1, fill=color.CLEAR)

    def keep_solution(self):
        self.keep_path = not self.keep_path
        if self.keep_path:
            self.button_show_path.config(text="Hide path")
        else:
            self.button_show_path.config(text="Show path")

    def check_final(self):
        if self.solution["solution_found"] == True:
            success_window = tk.Toplevel(self)
            Label(success_window, text="Successfully found!", font="Lato 14", foreground=color.FINISH,
                  justify='center').grid(pady=20, padx=20)
        else:
            success_window = tk.Toplevel(self)
            Label(success_window, text="Solution not found!", font="Lato 14", foreground=color.START,
                  justify='center').grid(pady=20, padx=20)
        # x = self.solution["solution"][-1].current_position[0]
        # y = self.solution["solution"][-1].current_position[1]
        # if (x, y) == self.exit_cell:
        #     success_window = tk.Toplevel(self)
        #     Label(success_window, text="Successfully found!", font="Lato 14", foreground=color.FINISH,
        #           justify='center').grid(pady=20, padx=20)
        # elif self.choosen_algorithm.get() == "bidirectional":
        #     success_window = tk.Toplevel(self)
        #     Label(success_window, text="The paths have met!", font="Lato 14", foreground=color.FINISH,
        #           justify='center').grid(pady=20, padx=20)
        # else:
        #     success_window = tk.Toplevel(self)
        #     Label(success_window, text="Found a partial path!", font="Lato 14", foreground=color.FINISH,
        #           justify='center').grid(pady=20, padx=20)

    def get_color(self, x):
        if x == 1:
            self.color = color.WALL
        elif x == 2:
            self.color = color.START
        elif x == 3:
            self.color = color.FINISH
        else:
            self.color = color.CLEAR

    def heuristic_window(self):
        heuristic = tk.Toplevel(self)
        heuristic.geometry("450x400")

        Label(heuristic, text="Enter a heuristic function!", font="Lato 14", foreground=color.FINISH,
              justify='center').grid(
            pady=20, padx=20)
        T = tk.Text(heuristic, height=15, width=50, font="Lato 12")
        T.insert(tk.END, "Ex: |x1 - x2| + |y1 - y2|")
        T.grid()

        self.send_button = Button(heuristic, style='W.TButton', text="Send formula",
                                  command=lambda: self.send_formula(T))
        self.send_button.grid(pady=20, padx=20)

    def send_formula(self, T):
        print(T.get("1.0", "end-1c"))

    def create_styles(self):
        style = Style()
        style.configure('W.TButton', font=('Lato', 12, 'bold'), background=color.APP, foreground=color.APP)
        style.configure('W.TButton', padding=4, borderwidth=10)
        style.configure('W.TLabel', font=('Lato', 12, 'bold'), foreground=color.APP)


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
