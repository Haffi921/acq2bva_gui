from interfaces.frame import Frame


class Page(Frame):
    def __init__(self, container, **kwargs) -> None:
        self.loaded = False

        super().__init__(container, **kwargs)

    def load(self) -> None:
        self.tkraise()
        self.loaded = True

    def validate(self) -> None:
        raise NotImplemented
