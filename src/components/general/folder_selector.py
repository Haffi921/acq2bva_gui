from pathlib import Path

import tkinter as tk
import tkinter.filedialog as fd

from interfaces.frame import Frame

from components.general.entry import Entry
from components.general.image_button import ImageButton


class FolderSelector(Frame):
    OPEN_FOLDER_ICON = "./icons/open_folder.png"
    FOLDER_HOME = str(Path.home().resolve())

    def __init__(self, container, **kwargs) -> None:
        self.folder: Entry = None
        self.open_folder: ImageButton = None

        self.current_dir = self.FOLDER_HOME

        super().__init__(container, **kwargs)

    def open_dir(self):
        if new_dir := fd.askdirectory(initialdir=self.current_dir):
            self.folder.set_value(str(Path(new_dir).resolve()))

    def validate_dir(self, *args) -> bool:
        new_dir = Path(self.folder.get_value().strip()).resolve()

        if self.current_dir != new_dir:
            self.current_dir = new_dir
            return True

        return False

    def create_components(self) -> None:
        self.folder = Entry(self, self.FOLDER_HOME, width=40)
        self.open_folder = ImageButton(self, self.OPEN_FOLDER_ICON, self.open_dir)

        self.folder.trace_add(self.validate_dir)

    def geometry(self) -> None:
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

    def pack_components(self) -> None:
        self.folder.grid(column=0, row=0, sticky=tk.NSEW, padx=(0, 4))
        self.open_folder.grid(column=1, row=0, sticky=tk.NSEW, padx=(4, 0))
