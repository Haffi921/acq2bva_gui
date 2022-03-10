import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path

from PIL import Image, ImageTk

from .frame import Frame


class ImageButton(tk.Button):
    def __init__(
        self, container, image_path, command, width=15, height=15, **kwargs
    ) -> None:
        image_path = str(Path(image_path).resolve())
        print(image_path)
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
        self.file_list = FileList(self, bg="lightgray", borderwidth=0)

        # Layout
        self.folder.grid(column=0, row=0, sticky=tk.NSEW, padx=1)
        self.open_folder.grid(column=1, row=0, sticky=tk.E, padx=1)
        self.file_list.grid(column=0, row=1, columnspan=2, sticky=tk.NSEW, pady=6)

        self.pack(expand=True, fill="both", padx=10, pady=10)

    def can_continue(self) -> bool:
        if not self.current_dir.is_dir():
            self.folder.config(fg="red")
            self.folder.after(700, lambda: self.folder.config(fg="black"))
            return False
        if len(self.files) == 0:
            self.file_list.config(highlightbackground="red")
            return False
        return True

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
