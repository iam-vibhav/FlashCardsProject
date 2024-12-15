import tkinter as tk
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
CORRECT_COLOR = "#00FF00"
WRONG_COLOR = "#FF0000"
COUNT_DOWN = 10

# Load flashcards
try:
    FLASH_CARDS = pd.read_csv("data/french_words.csv")
except FileNotFoundError:
    print("CSV file not found. Please check the file path.")
    FLASH_CARDS = pd.DataFrame(columns=["French", "English"])

FRESH_FLASH_CARDS = {}
GUESSED_FLASH_CARDS = {}

# Populate flashcards dictionary
for _, row in FLASH_CARDS.iterrows():
    french, english = row
    FRESH_FLASH_CARDS[french] = english

# Initialize global variables
new_french_card = ""
new_english_card = ""

# ---------------------------------- TIMERS --------------------------------
def count_down():
    global COUNT_DOWN
    if COUNT_DOWN > 0:
        COUNT_DOWN -= 1
        window.after(1000, count_down)
    else:
        flip_card()


def flip_card():
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(language, text="English")
    canvas.itemconfig(word, text=new_english_card)
    wrong_button.grid(row=1, column=0)
    right_button.grid(row=1, column=1)


def reset_count_down():
    global COUNT_DOWN
    COUNT_DOWN = 10
    canvas.itemconfig(card, image=card_front)
    wrong_button.grid_forget()
    right_button.grid_forget()
    reset_bg_color()
    generate_flash_card()
    canvas.itemconfig(language, text="French")
    canvas.itemconfig(word, text=new_french_card)
    count_down()


# ----------------------------------- FLASH CARDS SETUP ---------------------
def generate_flash_card():
    global new_french_card, new_english_card
    if FRESH_FLASH_CARDS:
        new_french_card = random.choice(list(FRESH_FLASH_CARDS.keys()))
        new_english_card = FRESH_FLASH_CARDS[new_french_card]
    else:
        new_french_card = ""
        new_english_card = ""


# ----------------------------------- BUTTON FUNCTIONALITY -------------------
def reset_bg_color():
    window.config(bg=BACKGROUND_COLOR)
    canvas.config(bg=BACKGROUND_COLOR)


def right_answer():
    global FRESH_FLASH_CARDS, GUESSED_FLASH_CARDS
    GUESSED_FLASH_CARDS[new_french_card] = new_english_card
    del FRESH_FLASH_CARDS[new_french_card]
    if not FRESH_FLASH_CARDS:
        FRESH_FLASH_CARDS = GUESSED_FLASH_CARDS
        GUESSED_FLASH_CARDS = {}
    window.config(bg=CORRECT_COLOR)
    canvas.config(bg=CORRECT_COLOR)
    window.after(3000, reset_count_down)


def wrong_answer():
    window.config(bg=WRONG_COLOR)
    canvas.config(bg=WRONG_COLOR)
    window.after(3000, reset_count_down)


# ----------------------------------- UI SETUP -------------------------------
window = tk.Tk()
window.title("Flash Cards")
window.config(padx=10, pady=10, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(width=800, height=626)
card_front = tk.PhotoImage(file="images/card_front.png")
card = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
language = canvas.create_text(400, 150, text="Title", font=('Ariel', 40, 'italic'))
word = canvas.create_text(400, 263, text="Word", font=('Courier', 60, 'bold'))
card_back = tk.PhotoImage(file="images/card_back.png")
canvas.grid(row=0, column=0, columnspan=2)

cross_image = tk.PhotoImage(file="images/wrong.png")
wrong_button = tk.Button(image=cross_image, command=wrong_answer)
wrong_button.config(highlightthickness=0)

tick_image = tk.PhotoImage(file="images/right.png")
right_button = tk.Button(image=tick_image, command=right_answer)
right_button.config(highlightthickness=0)

generate_flash_card()
canvas.itemconfig(language, text="French")
canvas.itemconfig(word, text=new_french_card)

count_down()

window.mainloop()
