import tkinter as tk

window = tk.Tk()
window.title("Menu for snake game")

text = tk.StringVar()
label = tk.Label(window, textvariable=text, padx=100, pady=20)
label.pack()
text.set( "Choose game ;)")




def play_cleaner():
    import pl.karol.dziachan.cleaner.cleaner

def play_snake():
    import pl.karol.dziachan.snake.snake as snake


def inst_snake():
    pass
def inst_cleaner():
    pass
def score():
    pass

snake = tk.Button(window, text="Snake", width=20, command=play_snake)
cleaner = tk.Button(window, text="Cleaner", width=20, command=play_cleaner)

snake.pack()
cleaner.pack()


tk.mainloop()  
