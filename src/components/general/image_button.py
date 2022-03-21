import tkinter as tk

from pathlib import Path

from PIL import Image, ImageTk


class ImageButton(tk.Button):
    def __init__(
        self, container, image_path, command, width=15, height=15, **kwargs
    ) -> None:
        image_path = str(Path(image_path).resolve())
        self.image = ImageTk.PhotoImage(
            Image.open(image_path).resize((width, height), Image.ANTIALIAS)
        )
        super().__init__(container, image=self.image, command=command, **kwargs)
