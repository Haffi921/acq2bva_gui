import tkinter as tk
from typing import Callable

from components.general.button import Button
from interfaces.frame import Frame

## Model
class Indexer:
    def __init__(self, max) -> None:
        self.MIN, self.index = 0, 0
        self.MAX = max(max, 0)

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
        super().__init__(container, **kwargs)

        self.indexer = Indexer(max=max)

        self.back_button = None
        self.next_btn = None

        self.back_func, self.next_func = btn_func

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
        self.back_button = Button(self, "Back", tk.DISABLED, self.back)
        self.next_btn = Button(self, "Continue", tk.ACTIVE, self.next)

    def pack_components(self) -> None:
        self.back_button.pack(side=tk.RIGHT, before=self.next_btn)
        self.next_btn.pack(side=tk.RIGHT, padx=10)
