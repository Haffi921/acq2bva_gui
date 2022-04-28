import tkinter as tk
from typing import Callable

from components.general.button import Button
from interfaces.frame import Frame

## Model
class Indexer:
    def __init__(self, maximum) -> None:
        self.MIN, self.index = 0, 0
        self.MAX = max(maximum, 0)

    def decrease(self) -> int:
        if self.index > self.MIN:
            self.index -= 1
        return self.index

    def increase(self) -> int:
        if self.index < self.MAX:
            self.index += 1
        return self.index

    def is_min(self) -> bool:
        return self.index == self.MIN

    def is_max(self) -> bool:
        return self.index == self.MAX


## View
class Paginator(Frame):
    def __init__(
        self,
        container: Frame,
        max: int,
        btn_func: tuple[Callable[[], None], Callable[[], None]],
        **kwargs
    ) -> None:
        self.indexer = Indexer(maximum=max)

        self.back_button = None
        self.next_btn = None

        self.back_func, self.next_func = btn_func

        super().__init__(container, **kwargs)

        self.refresh_state()

    def index(self) -> int:
        return self.indexer.index

    def refresh_state(self) -> None:
        if self.indexer.is_min():
            self.back_button.disable()
        else:
            self.back_button.enable()

        if self.indexer.is_max():
            self.next_btn.disable()
        else:
            self.next_btn.make_active()

    def back(self) -> None:
        self.indexer.decrease()
        self.refresh_state()
        self.back_func()

    def next(self) -> None:
        self.indexer.increase()
        self.refresh_state()
        self.next_func()

    def create_components(self) -> None:
        self.back_button = Button(self, "Back", state=tk.DISABLED, command=self.back)
        self.next_btn = Button(self, "Continue", state=tk.ACTIVE, command=self.next)

    def pack_components(self) -> None:
        self.back_button.pack(side=tk.RIGHT)
        self.next_btn.pack(side=tk.RIGHT, padx=10, before=self.back_button)
