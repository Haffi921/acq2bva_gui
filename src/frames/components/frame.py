from tkinter import ttk


class Frame(ttk.Frame):
    def __init__(self, container, height, width, padding, **kwargs) -> None:
        super().__init__(
            container, height=height, width=width, padding=padding, **kwargs
        )

    def validate(self) -> tuple[bool, str | None]:
        raise NotImplemented
