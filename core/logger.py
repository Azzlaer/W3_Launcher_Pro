from __future__ import annotations

from datetime import datetime
from tkinter import END, Text


class GuiLogger:
    def __init__(self, text_widget: Text | None = None):
        self.text_widget = text_widget

    def bind(self, text_widget: Text) -> None:
        self.text_widget = text_widget

    def log(self, message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{stamp}] {message}\n"
        print(line, end="")
        if self.text_widget:
            self.text_widget.configure(state="normal")
            self.text_widget.insert(END, line)
            self.text_widget.see(END)
            self.text_widget.configure(state="disabled")
