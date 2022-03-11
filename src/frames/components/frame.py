from tkinter import ttk


class Frame(ttk.Frame):
    def __init__(self, container, height, width, padding, **kwargs) -> None:
        super().__init__(
            container, height=height, width=width, padding=padding, **kwargs
        )

    def can_continue(self) -> bool:
        raise NotImplemented

    def display_info_message(self, msg):
        self.master.display_info_message(msg)

    def remove_info_message(self):
        self.master.remove_info_message()
