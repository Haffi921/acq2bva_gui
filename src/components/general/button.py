import tkinter as tk
from tkinter import ttk


class Button(ttk.Button):
    def __init__(self, container, text, **kwargs):
        super().__init__(container, text=text, **kwargs)

    def set_command(self, command) -> None:
        self.config(command=command)

    def make_active(self) -> None:
        self.config(state=tk.ACTIVE)

    def enable(self) -> None:
        self.config(state=tk.NORMAL)

    def disable(self) -> None:
        self.config(state=tk.DISABLED)

    def is_active(self) -> bool:
        return str(self["state"]) == tk.ACTIVE

    def is_enabled(self) -> bool:
        return str(self["state"]) == tk.NORMAL

    def is_disabled(self) -> bool:
        return str(self["state"]) == tk.DISABLED

    def get_state(self) -> str:
        return str(self["state"])


if __name__ == "__main__":
    root = tk.Tk()
    btn = Button(root, "Continue", state=tk.ACTIVE)

    def toggle_state():
        print(btn.get_state())
        if btn.is_enabled():
            btn.make_active()
        elif btn.is_active():
            btn.disable()
            btn.after(1000, toggle_state)
        else:
            btn.enable()

    btn.set_command(toggle_state)

    btn.pack()
    root.mainloop()
