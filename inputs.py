import tkinter as tk

class InputDialog(tk.Toplevel):
    """Spawns a dialog to get user input"""
    def __init__(self, parent, message):
        super().__init__(parent)

        self.title(message)
        self.geometry("300x150")
        self.entry = tk.Entry(self, width=30)
        self.entry.pack(pady=20)

        self.entry.focus_set()
        self.entry.bind("<Return>", self._on_save)

        self.grab_set()
        self.entry.focus_set()

        self.result = None

    def _on_save(self, event):
        self.result = self.entry.get()
        self.destroy()
