import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter.ttk import *
import time
import utils.colors as color
import json

from problemSolver import ProblemSolver
from mazeState import MazeState
from hanoiState import HanoiState


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
        self.button_other_problem = Button(self, text="Hanoi problem", style='W.TButton',
                                           command=lambda: self.master.switch_frame(HanoiInterface))
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
        self.heuristic_function_button = None
        self.heuristic_formula = "abs(current_line - final_line) + abs(current_column - final_column)"
        self.path_option = None
        self.bkt_option = 0
        self.random_steps_label = None
        self.random_steps_entry = None
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

        self.button_wall = Button(self, text="Select wall", style='W.TButton', command=lambda: self.get_color(1))
        self.button_wall.grid(row=1, column=1, pady=20, padx=20)
        self.button_start = Button(self, text="Select start", style='W.TButton', command=lambda: self.get_color(2))
        self.button_start.grid(row=1, column=2, pady=20, padx=20)
        self.button_exit = Button(self, text="Select exit", style='W.TButton', command=lambda: self.get_color(3))
        self.button_exit.grid(row=1, column=3, pady=20, padx=20)

        self.button_clear = Button(self, text="Clear path", style='W.TButton', command=lambda: self.clear_path())
        self.button_clear.grid(row=3, column=4, pady=20, padx=20)
        self.choosen_algorithm = tk.StringVar(self)
        self.choosen_algorithm.set("DFS")
        self.algorithm = tk.OptionMenu(self, self.choosen_algorithm, "BKT", "BFS", "DFS", "random", "bidirectional",
                                       "greedy", "hill_climbing", "A*", "simulated_annealing",
                                       command=self.algorithm_options)

        self.algorithm.config(width=20, font=('Lato', 12, 'bold'), foreground=color.APP)
        self.algorithm.grid(row=3, column=2)
        self.button_export = Button(self, text="Export data", style='W.TButton', command=lambda: self.export_data())
        self.button_export.grid(row=3, column=0, pady=20, padx=20)

        self.back_button = Button(self, style='W.TButton', text="Back", command=lambda: self.master.switch_frame(Menu))
        self.back_button.grid(row=4, column=0, pady=20, padx=20)
        self.button_play = Button(self, style='W.TButton', text="Play", command=self.play)
        self.button_play.grid(row=4, column=2, pady=20, padx=20)
        self.button_stop = Button(self, style='W.TButton', text="Stop", command=self.stop)
        self.button_stop.grid(row=4, column=4, pady=20, padx=20)

        self.draw_maze()

    def get_states_position_list(self, states_type):
        solution_path = []
        alg_name = self.algorithm

        if self.solution[states_type][0].current_position != self.solution[states_type][0].start_position:
            solution_state = {"line": self.solution[states_type][0].start_position[0],
                              "column": self.solution[states_type][0].start_position[1]}
            if alg_name == "BKT" or alg_name == "DFS" and states_type != "solution":
                solution_state["type"] = "forward"
            solution_path.append(solution_state)

        states_position_list = []
        for state in self.solution[states_type]:
            solution_state = {"line": state.current_position[0],
                              "column": state.current_position[1]
                              }
            if (alg_name == "BKT" or alg_name == "DFS") and solution_path and states_type != "solution":
                solution_state["type"] = "forward"
                if (solution_path[-1]["line"], solution_path[-1]["column"]) == state.current_position:
                    solution_state["type"] = "backward"
                if state.current_position in states_position_list:
                    solution_state["type"] = "backward"

            solution_path.append(solution_state)
            states_position_list.append(state.current_position)

        return solution_path

    @staticmethod
    def get_algorithm_type(alg_name):
        types = {"BKT": "uninformed",
                 "DFS": "uninformed",
                 "BFS": "uninformed",
                 "random": "uninformed",
                 "bidirectional": "uninformed",
                 "greedy": "informed",
                 "hill_climbing": "informed",
                 "A*": "informed",
                 "simulated_annealing": "informed"
                 }
        return types[alg_name]

    def write_to_json_file(self, file_path, data):
        json.dump(data, file_path, indent=4)

    def export_data(self):
        if self.solution:
            data = {"problem_type": "Maze",
                    "maze": self.solution["visited_states"][0].maze,
                    "start_position": self.solution["visited_states"][0].start_position,
                    "end_position": self.solution["visited_states"][0].end_position,
                    "algorithm_type": MazeInterface.get_algorithm_type(self.algorithm),
                    "algorithm_name": self.algorithm,
                    "solution_found": self.solution["solution_found"]}
            if self.solution["solution_found"]:
                data["solution_path"] = self.get_states_position_list("solution")
            data["visited_position"] = self.get_states_position_list("visited_states")
            # print(data)
            # json_object = json.dumps(data, indent=4)
            # json_file = open("exports/export.json", 'w')
            # json_file.write(json_object)

            files = [('JSON File', '*.json')]
            file_path = asksaveasfile(filetypes=files, defaultextension=json, initialfile='representation')
            self.write_to_json_file(file_path, data)

        else:
            return 0

    def algorithm_options(self, event):
        print(event)

        if event == "hill_climbing" or event == "greedy":
            self.heuristic_function_button = Button(self, style='W.TButton', text="Heuristic function",
                                                    command=lambda: self.heuristic_window())
            self.heuristic_function_button.grid(row=2, column=4, pady=20, padx=20)
        else:
            if self.heuristic_function_button:
                self.heuristic_function_button.grid_forget()

        if event == "BKT":
            self.choosen_path = tk.StringVar(self)
            self.choosen_path.set("Any solution")
            self.path_option = tk.OptionMenu(self, self.choosen_path, "Any solution", "Best solution")

            self.path_option.config(width=20, font=('Lato', 12, 'bold'), foreground=color.APP)
            self.path_option.grid(row=2, column=4, pady=20, padx=20)
        else:
            if self.path_option:
                self.path_option.grid_forget()

        if event == "random":
            self.random_steps_label = Label(self, text="Number of steps:", style='W.TLabel')
            self.random_steps_label.grid(row=2, column=4)
            self.random_steps_entry = tk.Entry(self, width=10)
            self.random_steps_entry.insert(0, '1000')
            self.random_steps_entry.grid(row=2, column=5, pady=20, padx=20)
        else:
            if self.random_steps_label:
                self.random_steps_label.grid_forget()
            if self.random_steps_entry:
                self.random_steps_entry.grid_forget()

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
        if self.start_cell and self.exit_cell:
            if self.stop_play:
                self.stop()
            self.clear_path()
            problem = MazeState(self.maze_height, self.maze_width, self.start_cell, self.start_cell, self.exit_cell,
                                self.maze, score_function_expr=self.heuristic_formula)
            self.ps = ProblemSolver(problem)
            self.algorithm = self.choosen_algorithm.get()
            self.algorithm_play()

    def algorithm_play(self):
        self.button_play.config(state=tk.DISABLED)
        self.canvas.tag_unbind("cell", "<Button-1>")
        if self.algorithm == "BKT":
            if self.choosen_path.get() == "Any solution":
                self.bkt_option = 0
            else:
                self.bkt_option = 1
            self.solution = self.ps.BKT()
            self.BKT_play()
        elif self.algorithm == "DFS":
            self.solution = self.ps.DFS()
            self.DFS_BFS_play()
        elif self.algorithm == "BFS":
            self.solution = self.ps.BFS()
            self.DFS_BFS_play()
        elif self.algorithm == "bidirectional":
            self.solution = self.ps.bidirectional()
            self.bidirectional_play()
        elif self.algorithm == "random":
            self.solution = self.ps.random(int(self.random_steps_entry.get()))
            self.random_play()
        elif self.algorithm == "greedy":
            self.solution = self.ps.greedy()
            self.greedy_play()
        elif self.algorithm == "hill_climbing":
            self.solution = self.ps.hill_climbing()
            self.hill_play()
        elif self.algorithm == "A*":
            self.solution = self.ps.a_star()
            self.a_star_play()
        elif self.algorithm == "simulated_annealing":
            self.solution = self.ps.simulated_annealing()
            self.simulated_annealing_play()

        if not self.stop_play:
            self.check_final()
        self.canvas.tag_bind("cell", "<Button-1>", self.clicked)
        self.button_play.config(state=tk.NORMAL)

    def simulated_annealing_play(self):
        solution = self.solution
        print(solution)
        if solution["solution_found"]:
            visited_states = solution["visited_states"][1:-1]
        else:
            visited_states = solution["visited_states"][1:]
        for state in visited_states:
            if self.stop_play:
                break
            print(state.current_position[0], state.current_position[1])
            cell_id = state.current_position[0] * self.maze_width + state.current_position[1] + 1
            if self.canvas.itemcget(cell_id, 'fill') == color.VISITED:
                self.canvas.itemconfigure(cell_id, width=1, fill=color.VISITED_TWICE)
            else:
                if self.canvas.itemcget(cell_id, 'fill') != color.VISITED_TWICE:
                    self.canvas.itemconfigure(cell_id, width=1, fill=color.VISITED)
            self.update()
            time.sleep(.5)
        if solution["solution_found"]:
            self.draw_solution(solution["solution"][1:-1])

    def a_star_play(self):
        solution = self.solution
        print(solution)
        if solution["solution_found"]:
            visited_states = solution["visited_states"][1:-1]
        else:
            visited_states = solution["visited_states"][1:]
        for state in visited_states:
            if self.stop_play:
                break
            cell_id = state.current_position[0] * self.maze_width + state.current_position[1] + 1
            if self.canvas.itemcget(cell_id, 'fill') != color.FINISH:
                self.canvas.itemconfigure(cell_id, width=1, fill=color.VISITED)
            self.update()
            time.sleep(.5)
        if solution["solution_found"]:
            self.draw_solution(solution["solution"][0:-1])

    def bidirectional_play(self):
        solution = self.solution
        print(solution)
        if solution["solution_found"]:
            visited_states = solution["visited_states"][1:-1]
        else:
            visited_states = solution["visited_states"][1:]
        for state in visited_states:
            if self.stop_play:
                break
            cell_id = state.current_position[0] * self.maze_width + state.current_position[1] + 1
            if self.canvas.itemcget(cell_id, 'fill') != color.FINISH:
                self.canvas.itemconfigure(cell_id, width=1, fill=color.VISITED)
            self.update()
            time.sleep(.5)
        if solution["solution_found"]:
            self.draw_solution(solution["solution"])

    def random_play(self):
        solution = self.solution
        for state in solution["visited_states"]:
            if self.stop_play:
                break
            self.move_cell(state.current_position[0], state.current_position[1])

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
            self.draw_solution(solution["solution"][1:-1])

    def hill_play(self):
        solution = self.solution
        if solution["solution_found"]:
            visited_states = solution["visited_states"][1:-1]
        else:
            visited_states = solution["visited_states"][1:]
        for state in visited_states:
            if self.stop_play:
                break
            cell_id = state.current_position[0] * self.maze_width + state.current_position[1] + 1
            self.canvas.itemconfigure(cell_id, width=1, fill=color.VISITED)
            self.update()
            time.sleep(.5)
        if solution["solution_found"]:
            self.draw_solution(solution["solution"][1:-1])

    def greedy_play(self):
        solution = self.solution
        if solution["solution_found"]:
            visited_states = solution["visited_states"][1:-1]
        else:
            visited_states = solution["visited_states"][1:]
        for state in visited_states:
            if self.stop_play:
                break
            cell_id = state.current_position[0] * self.maze_width + state.current_position[1] + 1
            self.canvas.itemconfigure(cell_id, width=1, fill=color.VISITED)
            self.update()
            time.sleep(.5)
        if solution["solution_found"]:
            self.draw_solution(solution["solution"][0:-1])

    def DFS_BFS_play(self):
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
                self.canvas.itemconfigure(cell_id, width=1, fill=color.MEMORIZED)
            else:
                self.canvas.itemconfigure(cell_id, width=1, fill=color.VISITED)
            self.update()
            time.sleep(.5)
        if solution["solution_found"]:
            if self.algorithm == "BFS":
                self.draw_solution(solution["solution"][0:-1])
            else:
                self.draw_solution(solution["solution"][1:-1])

    def draw_solution(self, solution_states):
        for state in solution_states:
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
        if not self.stop_play:
            self.button_play.config(state=tk.NORMAL)

    def clear_path(self):
        for i in range(self.maze_width * self.maze_height):
            if self.canvas.itemcget(i, 'fill') == color.VISITED or \
                    self.canvas.itemcget(i, 'fill') == color.COMMON or \
                    self.canvas.itemcget(i, 'fill') == color.SOLUTION or \
                    self.canvas.itemcget(i, 'fill') == color.MEMORIZED:
                self.canvas.itemconfigure(i, width=1, fill=color.CLEAR)

    def check_final(self):
        if self.solution["solution_found"]:
            success_window = tk.Toplevel(self)
            Label(success_window, text="Successfully found!", font="Lato 14", foreground=color.FINISH,
                  justify='center').grid(pady=20, padx=20)
        else:
            success_window = tk.Toplevel(self)
            Label(success_window, text="No solution found!", font="Lato 14", foreground=color.START,
                  justify='center').grid(pady=20, padx=20)

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

        Label(heuristic, text="Enter a heuristic function!", font="Lato 14", foreground=color.FINISH,
              justify='center').grid(row=0, column=1, pady=20, padx=20)
        T = tk.Text(heuristic, height=15, width=60, font="Lato 12")
        T.insert(tk.END, self.heuristic_formula)
        T.grid(row=1, columnspan=3)

        self.save_button = Button(heuristic, style='W.TButton', text="Save formula",
                                  command=lambda: self.save_formula(T))
        self.save_button.grid(row=2, column=0, pady=20, padx=10)
        self.instruction_button = Button(heuristic, style='W.TButton', text="See instructions",
                                         command=lambda: self.display_instructions())
        self.instruction_button.grid(row=2, column=2, pady=20, padx=10)

    def save_formula(self, T):
        print(T.get("1.0", "end-1c"))
        self.heuristic_formula = T.get("1.0", "end-1c")

    def display_instructions(self):
        instructions = tk.Toplevel(self)
        # instructions.geometry("450x400")
        Label(instructions, text="Available functions", font="Lato 14", foreground=color.FINISH,
              justify='center').grid(row=0, columnspan=2, pady=20, padx=20)
        default_function_list = tk.Listbox(instructions, font="Lato 12")
        default_list = ["sqrt", "sqrt_ord", "sin", "cos", "tg", "ctg", "abs", "min", "max"]
        costum_function_list = tk.Listbox(instructions, font="Lato 12")
        custom_valid_functions = ["line_min", "line_max", "line_sum", "line_prod",
                                  "matrix_min", "matrix_max", "matrix_sum", "matrix_prod", "matrix_column_index",
                                  "matrix_line_index",
                                  "number_of_lines", "number_of_columns", "current_line", "current_column",
                                  "final_line", "final_column",
                                  "start_line", "start_column", "container"]
        for item in default_list:
            default_function_list.insert(tk.END, item)
        for item in custom_valid_functions:
            costum_function_list.insert(tk.END, item)
        default_function_list.grid(row=1, column=0, pady=20, padx=20)
        costum_function_list.grid(row=1, column=1, pady=20, padx=20)

    def create_styles(self):
        style = Style()
        style.configure('W.TButton', font=('Lato', 12, 'bold'), background=color.APP, foreground=color.APP)
        style.configure('W.TButton', padding=4, borderwidth=10)
        style.configure('W.TLabel', font=('Lato', 12, 'bold'), foreground=color.APP)


class HanoiInterface(tk.Frame):
    def __init__(self, master, size=35):
        tk.Frame.__init__(self, master)
        tk.Frame.config(self, width=550, height=550)
        self.representation = None
        self.pieces_label = tk.Label(self, text="Nr of Pieces:", font=('Helvetica', 15))
        self.pieces_label.place(relx=0.05, rely=0.05)
        self.pieces_input = tk.StringVar(self, value="4")
        self.pieces_entry = tk.Entry(self, font=('Helvetica', 16), textvariable=self.pieces_input, fg="black",
                                     bg="white", width=2)
        self.pieces_entry.place(relx=0.28, rely=0.05)

        self.towers_label = tk.Label(self, text="Nr of Towers:", font=('Helvetica', 15))
        self.towers_label.place(relx=0.35, rely=0.05)
        self.towers_input = tk.StringVar(self, value="3")
        self.towers_entry = tk.Entry(self, font=('Helvetica', 16), textvariable=self.towers_input, fg="black",
                                     bg="white", width=2)
        self.towers_entry.place(relx=0.59, rely=0.05)

        self.initial_tower_label = tk.Label(self, text="Initial tower:", font=('Helvetica', 15))
        self.initial_tower_label.place(relx=0.67, rely=0.05)
        self.initial_tower_input = tk.StringVar(self, value="1")
        self.initial_tower_entry = tk.Entry(self, font=('Helvetica', 16), textvariable=self.initial_tower_input,
                                            fg="black",
                                            bg="white", width=2)
        self.initial_tower_entry.place(relx=0.89, rely=0.05)

        self.play_button = Button(self, style='W.TButton', text="Play", command=self.start_drawing)
        self.play_button.place(relx=0.38, rely=0.8)

        self.menu_button = Button(self, style='W.TButton', text="Back", command=lambda: self.master.switch_frame(Menu))
        self.menu_button.place(relx=0.11, rely=0.8)
        # self.start_drawing()

    def get_solution(self):
        nr_pieces = int(self.pieces_input.get())
        nr_towers = int(self.towers_input.get())
        initial_tower = int(self.initial_tower_input.get())
        state = HanoiState(nr_towers, nr_pieces, initial_tower)
        ps = ProblemSolver(state)
        solution = ps.BKT()['visited_states']
        return solution

    def start_drawing(self):
        self.play_button.place_forget()
        solution = self.get_solution()
        self.keep_drawing(solution, 0)
        print("AM SOLUTIA")

    def keep_drawing(self, intermediate_states, index_of_state):
        state_info = intermediate_states[index_of_state].tower_pieces()
        new_representation = HanoiRepr(self, state_info)
        self.switch_item(new_representation)
        if index_of_state <= len(intermediate_states) - 2:
            self.after(1000, lambda: self.keep_drawing(intermediate_states, index_of_state + 1))
        else:
            self.play_button.place(relx=0.38, rely=0.8)

    def switch_item(self, new_representation):
        if self.representation is not None:
            self.representation.place_forget()
        self.representation = new_representation
        self.representation.place(relx=0.2, rely=0.4)


class HanoiRepr(tk.Frame):
    def __init__(self, master, state_info, size=35):
        tk.Frame.__init__(self, master)
        nr_of_towers = len(state_info.keys())
        nr_pieces = 0
        for pieces in state_info.values():
            nr_pieces += len(pieces)
        w = list(range(nr_pieces))
        frames = []
        for k in range(nr_of_towers):
            frames.append(Frame(self, height=nr_pieces * 100, width=(nr_pieces + 1) * 25))
            frames[k].grid(row=0, column=k)
        for f in range(nr_of_towers):
            w_tmp = tk.Canvas(frames[f], width=nr_pieces * 25, height=26)
            w_tmp.grid(row=nr_pieces, column=0, columnspan=(nr_pieces + 1))
            w_tmp.create_rectangle(0, 0, nr_pieces * 25, 10, fill="blue")
            for i in range(0, len(state_info[f + 1])):
                w[i] = tk.Canvas(frames[f], width=(state_info[f + 1][i]) * 25, height=26)
                w[i].grid(row=nr_pieces - i - 1, column=0)
                w[i].create_rectangle(0, 0, state_info[f + 1][i] * 25, 25, fill="black")
            for i in range(len(state_info[f + 1]), nr_pieces):
                w[i] = tk.Canvas(frames[f], width=nr_pieces * 25, height=26)
                w[i].grid(row=nr_pieces - i - 1, column=0, columnspan=(nr_pieces + 1))
                w[i].create_rectangle(0, 0, nr_pieces * 25, 25, fill="white")


if __name__ == '__main__':
    app = MainApp()
    # app.start()
    # app.master.title('Maze game')
    app.mainloop()
