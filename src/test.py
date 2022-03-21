import tkinter as tk

from components.acq_list import AcqList

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x300")
    acq_list = AcqList(root)
    acq_list.pack()
    root.after(1000, lambda: acq_list.set_list(("Hello", "No")))
    root.after(2000, lambda: acq_list.set_list(""))
    root.mainloop()
