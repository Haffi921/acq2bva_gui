import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path

from PIL import Image, ImageTk

from .frame import Frame


class ImageButton(tk.Button):
    def __init__(
        self, container, image_path, command, width=15, height=15, **kwargs
    ) -> None:
        self.image = ImageTk.PhotoImage(
            Image.open(image_path).resize((width, height), Image.ANTIALIAS)
        )
        super().__init__(container, image=self.image, command=command, **kwargs)


class FolderEntry(tk.Entry):
    def __init__(self, container, value, validator, **kwargs) -> None:
        self.value = tk.StringVar(container, value=value)
        super().__init__(container, textvariable=self.value, **kwargs)
        self.value.trace_add("write", validator)

    def get_value(self) -> str:
        return self.value.get()

    def set_value(self, new_value):
        self.value.set(new_value)
        self.xview_moveto(1)


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
    def __init__(self, container, height, width, padding) -> None:
        super().__init__(container, height, width, padding)

        # Class variables
        self.current_dir = Path.home()
        self.files = ()

        # Components
        self.folder = FolderEntry(self, self.current_dir, self.validate_folder)
        self.open_folder = ImageButton(self, "../icons/open_folder.png", self.open_dir)
        self.file_list = FileList(self)

        # Layout
        self.folder.grid(column=0, row=0, sticky=tk.EW)
        self.open_folder.grid(column=1, row=0, sticky=tk.EW)
        self.file_list.grid(column=0, row=1, columnspan=2, sticky=tk.NSEW)

        self.pack(expand=True, fill="both")

    def can_continue(self) -> bool:
        return self.current_dir.is_dir() and len(self.files) != 0

    def validate_folder(self):
        new_directory = Path(self.folder.get_value()).resolve()
        if (
            new_directory.exists()
            and new_directory.is_dir()
            and self.current_folder != new_directory
        ):
            self.current_folder = new_directory
            self.scan_dir()

    def scan_dir(self):
        new_files = []
        for file in self.current_folder.iterdir():
            if file.is_file() and file.match("*.acq"):
                new_files.append(Path(file.parent.name, file.name))
        self.files = tuple(new_files)
        self.file_list.set_list(self.files)

    def open_dir(self):
        if new_folder := fd.askdirectory(initialdir=self.current_dir):
            self.folder.set_value(new_folder)
