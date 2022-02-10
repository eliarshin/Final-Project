

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

import pandas as pd


class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("crack the password")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand="true")
        self.geometry("900x500")



class DataTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")
        self.stored_dataframe = pd.DataFrame()






if __name__ == "__main__":
    root = Application()
    root.mainloop()