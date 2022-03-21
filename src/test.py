import tkinter as tk

from components.acq_list import AcqList

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x300")
    acq_list = AcqList(root)
    acq_list.pack()
    root.mainloop()
