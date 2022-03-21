import tkinter as tk

from interfaces.frame import Frame
from components.general.list_box import ListBox
from components.constants import NORMAL_COLOR, ERROR_COLOR


class AcqList(Frame):
    def __init__(self, container, **kwargs) -> None:
        self.error_count = 0

        super().__init__(container, **kwargs)

    def create_components(self) -> None:
        self.acq_file_list = ListBox(
            self,
            bg="lightgray",
            borderwidth=0,
            highlightbackground=NORMAL_COLOR,
        )
        self.no_files_label = tk.Label(
            self,
            text="No .acq files in directory...",
            bg="lightgray",
            fg="gray34",
        )

        self.acq_file_list.bindtags((self.acq_file_list, self, "all"))

    def geometry(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def pack_components(self) -> None:
        self.acq_file_list.grid(column=0, row=0, sticky=tk.NSEW)
        self.no_files_label.grid(column=0, row=0)

    def get_list(self) -> tuple[str]:
        return self.acq_file_list.get_list()

    def set_list(self, new_values: tuple[str]) -> None:
        self.acq_file_list.set_list(new_values)
        if len(new_values):
            self.no_files_label.grid_forget()
        else:
            self.no_files_label.grid()

    def highlight_error(self):
        self.error_count += 1
        self.error_border()
        self.after(700, self.remove_error)

    def remove_error(self):
        self.error_count -= 1
        if self.error_count < 1:
            self.normal_border()

    def normal_border(self):
        self.acq_file_list.config(highlightbackground=NORMAL_COLOR)

    def error_border(self):
        self.acq_file_list.config(highlightbackground=ERROR_COLOR)
