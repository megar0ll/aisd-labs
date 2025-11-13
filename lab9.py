import tkinter as tk
import random
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.resizable(False, False)
        self.board_size = 3
        self.cell_size = 100
        self.computer_starts = True
        self.current_player = "O"
        self.game_over = False
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.canvas = tk.Canvas(
            self.window,
            width=self.board_size * self.cell_size,
            height=self.board_size * self.cell_size,
            bg="white"
        )
        self.canvas.pack()
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=10)
        self.new_game_button = tk.Button(
            self.button_frame,
            text="Новая игра",
            command=self.new_game,
            font=("Arial", 12)
        )
        self.new_game_button.pack(side=tk.LEFT, padx=5)
        self.switch_first_move_button = tk.Button(
            self.button_frame,
            text="Игрок ходит первым",
            command=self.switch_first_move,
            font=("Arial", 12)
        )
        self.switch_first_move_button.pack(side=tk.LEFT, padx=5)
        self.status_label = tk.Label(
            self.window,
            text="Ход: Компьютер (O)",
            font=("Arial", 12)
        )
        self.status_label.pack()
        self.canvas.bind("<Button-1>", self.click_handler)
        self.draw_board()
        if self.computer_starts:
            self.window.after(500, self.computer_move)

    def switch_first_move(self):
        self.computer_starts = not self.computer_starts
        if self.computer_starts:
            self.switch_first_move_button.config(text="Игрок ходит первым")
            self.current_player = "O"
            self.status_label.config(text="Ход: Компьютер (O)")
        else:
            self.switch_first_move_button.config(text="Компьютер ходит первым")
            self.current_player = "X"
            self.status_label.config(text="Ход: Игрок (X)")
        self.new_game()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(1, self.board_size):
            self.canvas.create_line(
                i * self.cell_size, 0,
                i * self.cell_size, self.board_size * self.cell_size,
                width=2
            )
            self.canvas.create_line(
                0, i * self.cell_size,
                   self.board_size * self.cell_size, i * self.cell_size,
                width=2
            )
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.cell_size
                y = row * self.cell_size
                if self.board[row][col] == "X":
                    self.draw_x(x, y)
                elif self.board[row][col] == "O":
                    self.draw_o(x, y)

    def draw_x(self, x, y):
        margin = 15
        self.canvas.create_line(
            x + margin, y + margin,
            x + self.cell_size - margin, y + self.cell_size - margin,
            width=3, fill="red"
        )
        self.canvas.create_line(
            x + self.cell_size - margin, y + margin,
            x + margin, y + self.cell_size - margin,
            width=3, fill="red"
        )

    def draw_o(self, x, y):
        margin = 15
        self.canvas.create_oval(
            x + margin, y + margin,
            x + self.cell_size - margin, y + self.cell_size - margin,
            width=3, outline="blue"
        )

    def click_handler(self, event):
        if self.game_over or self.current_player == "O":
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.board[row][col] == "":
                self.make_move(row, col)

    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        self.draw_board()
        if self.check_win(self.current_player):
            self.game_over = True
            winner = "Игрок" if self.current_player == "X" else "Компьютер"
            self.status_label.config(text=f"Победил {winner}!")
            messagebox.showinfo("Игра окончена", f"Победил {winner}!")
        elif self.check_draw():
            self.game_over = True
            self.status_label.config(text="Ничья!")
            messagebox.showinfo("Игра окончена", "Ничья!")
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_status()
            if self.current_player == "O" and not self.game_over:
                self.window.after(500, self.computer_move)

    def computer_move(self):
        if self.game_over:
            return
        move = self.find_winning_move("O")
        if move:
            row, col = move
            self.make_move(row, col)
            return
        move = self.find_winning_move("X")
        if move:
            row, col = move
            self.make_move(row, col)
            return
        if self.board[1][1] == "":
            self.make_move(1, 1)
            return
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for row, col in corners:
            if self.board[row][col] == "":
                self.make_move(row, col)
                return
        empty_cells = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == "":
                    empty_cells.append((row, col))
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)

    def find_winning_move(self, player):
        for row in range(self.board_size):
            if self.board[row].count(player) == 2 and "" in self.board[row]:
                for col in range(self.board_size):
                    if self.board[row][col] == "":
                        return (row, col)
        for col in range(self.board_size):
            column = [self.board[row][col] for row in range(self.board_size)]
            if column.count(player) == 2 and "" in column:
                for row in range(self.board_size):
                    if self.board[row][col] == "":
                        return (row, col)
        main_diag = [self.board[i][i] for i in range(self.board_size)]
        if main_diag.count(player) == 2 and "" in main_diag:
            for i in range(self.board_size):
                if self.board[i][i] == "":
                    return (i, i)
        anti_diag = [self.board[i][self.board_size - 1 - i] for i in range(self.board_size)]
        if anti_diag.count(player) == 2 and "" in anti_diag:
            for i in range(self.board_size):
                if self.board[i][self.board_size - 1 - i] == "":
                    return (i, self.board_size - 1 - i)
        return None

    def check_win(self, player):
        for row in range(self.board_size):
            if all(self.board[row][col] == player for col in range(self.board_size)):
                return True
        for col in range(self.board_size):
            if all(self.board[row][col] == player for row in range(self.board_size)):
                return True
        if all(self.board[i][i] == player for i in range(self.board_size)):
            return True
        if all(self.board[i][self.board_size - 1 - i] == player for i in range(self.board_size)):
            return True
        return False

    def check_draw(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == "":
                    return False
        return True

    def update_status(self):
        if self.current_player == "X":
            self.status_label.config(text="Ход: Игрок (X)")
        else:
            self.status_label.config(text="Ход: Компьютер (O)")

    def new_game(self):
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.game_over = False
        if self.computer_starts:
            self.current_player = "O"
            self.status_label.config(text="Ход: Компьютер (O)")
        else:
            self.current_player = "X"
            self.status_label.config(text="Ход: Игрок (X)")

        self.draw_board()
        if self.computer_starts and not self.game_over:
            self.window.after(500, self.computer_move)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
