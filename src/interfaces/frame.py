from tkinter import ttk


class Frame(ttk.Frame):
    def __init__(self, container, **kwargs) -> None:
        super().__init__(container, **kwargs)

        self.create_components()
        self.geometry()
        self.pack_components()

    def create_components(self) -> None:
        raise NotImplemented

    def geometry(self) -> None:
        pass

    def pack_components(self) -> None:
        raise NotImplemented
