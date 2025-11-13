import tkinter as tk
from tkinter import messagebox
import random
root, player_board, enemy_board, player_display, bot_display = None, None, None, None, None
player_buttons, enemy_buttons, bot_hits, bot_targets = [], [], [], []
bot_mode, game_over, placing_ships, ships = "search", False, True, [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
size_var, dir_var, ships_label, turn_label = None, None, None, None
current_turn = "player"

def create_board(): return [["~" for _ in range(10)] for _ in range(10)]

def can_place_ship(b, x, y, s, d):
    if d == "h" and y + s <= 10:
        for i in range(max(0, x - 1), min(10, x + 2)):
            for j in range(max(0, y - 1), min(10, y + s + 1)):
                if b[i][j] != "~": return False
    elif d == "v" and x + s <= 10:
        for i in range(max(0, x - 1), min(10, x + s + 1)):
            for j in range(max(0, y - 1), min(10, y + 2)):
                if b[i][j] != "~": return False
    else:
        return False
    return True

def place_ship(b, x, y, s, d):
    if can_place_ship(b, x, y, s, d):
        for i in range(s):
            if d == "h":
                b[x][y + i] = "S"
            else:
                b[x + i][y] = "S"
        return True
    return False

def setup_bot_ships():
    for s in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
        while not place_ship(enemy_board, random.randint(0, 9), random.randint(0, 9), s,
                             random.choice(["h", "v"])): pass

def update_ships_label():
    c = {4: 0, 3: 0, 2: 0, 1: 0}
    for s in ships: c[s] += 1
    ships_label.config(
        text=f"Осталось кораблей: {', '.join(f'{v}×{k}' for k, v in sorted(c.items(), reverse=True) if v) or 'нет кораблей'}")

def update_turn_label():
    if placing_ships:
        turn_label.config(text="Расстановка кораблей", fg="orange", font=("Arial", 12, "bold"))
    elif game_over:
        turn_label.config(text="Игра завершена", fg="red", font=("Arial", 12, "bold"))
    elif current_turn == "player":
        turn_label.config(text="ВАШ ХОД → Стреляйте по полю противника", fg="green", font=("Arial", 12, "bold"))
    else:
        turn_label.config(text="ХОД ПРОТИВНИКА ← Ждите...", fg="red", font=("Arial", 12, "bold"))

def update_ui():
    for i in range(10):
        for j in range(10):
            c = player_board[i][j]
            bg_color = "lightblue" if c == "S" else "white" if c == "~" else "red" if c == "X" else "lightgray"
            player_buttons[i][j].config(
                bg=bg_color,
                state="disabled" if not placing_ships else "normal",
                relief="raised" if c == "S" else "sunken"
            )
            c = player_display[i][j]
            if c == "X":
                bg_color = "red"
                text = "💥"
            elif c == "O":
                bg_color = "lightgray"
                text = "•"
            else:
                bg_color = "lightcyan"
                text = ""

            enemy_buttons[i][j].config(
                bg=bg_color,
                text=text,
                state="disabled" if c in ["X", "O"] or placing_ships or current_turn == "bot" or game_over else "normal"
            )
    update_ships_label()
    update_turn_label()

def place_ship_click(x, y):
    global placing_ships, ships
    if not placing_ships or not ships: return
    try:
        s = int(size_var.get())
        if s not in ships: raise ValueError
        if place_ship(player_board, x, y, s, "h" if dir_var.get() == "Горизонтально" else "v"):
            ships.remove(s)
            if not ships:
                placing_ships = False
                for i in range(10):
                    for j in range(10):
                        player_buttons[i][j].config(command=lambda: None, state="disabled")
                        enemy_buttons[i][j].config(state="normal")
            update_ui()
    except:
        pass
def is_hit(b, x, y): return b[x][y] == "S"

def is_ship_sunk(b, x, y, d):
    if b[x][y] != "X": return False
    v, s = set(), [(x, y)]
    while s:
        cx, cy = s.pop()
        if (cx, cy) in v or not (0 <= cx < 10 and 0 <= cy < 10): continue
        if b[cx][cy] == "X": v.add((cx, cy)); s.extend(
            [(cx + dx, cy + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)] if
             0 <= cx + dx < 10 and 0 <= cy + dy < 10])
    for cx, cy in v:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and b[nx][ny] == "S": return False
    for cx, cy in v:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and b[nx][ny] == "~": b[nx][ny] = d[nx][ny] = "O"
    return True

def all_ships_sunk(b): return not any("S" in row for row in b)

def player_turn(x, y):
    global game_over, player_display, enemy_board, current_turn
    if game_over or placing_ships or player_display[x][y] in ["X", "O"] or current_turn == "bot": return
    hit = is_hit(enemy_board, x, y)
    player_display[x][y] = enemy_board[x][y] = "X" if hit else "O"
    is_ship_sunk(enemy_board, x, y, player_display)
    if all_ships_sunk(enemy_board):
        messagebox.showinfo("Победа!", "🎉 Вы потопили все корабли противника! 🎉")
        game_over = True
        current_turn = None
    elif not hit:
        current_turn = "bot"
        root.after(1000, bot_turn)
    update_ui()

def bot_turn():
    global player_board, bot_display, bot_hits, bot_targets, bot_mode, game_over, current_turn
    if game_over: return
    if bot_mode == "hunt" and bot_hits:
        x, y = bot_hits[-1]
        for dx, dy in random.sample([(0, 1), (1, 0), (0, -1), (-1, 0)], 4):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and bot_display[nx][ny] == "~":
                bot_targets = [(nx, ny)];
                break
        else:
            bot_mode = "search";
            bot_hits.pop()

    if bot_mode == "search":
        bot_targets = [(i, j) for i in range(10) for j in range(10) if
                       bot_display[i][j] == "~" and (i + j) % 2 == 0] or [(i, j) for i in range(10) for j in range(10)
                                                                          if bot_display[i][j] == "~"]
    if not bot_targets: return
    x, y = random.choice(bot_targets);
    bot_targets.remove((x, y));
    hit = is_hit(player_board, x, y)
    bot_display[x][y] = player_board[x][y] = "X" if hit else "O";
    is_ship_sunk(player_board, x, y, bot_display)
    if hit:
        bot_hits.append((x, y));
        bot_mode = "hunt"
    if all_ships_sunk(player_board):
        messagebox.showinfo("Поражение", "💀 Бот потопил все ваши корабли!")
        game_over = True
        current_turn = None
    elif not hit:
        current_turn = "player"
    else:
        root.after(1000, bot_turn)
    update_ui()

def create_ui():
    global root, player_buttons, enemy_buttons, size_var, dir_var, ships_label, turn_label
    title_label = tk.Label(root, text="🌊 МОРСКОЙ БОЙ 🌊", font=("Arial", 16, "bold"), fg="darkblue")
    title_label.grid(row=0, column=0, columnspan=2, pady=10)
    turn_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
    turn_label.grid(row=1, column=0, columnspan=2, pady=5)
    pf = tk.Frame(root, relief="ridge", bd=2, bg="lightgray")
    pf.grid(row=2, column=0, padx=15, pady=10)

    ef = tk.Frame(root, relief="ridge", bd=2, bg="lightgray")
    ef.grid(row=2, column=1, padx=15, pady=10)
    tk.Label(pf, text="ВАШЕ ПОЛЕ", font=("Arial", 12, "bold"), fg="darkgreen", bg="lightgray").grid(row=0, column=0,
                                                                                                    columnspan=11,
                                                                                                    pady=5)
    tk.Label(ef, text="ПОЛЕ ПРОТИВНИКА", font=("Arial", 12, "bold"), fg="darkred", bg="lightgray").grid(row=0, column=0,
                                                                                                        columnspan=11,
                                                                                                        pady=5)
    letters = "АБВГДЕЖЗИК"
    for i in range(10):
        tk.Label(pf, text=letters[i], font=("Arial", 10, "bold"), bg="lightgray").grid(row=1, column=i + 1, padx=2)
        tk.Label(ef, text=letters[i], font=("Arial", 10, "bold"), bg="lightgray").grid(row=1, column=i + 1, padx=2)
        tk.Label(pf, text=str(i + 1), font=("Arial", 10, "bold"), bg="lightgray").grid(row=i + 2, column=0, padx=2)
        tk.Label(ef, text=str(i + 1), font=("Arial", 10, "bold"), bg="lightgray").grid(row=i + 2, column=0, padx=2)
    for i in range(10):
        pr, er = [], []
        for j in range(10):
            btn = tk.Button(pf, width=3, height=1, font=("Arial", 8),
                            command=lambda x=i, y=j: place_ship_click(x, y),
                            relief="raised", bd=1)
            btn.grid(row=i + 2, column=j + 1, padx=1, pady=1)
            pr.append(btn)
            btn = tk.Button(ef, width=3, height=1, font=("Arial", 8),
                            command=lambda x=i, y=j: player_turn(x, y),
                            state="disabled", relief="raised", bd=1)
            btn.grid(row=i + 2, column=j + 1, padx=1, pady=1)
            er.append(btn)
        player_buttons.append(pr)
        enemy_buttons.append(er)
    control_frame = tk.Frame(root, relief="groove", bd=2, bg="lightyellow")
    control_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
    ships_label = tk.Label(control_frame, text="", font=("Arial", 10), bg="lightyellow")
    ships_label.grid(row=0, column=0, columnspan=4, pady=5)
    tk.Label(control_frame, text="Размер корабля:", font=("Arial", 9), bg="lightyellow").grid(row=1, column=0, padx=5)
    size_var = tk.StringVar(value=str(ships[0]))
    size_menu = tk.OptionMenu(control_frame, size_var, *sorted(set(ships), reverse=True))
    size_menu.config(font=("Arial", 8))
    size_menu.grid(row=1, column=1, padx=5)
    tk.Label(control_frame, text="Направление:", font=("Arial", 9), bg="lightyellow").grid(row=1, column=2, padx=5)
    dir_var = tk.StringVar(value="Горизонтально")
    dir_menu = tk.OptionMenu(control_frame, dir_var, "Горизонтально", "Вертикально")
    dir_menu.config(font=("Arial", 8))
    dir_menu.grid(row=1, column=3, padx=5)
    legend_frame = tk.Frame(root, relief="groove", bd=1, bg="white")
    legend_frame.grid(row=4, column=0, columnspan=2, pady=5)
    tk.Label(legend_frame, text="Легенда:", font=("Arial", 9, "bold"), bg="white").grid(row=0, column=0, columnspan=4, pady=2)
    tk.Label(legend_frame, text="■ Корабль", bg="lightblue", width=10).grid(row=1, column=0, padx=2)
    tk.Label(legend_frame, text="💥 Попадание", bg="red", fg="white", width=12).grid(row=1, column=1, padx=2)
    tk.Label(legend_frame, text="• Промах", bg="lightgray", width=8).grid(row=1, column=2, padx=2)
    tk.Label(legend_frame, text="~ Вода", bg="lightcyan", width=8).grid(row=1, column=3, padx=2)
    update_ui()

def main():
    global root, player_board, enemy_board, player_display, bot_display
    root = tk.Tk()
    root.title("Морской бой")
    root.configure(bg="aliceblue")
    player_board, enemy_board, player_display, bot_display = create_board(), create_board(), create_board(), create_board()
    setup_bot_ships()
    create_ui()
    root.mainloop()
if __name__ == "__main__":
    main()
