from textwrap import fill
import tkinter as tk
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

try:
  data = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
  data = pd.read_csv('data/french_words.csv')
  to_learn = pd.DataFrame.to_dict(data, orient='records')
  print('brand new')
else:
  to_learn = pd.DataFrame.to_dict(data, orient='records')
  print('to learn')

current_card = {}

# Logic
def next_card():
  global current_card, flip_timer, df
  window.after_cancel(flip_timer)
  current_card = choice(to_learn)
  flash_card.itemconfig(card_image, image=card_front)
  flash_card.itemconfig(card_title, text='French', fill='black')
  flash_card.itemconfig(card_word, text=current_card['French'], fill='black')
  flip_timer = window.after(4000, flip_card)

def is_known():
  to_learn.remove(current_card)
  df = pd.DataFrame(to_learn)
  print(len(to_learn))
  df.to_csv('data/to_learn.csv')
  next_card()
  
def flip_card():
  global current_card
  flash_card.itemconfig(card_image, image=card_back)
  flash_card.itemconfig(card_title, text='English' ,fill='white')
  flash_card.itemconfig(card_word, text=current_card['English'], fill='white')

# 


window = tk.Tk()
window.title('Flashy')
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(4000, flip_card)

card_back = tk.PhotoImage(file='images/card_back.png')
card_front = tk.PhotoImage(file='images/card_front.png')
flash_card = tk.Canvas(highlightthickness=0, width=800, height=526, bg=BACKGROUND_COLOR)
card_image = flash_card.create_image(400, 263, image=card_front)
card_title = flash_card.create_text(400 ,150 ,text='', font=('Arial', 40, 'italic'))
card_word = flash_card.create_text(400 ,263 ,text='', font=('Arial', 60, 'bold'))
flash_card.grid(column=0, row=0, columnspan=2)

right_image = tk.PhotoImage(file="images/right.png")
right_button = tk.Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=0, row=1)

wrong_image = tk.PhotoImage(file="images/wrong.png")
wrong_button = tk.Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()


window.mainloop()
