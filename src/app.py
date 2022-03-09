import tkinter as tk
from tkinter import ttk


class Frame(ttk.Frame):
    def __init__(self, container, height, width, padding) -> None:
        super().__init__(container, height=height, width=width, padding=padding)

    def can_continue(self) -> bool:
        raise NotImplemented


class Button(ttk.Button):
    def __init__(self, container, text, default_state, command, **kwargs):
        super().__init__(
            container, text=text, state=default_state, command=command, **kwargs
        )

    def make_active(self) -> None:
        self.config(state=tk.ACTIVE)

    def enable(self) -> None:
        self.config(state=tk.NORMAL)

    def disable(self) -> None:
        self.config(state=tk.DISABLED)

    def is_disabled(self) -> bool:
        return str(self["state"]) == tk.DISABLED


class App(tk.Tk):
    def __init__(self, width, height, title=None, icon=None, **kwargs) -> None:
        super().__init__(**kwargs)

        # Class variables
        self.index = 0
        self.frames = [5, 6, 7, 8, 9, 10]
        self.current_frame = self.frames[self.index]
        self.MIN = 0
        self.MAX = len(self.frames) - 1

        # Options
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

        # Title and icon
        if title:
            self.title(title)
        if icon:
            self.iconphoto(False, tk.PhotoImage(icon))

        # Buttons
        self.continue_button = Button(self, "Continue", tk.ACTIVE, self.forward)
        self.back_button = Button(self, "Back", tk.DISABLED, self.backward)

        self.continue_button.pack(side=tk.RIGHT)
        self.back_button.pack(side=tk.RIGHT)

        self.mainloop()

    def forward(self):
        if self.current_frame.can_continue():
            self.index += 1
            self.current_frame = self.frames[self.index]

        if self.index == self.MAX:
            self.continue_button.disable()

        if self.back_button.is_disabled():
            self.back_button.enable()

        print(self.current_frame)

    def backward(self):
        self.index -= 1
        self.current_frame = self.frames[self.index]

        if self.index == self.MIN:
            self.back_button.disable()

        if self.continue_button.is_disabled():
            self.continue_button.make_active()

        print(self.current_frame)


if __name__ == "__main__":
    app = App(300, 300, "acq2bva")
