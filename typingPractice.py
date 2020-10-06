# cd  C:\Users\nellissery\Desktop\python code\py programs 
from tkinter import messagebox
from tkinter import *
import itertools
import random
import time
import datetime
import sqlite3

# constants
FONT_COLOR = itertools.cycle('red green blue yellow black #e313ec #583bc4 Aqua SaddleBrown'.split())
TEXT_SIZE = 256
# average length of a word is 4.7 letters


conn = sqlite3.connect("typingPracticeStats.db")
cursor = conn.cursor()


# database to upload scores, dates
# cursor.execute("""CREATE TABLE scores (
#                      WPM  integer,
#                      EPM  integer,
#                      DAT text )""")



# variables/inputs
letters = ""
letterCount = 0
errorCount = 0
startTime = 0

setup = Tk()
setup.title("setup")
setup.config(background="silver")
setup.resizable(width=False, height=False)

# setup function
def click():
    global letterEntry, letters
    letters = [letter for letter in letterEntry.get()]
    setup.destroy()

# creating setup widgets
label1 = Label(setup, text="type the letters needed to practice", bg="silver")
letterEntry = Entry(setup)
button1 = Button(setup, text="Enter", command=click)

# placing setup widgets
label1.grid(row=0, column=0)
letterEntry.grid(row=1, column=0)
button1.grid(row=2, column=0)

setup.mainloop()


# main screen
main = Tk()
main.title("typing practice")
mainMenu = Menu(main)
main.config(background="silver", menu=mainMenu)
main.geometry("400x400")
main.resizable(width=False, height=False)

def letterCheck(event):
    global textLabel, letterCount, startTime, errorCount
    print(textLabel["text"])
    if letterCount == 1 :
        startTime = time.time()
    if textLabel["text"] == event.char:
        letterCount += 1
        textLabel.pack_forget()
        textLabel = Label(text=random.choice(letters), fg=next(FONT_COLOR), bg="silver", font=("Helvetica", TEXT_SIZE))
        textLabel.pack(anchor=CENTER)
    else:
        errorCount += 1

def exitProccess(event=None):
    global textLabel, letterCount, startTime, errorCount
    wordCount = letterCount / 4.7
    timeTotal = time.time() - startTime
    d = datetime.datetime.now()

    conn = sqlite3.connect("typingPracticeStats.db")
    cursor = conn.cursor()
    
    # adding values into 
    cursor.execute("INSERT INTO scores VALUES (:WPM, :EPM, :DAT)",
                    {
                     "WPM":  int(wordCount / (timeTotal / 60)),           
                     "EPM":  int(errorCount / (timeTotal / 60)),
                     "DAT":  str(d.date())
                     })
    
    response = messagebox.showinfo(message=f"""your WPM was {int(wordCount / (timeTotal / 60))} at a rate of 
                                    {int(errorCount / (timeTotal / 60))} errors per minute on {d.date()}""")
    
    conn.commit()
    conn.close()


textLabel = Label(text=random.choice(letters), fg=next(FONT_COLOR), bg="silver",  font=("Helvetica", TEXT_SIZE))

tempButton = Button(text="End", command=exitProccess)
tempButton.bind("<Key>", letterCheck)

textLabel.pack(anchor=CENTER)
tempButton.pack(anchor=CENTER)


conn.commit()
conn.close()

main.mainloop()

