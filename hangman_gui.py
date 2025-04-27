import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from wonderwords import RandomWord
import string
import subprocess, sys

class Hangman(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman")
        self.header=tk.Label(self, text="HANGMAN", font=("Times New Roman", 25))
        self.header.pack(padx=10, pady=10)
        self.counter_process=0
        self.upperframe=tk.Frame(self)
        self.upperframe.pack(padx=10, pady=10)
        self.hangman_label=tk.Label(self.upperframe)
        self.show_process()
        self.new_word()
        self.keyboard()
        
        self.mainloop()

    def exit_hangman(self, state):
        self.destroy()
        if state:
            subprocess.Popen([sys.executable] + sys.argv)

    def keyboard(self):
        keyboard_frame=tk.Frame(self)
        keyboard_frame.pack(padx=10, pady=10)
        i=-1
        for r in range(3):
            for c in range(9):
                    i+=1
                    if i!=26:
                        letter_button=tk.Button(keyboard_frame,text=string.ascii_lowercase[i], font=("Times New Roman", 9), background="dark gray", foreground="white", relief=tk.RAISED, width=6, height=2)
                        letter_button.bind("<Button-1>", self.hangman_word) # 3 row *9 
                    else:
                        letter_button=tk.Button(keyboard_frame,text="New\ngame", font=("Times New Roman", 9), background="dark gray", foreground="white", relief=tk.RAISED, width=6, height=2, command= lambda:self.exit_hangman(True))
                    
                    letter_button.grid(row=r, column=c)

    def show_process(self):
        self.counter_process+=1
        path="D:\\Daniel Rabe\\Downloads\\hangman\\"
        step=Image.open(path + str(self.counter_process)+".jpg")
        step=step.resize((160, 280))        
        step_tk=ImageTk.PhotoImage(step)
        self.hangman_label.config(image=step_tk)
        self.hangman_label.image=step_tk
        self.hangman_label.pack(padx=10, pady=10, side=tk.LEFT)
        if self.counter_process==8:
            if messagebox.askyesno("Game Information", f"You lost!\nThe correct word would have been: '{self.my_word}.'\nDo you want to play again?"):
                self.exit_hangman(True)
            else:
                self.exit_hangman(False)    

    def new_word(self):
        self.r=RandomWord()
        while True:
            self.my_word=self.r.word(word_min_length=7, include_categories=["noun"])
            if all(z in string.ascii_letters for z in self.my_word):
                break
        self.word_str=tk.StringVar()
        self.word__label=tk.Label(self.upperframe, textvariable=self.word_str, font=("Times New Roman", 15, "bold")) 
        self.word_str.set(" ".join("_" for x in self.my_word))
        self.word__label.pack(padx=10, pady=10, side=tk.RIGHT)     

    def hangman_word(self, event):
        self.update_word=list(self.word_str.get().split(" "))
        selected_button=event.widget
        selected_letter=selected_button.cget("text")
        selected_button.destroy()
        if selected_letter.lower() in self.my_word.lower():
            indices =[y[0] for y in enumerate(self.my_word) if y[1].lower()==selected_letter.lower()]
            while indices:
                self.update_word[indices[-1]]=selected_letter.lower()
                indices.pop(-1)
                self.word_str.set(" ".join(self.update_word))
                if "".join(self.update_word)==self.my_word:
                    if messagebox.askyesno("Game Information", "You won! Do you want to play again?"):
                        self.exit_hangman(True)
                    else:
                        self.exit_hangman(False)    
        else:
            self.show_process()            

start=Hangman()                                    