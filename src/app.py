import tkinter as tk

from components.info_message import InfoMessage
from components.paginator import Paginator
from pages.folder_selection import FolderSelect


class App(tk.Tk):
    def __init__(self, width, height, title=None, icon=None, **kwargs) -> None:
        super().__init__(**kwargs)

        # Window geometry
        self.width = width
        self.height = height
        self.window_geometry()

        # Components
        self.create_components()
        self.set_geometry()
        self.pack_components()

        # Main loop
        self.mainloop()

    def window_geometry(self):
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file="./icons/file.png"))

    def create_components(self) -> None:
        self.frames = [
            FolderSelect(self, padding=(12, 12, 12, 0)),
        ]
        self.info_message = InfoMessage(self, padding=(0, 12, 0, 12))
        self.paginator = Paginator(
            self, 0, (lambda x: x, lambda x: x), padding=(0, 12, 0, 12)
        )
        self.current_frame = self.frames[self.paginator.index()]

    def set_geometry(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def pack_components(self) -> None:
        self.current_frame.grid(column=0, row=0)
        self.info_message.grid(column=0, row=1)
        self.paginator.grid(column=0, row=2)


m = App(300, 400)
