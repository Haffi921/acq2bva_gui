import tkinter as tk
from tkinter import ttk
from pathlib import Path

from interfaces.page import Page
from components.general.folder_selector import FolderSelector
from components.acq_list import AcqList


class InputFolder(FolderSelector):
    def __init__(self, container, label, **kwargs) -> None:
        super().__init__(container, label, **kwargs)

        self.files: list[Path] = []
        self.files_string = tk.StringVar()

    def validate_dir(self, *args) -> bool:
        if super().validate_dir():
            self.files = []
            self.files_string.set("")
            if self.current_dir.exists() and self.current_dir.is_dir():
                self.scan_dir()

    def scan_dir(self, *args):
        files = []
        for file in self.current_dir.iterdir():
            if file.is_file() and file.match("*.acq"):
                files.append(Path(file))
                file.parent.stem
        self.files = files
        self.files_string.set(files)


class OutputFolder(FolderSelector):
    def __init__(self, container, label, **kwargs) -> None:
        super().__init__(container, label, **kwargs)

    def validate_dir(self) -> bool:
        if super().validate_dir():
            if not self.current_dir.parent.exists():
                return False


class FolderSelect(Page):
    def __init__(self, container, **kwargs) -> None:
        self.input: InputFolder = None
        self.file_list: AcqList = None
        self.separator: ttk.Separator = None
        self.output: OutputFolder = None

        super().__init__(container, **kwargs)

    def get_clean_input_files(self):
        new_list = []
        for file in self.input.files:
            new_list.append(str(Path(file.parent.stem, file.stem)))
        return new_list

    def update_file_list(self, *args):
        self.file_list.set_list(self.get_clean_input_files())

    def create_components(self) -> None:
        self.input = InputFolder(self, "AcqKnowledge folder:", padding=(0, 0, 0, 12))
        self.file_list = AcqList(self)
        self.output = OutputFolder(self, "Output folder:", padding=(0, 12, 0, 12))

        self.input.files_string.trace_add("write", self.update_file_list)

    def geometry(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=30)
        self.rowconfigure(2, weight=1)

    def pack_components(self) -> None:
        self.input.grid(column=0, row=0)
        self.file_list.grid(column=0, row=1)
        self.output.grid(column=0, row=2)

    def validate(self) -> None:
        if not self.input.current_dir.is_dir():
            self.input.highlight_error()
            raise NotADirectoryError("Input directory does not exist")

        if len(self.input.files) == 0:
            self.input.highlight_error()
            self.file_list.highlight_error()
            raise FileNotFoundError("There are no .acq files in input directory")

        if not self.output.current_dir.parent.is_dir():
            self.output.highlight_error()
            raise NotADirectoryError("Output directory does not exist")
