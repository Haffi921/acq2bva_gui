import tkinter as tk
import tkinter.filedialog as fd

from PIL import ImageTk, Image

from pathlib import Path


STARTING_PATH = Path.home()


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


class FolderSelector(tk.Frame):
    def __init__(
        self, root: tk.Tk, padding: int | tuple[int, int] = 0, **kwargs
    ) -> None:

        self.current_folder = Path(STARTING_PATH)
        self.input_folder = None
        self.open_folder = None
        self.file_list = None
        self.continue_btn = None

        if isinstance(padding, int):
            padding = (padding, padding)

        super().__init__(root, width=200, height=200, **kwargs)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=30)
        self.rowconfigure(2, weight=1)
        # self.columnconfigure(0, wi)

        self.create_folder_selector()

        self.pack(padx=padding[0], pady=padding[1], expand=True, fill="both")
        self.pack_components()

    def create_folder_selector(self):
        self.input_folder = FolderEntry(
            self, str(self.current_folder), self.validate_folder, width=60
        )
        self.open_folder = ImageButton(
            self, "./icons/open_folder.png", self.open_directory
        )
        self.file_list = FileList(self)
        self.continue_btn = tk.Button(self, text="Continue")

    def pack_components(self):
        self.input_folder.grid(column=0, row=0, padx=10)
        self.open_folder.grid(column=1, row=0, padx=10)
        self.file_list.grid(column=0, row=1, columnspan=2, sticky=tk.NSEW)
        # self.continue_btn.grid(column=1, row=2)

    def open_directory(self):
        if new_folder := fd.askdirectory(initialdir=self.current_folder):
            self.input_folder.set_value(new_folder)

    def validate_folder(self, *args):
        new_directory = Path(self.input_folder.get_value()).resolve()
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
            if file.is_file() and file.match("*.yaml"):
                new_files.append(Path(file.parent.name, file.name))
        self.file_list.set_list(tuple(new_files))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x450")
    root.resizable(False, False)

    FolderSelector(root, 15)

    root.mainloop()
