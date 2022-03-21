import tkinter as tk


class Entry(tk.Entry):
    def __init__(self, container, value="", **kwargs) -> None:
        self.value = tk.StringVar(container, value=value)
        super().__init__(container, textvariable=self.value, **kwargs)

    def get_value(self) -> str:
        return self.value.get()

    def set_value(self, new_value) -> None:
        self.value.set(new_value)
        self.xview_moveto(1)

    def trace_add(self, func) -> str:
        return self.value.trace_add("write", func)

    def trace_remove(self, cbname) -> None:
        self.value.trace_remove("write", cbname)
