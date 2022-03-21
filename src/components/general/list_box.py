import tkinter as tk


class ListBox(tk.Listbox):
    def __init__(self, container, **kwargs):
        self.list = tk.StringVar()
        super().__init__(
            container,
            listvariable=self.list,
            width=65,
            **kwargs,
        )

    def get_list(self) -> tuple[str]:
        return self.list.get()

    def set_list(self, new_values: tuple[str]) -> None:
        self.list.set(new_values)

    def trace_add(self, func) -> str:
        self.list.trace_add("write", func)

    def trade_remove(self, cbname) -> None:
        self.list.trace_remove("write", cbname)
