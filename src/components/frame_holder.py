from typing import Callable

import tkinter as tk
from tkinter import ttk

from interfaces.frame import Frame

from components.info_message import InfoMessage
from components.paginator import Paginator


class PageViewer(Frame):
    def __init__(
        self,
        container: Frame,
        frames: list[Callable[[Frame], Frame]],
        padding=0,
        **kwargs
    ) -> None:

        self.frames = frames
        super().__init__(container, padding, **kwargs)

    def create_components(self) -> None:
        self.frames = map(lambda frame: frame(self), self.frames)
        self.info_message = InfoMessage(self, padding=(12, 0))
        self.paginator = Paginator(self, self.frames)

    def geometry(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def pack_components(self) -> None:
        for frame in self.frames:
            frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.info_message.grid(column=0, row=1, sticky=tk.NSEW)
        self.paginator.grid(column=0, row=2, sticky=tk.NSEW)
