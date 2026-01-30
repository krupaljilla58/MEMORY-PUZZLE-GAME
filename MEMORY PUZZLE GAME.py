import tkinter as tk
import random
import time

# ------------------ Game Settings ------------------
ROWS = 4
COLS = 4
TIME_LIMIT = 60  # seconds
symbols = ["🍎", "🍌", "🍇", "🍒", "🥝", "🍍", "🍉", "🍓"] * 2

# ------------------ Main Window ------------------
root = tk.Tk()
root.title("Memory Puzzle Game")

buttons = {}
first_card = None
second_card = None
matched = set()
start_time = time.time()

# Shuffle cards
random.shuffle(symbols)

# ------------------ Functions ------------------
def update_timer():
    elapsed = int(time.time() - start_time)
    remaining = TIME_LIMIT - elapsed
    timer_label.config(text=f"Time Left: {remaining}s")

    if remaining <= 0:
        end_game("⏰ Time's Up! Game Over")
    else:
        root.after(1000, update_timer)

def on_click(r, c):
    global first_card, second_card

    if (r, c) in matched or (first_card and second_card):
        return

    buttons[(r, c)].config(text=symbols[r * COLS + c])

    if not first_card:
        first_card = (r, c)
    elif not second_card:
        second_card = (r, c)
        root.after(700, check_match)

def check_match():
    global first_card, second_card

    r1, c1 = first_card
    r2, c2 = second_card

    if symbols[r1 * COLS + c1] == symbols[r2 * COLS + c2]:
        matched.add((r1, c1))
        matched.add((r2, c2))
    else:
        buttons[(r1, c1)].config(text="")
        buttons[(r2, c2)].config(text="")

    first_card = None
    second_card = None

    if len(matched) == ROWS * COLS:
        end_game("🎉 You Won!")

def end_game(message):
    for btn in buttons.values():
        btn.config(state="disabled")
    result_label.config(text=message)

# ------------------ UI ------------------
timer_label = tk.Label(root, text="Time Left: 60s", font=("Arial", 14))
timer_label.grid(row=0, column=0, columnspan=COLS)

for r in range(ROWS):
    for c in range(COLS):
        btn = tk.Button(root, text="", width=6, height=3,
                        font=("Arial", 18),
                        command=lambda r=r, c=c: on_click(r, c))
        btn.grid(row=r+1, column=c)
        buttons[(r, c)] = btn

result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.grid(row=ROWS+2, column=0, columnspan=COLS)

# Start timer
update_timer()

root.mainloop()
