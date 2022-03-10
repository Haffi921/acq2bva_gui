from tkinter import ttk


class Frame(ttk.Frame):
    def __init__(self, container, height, width, padding) -> None:
        super().__init__(container, height=height, width=width, padding=padding)

    def can_continue(self) -> bool:
        raise NotImplemented
