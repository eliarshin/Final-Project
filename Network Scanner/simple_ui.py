from tkinter import Tk, Button, Label, Entry, Listbox, Text, MULTIPLE


window = Tk()
window.title('Testing UI')
window.geometry("400x300")
window.resizable(False, False)

lbl1 = Label(window, text="target")
lbl1.place(x=5,y=10)

ent1 = Entry(window, width="44")
ent1.place(x=70,y=10)
btn1 = Button(window, text="submit")
btn1.place(x=350,y=5)

lstbox1 = Listbox(window, selectmode=MULTIPLE )
lstbox1.insert(1, "Advanced scan")
lstbox1.insert(2, "regular scan")
lstbox1.insert(3, "network scan")
lstbox1.place(x=0, y=35)

txt = Text(window, width=10)
txt.place(x=170,y= 35)

window.mainloop()
