import tkinter as tk

from pathlib import Path

from .components.frame import Frame
from .components.widgets import ImageButton, FolderEntry


class OutputConfig(Frame):
    def __init__(self, container, height, width, padding, **kwargs) -> None:
        super().__init__(container, height, width, padding, **kwargs)

        # Class variables
        self.current_dir = Path.home()

        self.error_color = "red"
        self.normal_color = "black"
