import time
import sys
import socket
from tkinter import *
from datetime import datetime
import os


print("hello")

# This class has a ping and nslookup function
class Scanner(object):

    def __str__(self):
        return "-----END OF ACTION------"


    def pinger(self):

        gui.txt1.delete("1.0", END)
        ip = gui.ent.get()
        result = os.popen("ping {0}".format(ip)).read()
        gui.txt1.insert(END, result)
        gui.txt1.insert(END, rsp)


    def looker(self):
        gui.txt1.delete("1.0", END)
        ip = gui.ent.get()
        result = os.popen("nslookup {0}".format(ip)).read()
        gui.txt1.insert(END, result)
        gui.txt1.insert(END, rsp)


# this class have Port scan function
class Porter(object):
    def __init__(self):
        self.start_time = datetime.now()

    def portis(self):
        gui.txt1.delete("1.0", END)
        target = gui.ent.get()
        gui.txt1.insert(END,"-" * 10)
        gui.txt1.insert(END, "\nScanning Target: " + target)
        gui.txt1.insert(END, "\nScanning started at:" + str(self.start_time))
        gui.txt1.insert(END, "-" * 10)

        try:
            for port in range(1, 450):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.5)

                # returns an error indicator
                result = s.connect_ex((target, port))
                if result == 0:
                    gui.txt1.insert(END, "\nPort {} is open".format(port))
                s.close()

        except socket.gaierror:
            gui.txt1.insert(END,"Hostname Could Not Be Resolved!")
            time.sleep(1)
            sys.exit()
        except socket.error:
            gui.txt1.insert(END, "Server not responding!")
            sys.exit()


class Gui:
    
    def __init__(gui): 
        gui.root = Tk()
        gui.btn1 = Button(gui.root, text="pinger", command=rsp.pinger)
        gui.txt1 =Text(gui.root, width=60)
        gui.btn2=Button(gui.root, text="looker", command=rsp.looker)
        gui.btn3=Button(gui.root, text="port scan", command=rsd.portis)
        gui.lbl1=Label(gui.root, text="Insert IP or Domain >>")
        gui.ent =Entry(gui.root, width=20)

    def create_screen(gui):
        gui.root.title('PT Framework')
        gui.root.geometry("500x500")
        gui.root.resizable(False, False)
        m1c = '#00ee00'
        bgc = '#222222'
        dbg = '#000000'
        fgc = '#111111'
        gui.root.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc, highlightColor=m1c,
                   highlightBackground=m1c)

        gui.btn1.place(x=420, y=15)
    
        gui.btn2.place(x=360, y=15)
     
        gui.btn3.place(x=280, y=15)

        gui.txt1.place(x=4, y=100)

        gui.lbl1.place(x=2, y=20)

        gui.ent.place(x=150, y=20)


#starting GUI

if __name__ == "__main__":
    rsp = Scanner()
    rsd = Porter()
    gui = Gui()
    gui.create_screen()
    gui.root.mainloop()


    
# # lets start these classes!
# rsp = Scanner()
# rsd = Porter()


# # configuring the Tkinter GUI
# root = Tk()
# root.title('PT Framework')
# root.geometry("500x500")
# root.resizable(False, False)

# # ==== Colors ====
# m1c = '#00ee00'
# bgc = '#222222'
# dbg = '#000000'
# fgc = '#111111'
# root.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc, highlightColor=m1c,
#                    highlightBackground=m1c)

# btn1 = Button(root, text="pinger", command=rsp.pinger)
# btn1.place(x=420, y=15)
# btn2 = Button(root, text="looker", command=rsp.looker)
# btn2.place(x=360, y=15)
# btn3 = Button(root, text="port scan", command=rsd.portis)
# btn3.place(x=280, y=15)

# txt1 = Text(root, width=60)
# txt1.place(x=4, y=100)

# lbl1 = Label(root, text="Insert IP or Domain >>")
# lbl1.place(x=2, y=20)

# ent = Entry(root, width=20)
# ent.place(x=150, y=20)


# #starting GUI
# root.mainloop()



