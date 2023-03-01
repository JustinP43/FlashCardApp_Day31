#-----------------------------IMPORTS-----------------------------#
from tkinter import *
import pandas
import random

#-----------------------------VARIABLES-----------------------------#
BACKGROUND_COLOR = "#B1DDC6"

CARD_FRONT = "./images/card_front.png"
CARD_BACK = "./images/card_back.png"
CORRECT = "./images/right.png"
WRONG = "./images/wrong.png"
#-----------------------------FLASH CARD-----------------------------#
try: 
    data = pandas.read_csv("./data/words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv").to_dict(orient="records")
finally:
    to_learn = data
    current_card = {}

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data)
    french_word = current_card["French"]
       
    canvas.itemconfig(flashcard,image=front_card)
    canvas.itemconfig(title_text,text="French",fill="black") 
    canvas.itemconfig(word_text,text=french_word,fill="black")
    flip_timer = window.after(3000,func=flip_card)

def flip_card():
    canvas.itemconfig(flashcard,image=back_card)
    canvas.itemconfig(title_text,text="English",fill="white") 
    canvas.itemconfig(word_text,text=current_card["English"],fill="white")
    
def is_known():
    to_learn.remove(current_card)
    new_list = pandas.DataFrame(to_learn)
    new_list.to_csv("./data/words_to_learn.csv",index=False)

    next_card()

#-----------------------------USER INTERFACE-----------------------------#
window =Tk()
window.title("Flashcard App")
window.config(bg=BACKGROUND_COLOR,padx=50,pady=50)

flip_timer = window.after(3000,func=flip_card)

front_card = PhotoImage(file=CARD_FRONT)
back_card = PhotoImage(file=CARD_BACK)
correct = PhotoImage(file=CORRECT)
wrong = PhotoImage(file=WRONG)

canvas = Canvas(width=800,height=526,highlightthickness=0,bg=BACKGROUND_COLOR)
flashcard = canvas.create_image(410,265,image=front_card)
title_text = canvas.create_text(400,150,text="Title",font=("Ariel",50,"italic"))
word_text = canvas.create_text(400,263,text="Word",font=("Ariel",60,"bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_btn = Button(image=wrong,highlightthickness=0,bg=BACKGROUND_COLOR,padx=50,command=next_card)
wrong_btn.grid(row=1, column=0)

correct_btn = Button(image=correct,highlightthickness=0,bg=BACKGROUND_COLOR,padx=50,command=is_known)
correct_btn.grid(row=1,column=1)


next_card()


window.mainloop()