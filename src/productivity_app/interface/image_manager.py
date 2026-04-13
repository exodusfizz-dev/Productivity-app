
from typing import Protocol
import tkinter as tk


class ImageManager(Protocol):
    """Protocol for managing images in the UI."""
    def get_image(self, name: str) -> "tk.PhotoImage | None":
        ...
    # TODO: is the protocol necessary? maybe just a simple class is fine for now, since we only have one implementation. can always refactor later if needed.

class TkinterImageManager(ImageManager):
    """Manages loading and caching of images for tkinter UI."""
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.images = {}

    def get_image(self, name: str) -> "tk.PhotoImage | None":
        if name in self.images:
            return self.images[name]

        try:
            image_path = f"{self.image_dir}/{name}.png"
            image = tk.PhotoImage(file=image_path)
            self.images[name] = image
            return image
        except tk.TclError as e:
            print(f"[ImageManager] Warning: could not load image '{name}': {e}")
            return None
