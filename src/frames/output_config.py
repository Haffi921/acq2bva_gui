import tkinter as tk
import tkinter.filedialog as fd

from pathlib import Path

from .components.frame import Frame
from .components.widgets import ImageButton, FolderEntry


class OutputConfig(Frame):
    def __init__(self, container, height, width, padding, **kwargs) -> None:
        super().__init__(container, height, width, padding, **kwargs)

        # Class variables
        self.current_dir = Path.home() / "bva_data"

        self.error_color = "red"
        self.warning_color = "yellow"
        self.normal_color = "black"

        self.folder = FolderEntry(
            self, self.current_dir, self.validate_folder, width=40
        )
        self.open_folder = ImageButton(self, "./icons/open_folder.png", self.open_dir)
        # self.channel_list =

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=30)
        self.folder.grid(column=0, row=0, sticky=tk.EW, padx=1)
        self.open_folder.grid(column=1, row=0, sticky=tk.E, padx=1)

    def open_dir(self):
        if new_folder := fd.askdirectory(initialdir=self.current_dir):
            self.folder.set_value(new_folder)

    def is_current_dir_empty(self):
        return next(self.current_dir.iterdir(), None) == None

    def is_current_dir_bva_output(self):
        ext_list = []
        for file in self.current_dir.iterdir():
            if file.is_file() and file.suffix not in ext_list:
                ext_list.append(file.suffix)

        extra_ext = set(ext_list).difference([".dat", ".vhdr", ".vmrk"])

        if len(extra_ext) == 1:
            return len(extra_ext.difference([".wksp2"])) == 0

        return len(extra_ext) == 0

    def validate_folder(self, *args):
        new_directory = Path(self.folder.get_value()).resolve()
        if self.current_dir != new_directory:
            self.current_dir = new_directory

            self.remove_info_message()

            if not self.current_dir.parent.is_dir():
                self.display_info_message("Parent directory does not exist")

            else:

                if self.current_dir.is_dir() and not self.is_current_dir_empty():
                    if self.is_current_dir_bva_output():
                        self.display_info_message(
                            "Directory contains BVA data that will be overwritten"
                        )
                    else:
                        self.display_info_message(
                            "Highly recommend an empty output directory"
                        )
