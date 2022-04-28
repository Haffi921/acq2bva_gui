import tkinter as tk
from tkinter import ttk

from interfaces.frame import Frame


class InfoMessage(Frame):
    def __init__(self, container, padding=0, **kwargs) -> None:
        super().__init__(container, padding=padding, **kwargs)

    def create_components(self) -> None:
        self.label = ttk.Label(self)

    def pack_components(self) -> None:
        self.label.pack(side=tk.LEFT, fill="x")

    def set_msg(self, msg):
        self.label.config(text=msg)

    def clear_msg(self):
        self.label.config(text="")
