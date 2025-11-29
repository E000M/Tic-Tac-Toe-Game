import tkinter as tk
import random

root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("400x400")
root.resizable(False, False)
root.config(bg="#FFC3CC")

current_player = "X"
buttons = []
game_mode = None
scores = {"X": 0, "O": 0, "Tie": 0}

# --- UI Setup ---
menu_frame = tk.Frame(root, bg="#FFC3CC")
game_frame = tk.Frame(root, bg="#FFC3CC")
win_canvas = None
score_label = tk.Label(root, text="", font=("Arial Black", 12), bg="#FFC3CC", fg="#28301C")

# --- Game functions ---
def start_game(mode):
    global game_mode, scores, win_canvas, current_player
    
    game_mode = mode
    scores = {"X": 0, "O": 0, "Tie": 0}  
    current_player = "X"  
    

    if win_canvas:
        try:
            win_canvas.delete("all")
            win_canvas.place_forget()
            win_canvas.destroy()
        except (tk.TclError, AttributeError):
            pass
        win_canvas = None
    

    for row in buttons:
        for b in row:
            b.config(text="", state="normal", bg="#D2DB76")
    
    update_score()
    menu_frame.pack_forget()
    score_label.pack(pady=5)
    game_frame.pack(pady=5)
    btn_frame.pack(side='bottom', pady=10)
    
  
    root.update_idletasks()
    win_canvas = tk.Canvas(root, bg="", highlightthickness=0)
    win_canvas.place_forget() 

def go_back():
    global win_canvas
    game_frame.pack_forget()
    score_label.pack_forget()
    if win_canvas:
        win_canvas.place_forget()
        win_canvas.destroy()
        win_canvas = None
    menu_frame.pack(pady=50)
    btn_frame.pack(side='bottom', pady=10)

def update_score():
    score_label.config(text=f"X: {scores['X']}   O: {scores['O']}   Tie: {scores['Tie']}")

def restart_game():
    global current_player, win_canvas
    current_player = "X"
    if win_canvas:
        win_canvas.delete("all")
        win_canvas.place_forget()  
    for row in buttons:
        for b in row:
            b.config(text="", state="normal", bg="#D2DB76")

def draw_win_line(b1, b2, b3):
    """Draw a line through the three winning buttons"""
    global win_canvas
    if not win_canvas:
        return
    
    root.update_idletasks()
    game_frame.update_idletasks()
    
    game_frame_x = game_frame.winfo_x()
    game_frame_y = game_frame.winfo_y()
    game_frame_width = game_frame.winfo_width()
    game_frame_height = game_frame.winfo_height()
    
    x1 = game_frame_x + b1.winfo_x() + b1.winfo_width() // 2
    y1 = game_frame_y + b1.winfo_y() + b1.winfo_height() // 2
    x3 = game_frame_x + b3.winfo_x() + b3.winfo_width() // 2
    y3 = game_frame_y + b3.winfo_y() + b3.winfo_height() // 2
    
    win_canvas.place(x=game_frame_x, y=game_frame_y, width=game_frame_width, height=game_frame_height)
    win_canvas.config(bg="#FFC3CC")
    
    win_canvas.create_line(x1 - game_frame_x, y1 - game_frame_y, 
                          x3 - game_frame_x, y3 - game_frame_y, 
                          fill="#FF0000", width=8, capstyle=tk.ROUND)
    win_canvas.lift()  
    win_canvas.update()

def highlight(b1, b2, b3):
    for b in (b1, b2, b3):
        b.config(bg="#D2DB76")
    root.after(100, lambda: draw_win_line(b1, b2, b3))
    root.after(800, restart_game)

def disable_all():
    for row in buttons:
        for b in row:
            b.config(state="disabled")

def check_winner(do_highlight=True):
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            if do_highlight:
                highlight(buttons[i][0], buttons[i][1], buttons[i][2])
            return buttons[i][0]["text"]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            if do_highlight:
                highlight(buttons[0][i], buttons[1][i], buttons[2][i])
            return buttons[0][i]["text"]
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        if do_highlight:
            highlight(buttons[0][0], buttons[1][1], buttons[2][2])
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        if do_highlight:
            highlight(buttons[0][2], buttons[1][1], buttons[2][0])
        return buttons[0][2]["text"]
    return None

def is_full():
    return all(buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

def click(row, col):
    global current_player
    button = buttons[row][col]
    if button["text"] == "":
        button["text"] = current_player
        winner = check_winner()  
        if winner:
            scores[winner] += 1
            update_score()
            disable_all()
            return
        if is_full():
            scores["Tie"] += 1
            update_score()
            for r in buttons:
                for b in r:
                    b.config(bg="#28301C")
            root.after(800, restart_game)
            return
        if game_mode == "PvC" and current_player == "X":
            current_player = "O"
            root.after(500, computer_move)
        else:
            current_player = "O" if current_player == "X" else "X"

def computer_move():
    best_move = find_best_move()
    if best_move:
        row, col = best_move
    else:
        empty = [(i, j) for i in range(3) for j in range(3) if buttons[i][j]["text"] == ""]
        if not empty:
            return
        row, col = random.choice(empty)
    click(row, col)

def find_best_move():
    for player in ["O", "X"]:  
        for i in range(3):
            for j in range(3):
                if buttons[i][j]["text"] == "":
                    buttons[i][j]["text"] = player
                    simulated_winner = check_winner(do_highlight=False)
                    buttons[i][j]["text"] = ""
                    if simulated_winner == player:
                        return (i, j)
    return None

# --- MENU UI ---
tk.Label(menu_frame, text="Tic Tac Toe", font=("Arial Black", 18), bg="#FFC3CC", fg="#28301C").pack(pady=10)
tk.Button(menu_frame, text="2 Players", font=("Arial Black", 12), bg="#28301C", fg="#D2DB76", width=15, command=lambda: start_game("PvP")).pack(pady=6)
tk.Button(menu_frame, text="vs Computer", font=("Arial Black", 12), bg="#28301C", fg="#D2DB76", width=15, command=lambda: start_game("PvC")).pack(pady=6)
menu_frame.pack(pady=50)

# --- GAME UI ---
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(game_frame, text="", font=("Arial Black", 20, "bold"), width=3, height=1,
                        bg="#D2DB76", activebackground="#FFC3CC", fg="#28301C",
                        command=lambda r=i, c=j: click(r, c))
        btn.grid(row=i, column=j, padx=2, pady=2)
        row.append(btn)
    buttons.append(row)

btn_frame = tk.Frame(root, bg="#FFC3CC")
btn_frame.pack(side='bottom', pady=10)

restart_btn = tk.Button(btn_frame, text="Restart", font=("Arial Black", 10), bg="#28301C", fg="#D2DB76", command=restart_game)
restart_btn.grid(row=0, column=0, padx=5)
back_btn = tk.Button(btn_frame, text="Menu", font=("Arial Black", 10), bg="#28301C", fg="#D2DB76", command=go_back)
back_btn.grid(row=0, column=1, padx=5)

#The main loop
root.mainloop()
