#Start working on gui
from distutils import command
from sys import builtin_module_names
from tkinter import *
from tkinter.tix import TEXT
from matplotlib.pyplot import text

from pyparsing import col



root = Tk() # create the tkinter interface

############ entry

e = Entry(root,width=50,bg="green",fg="white",borderwidth=2)
e.pack() 
e.insert(0,"Enter your name : ") #put default text

############ function and button
def my_click():
    label = Label(root,text=e.get())
    label.pack()

btn = Button(root,text="click me",padx=50, command = my_click, fg="blue",bg="cyan")
btn.pack()

################################GRIDS AND LABELS#################################
# #create lale widge
# my_label = Label(root, text="Hello World!")
# my_label1 = Label(root, text="we are testing our things")

# #shoving it on screen
# #my_label.pack()

# #grid the lables - it is relative to the text inside
# my_label.grid(row = 0, column=0)
# my_label1.grid(row = 1, column=0)


#it create the loop to the screen
root.mainloop()