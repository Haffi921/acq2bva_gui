import tkinter as tk
from tkinter import ttk


from frames import FolderSelect


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
        self.frames = [FolderSelect(self, width, height, (12, 12, 12, 0))]
        self.current_frame = self.frames[self.index]
        self.MIN = 0
        self.MAX = len(self.frames) - 1

        # Options
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file="./icons/file.png"))

        # Title and icon
        if title:
            self.title(title)
        if icon:
            self.iconphoto(False, tk.PhotoImage(icon))

        # Buttons
        self.button_frame = ttk.Frame(self)
        self.continue_button = Button(
            self.button_frame, "Continue", tk.ACTIVE, self.forward
        )
        self.back_button = Button(self.button_frame, "Back", tk.DISABLED, self.backward)

        # Error message
        self.error_frame = ttk.Frame(self, height=20)
        self.error_message = ttk.Label(self.error_frame, padding=(12, 0))

        # Packing
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        for frame in self.frames:
            frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.error_frame.grid(column=0, row=1, sticky=tk.NSEW)
        self.button_frame.grid(column=0, row=2, sticky=tk.NSEW)

        self.continue_button.pack(side=tk.RIGHT, padx=10)
        self.back_button.pack(side=tk.RIGHT)
        self.error_message.pack(side=tk.LEFT, fill="x")

        self.mainloop()

    def forward(self):
        can_continue, error_msg = self.current_frame.validate()
        if can_continue:
            self.index += 1
            self.current_frame = self.frames[self.index]

            if self.index == self.MAX:
                self.continue_button.disable()

            if self.back_button.is_disabled():
                self.back_button.enable()

        if error_msg:
            self.error_message.config(text=error_msg)
            self.error_message.after(2000, lambda: self.error_message.config(text=""))

    def backward(self):
        can_continue, error_msg = self.current_frame.validate()
        if can_continue:
            self.index -= 1
            self.current_frame = self.frames[self.index]

            if self.index == self.MIN:
                self.back_button.disable()

            if self.continue_button.is_disabled():
                self.continue_button.make_active()

        if error_msg:
            self.error_message.config(text=error_msg)
            self.error_message.after(2000, lambda: self.error_message.config(text=""))


if __name__ == "__main__":
    app = App(300, 350, "acq2bva")
