"""Lightweight Tkinter interface for launching WAAPI helper scripts."""

from __future__ import annotations

import tkinter as tk


class Interface(tk.Tk):
    """Simple window that will eventually host script launch controls."""

    def __init__(self) -> None:
        """Initialise the root window with a placeholder button."""

        super().__init__()
        self.title("WAAPI Script Manager")
        self.minsize(720, 480)
        btn = tk.Button(self, text="Boton")
        btn.pack()


if __name__ == "__main__":
    root = Interface()
    root.mainloop()
