import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path

from .components.frame import Frame
from .components.widgets import ImageButton, FolderEntry


class FileList(tk.Listbox):
    def __init__(self, container, **kwargs):
        self.list = tk.StringVar()
        super().__init__(
            container,
            listvariable=self.list,
            width=65,
            **kwargs,
        )
        self.bindtags((self, container, "all"))

    def set_list(self, new_values: tuple):
        self.list.set(new_values)


class FolderSelect(Frame):
    def __init__(self, container, height, width, padding, **kwargs) -> None:
        super().__init__(container, height, width, padding, **kwargs)

        # Class variables
        self.current_dir = Path.home()
        self.files = ()

        self.error_color = "red"
        self.normal_color = "black"

        # Grid
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=30)

        # Components
        self.folder = FolderEntry(
            self, self.current_dir, self.validate_folder, width=40
        )
        self.open_folder = ImageButton(self, "./icons/open_folder.png", self.open_dir)
        self.file_list = FileList(
            self, bg="lightgray", borderwidth=0, highlightbackground=self.normal_color
        )

        # Layout
        self.folder.grid(column=0, row=0, sticky=tk.NSEW, padx=1)
        self.open_folder.grid(column=1, row=0, sticky=tk.E, padx=1)
        self.file_list.grid(column=0, row=1, columnspan=2, sticky=tk.NSEW, pady=(10, 0))

        # self.pack(expand=True, fill="both", padx=10, pady=10)

    def can_continue(self) -> bool:
        if not self.current_dir.is_dir():
            self.folder.config(fg=self.error_color)
            self.folder.after(700, lambda: self.folder.config(fg=self.normal_color))
            self.display_info_message("Directory does not exist")
            return False

        if len(self.files) == 0:
            self.file_list.config(highlightbackground=self.error_color)
            self.file_list.after(
                700,
                lambda: self.file_list.config(highlightbackground=self.normal_color),
            )
            self.display_info_message("There are no .acq files in this directory")
            return False

        return (True, None)

    def validate_folder(self, *args):
        new_directory = Path(self.folder.get_value()).resolve()
        if self.current_dir != new_directory:
            self.current_dir = new_directory
            self.files = ()
            self.file_list.set_list(self.files)

            if self.current_dir.exists() and self.current_dir.is_dir():
                self.scan_dir()

    def scan_dir(self):
        new_files = []
        for file in self.current_dir.iterdir():
            if file.is_file() and file.match("*.acq"):
                new_files.append(Path(file.parent.name, file.name))
        self.files = tuple(new_files)
        self.file_list.set_list(self.files)

    def open_dir(self):
        if new_folder := fd.askdirectory(initialdir=self.current_dir):
            self.folder.set_value(new_folder)
