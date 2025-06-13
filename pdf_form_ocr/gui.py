from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

from .ocr import pdf_to_images, ocr_image
from .form import FormLayout


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PDF Form OCR")
        self.geometry("800x600")

        self.pdf_path: Path | None = None
        self.images: list[Image.Image] = []
        self.layout = FormLayout.load("form_layout.json")
        self.field_entries: Dict[str, tk.Entry] = {}

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Open PDF", command=self.open_pdf)
        file_menu.add_command(label="Setup Form", command=self.setup_form)
        file_menu.add_command(label="Extract Data", command=self.extract_data)
        file_menu.add_command(label="Save Data", command=self.save_data)
        self.menu.add_cascade(label="File", menu=file_menu)

        self._image_on_canvas = None
        self._setup_mode = False
        self._start_x = self._start_y = 0

    def open_pdf(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        self.pdf_path = Path(path)
        self.images = pdf_to_images(path)
        if not self.images:
            messagebox.showerror("Error", "Failed to load PDF")
            return
        self.show_page(0)

    # Display first page on canvas
    def show_page(self, index: int) -> None:
        if index >= len(self.images):
            return
        img = self.images[index]
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self._image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def setup_form(self) -> None:
        if not self.images:
            messagebox.showinfo("Info", "Load a PDF first")
            return
        self._setup_mode = True
        self.canvas.bind("<Button-1>", self._on_setup_start)
        self.canvas.bind("<ButtonRelease-1>", self._on_setup_end)
        messagebox.showinfo("Setup", "Drag to draw field, you'll be prompted for a name")

    def _on_setup_start(self, event: tk.Event) -> None:
        if not self._setup_mode:
            return
        self._start_x = event.x
        self._start_y = event.y

    def _on_setup_end(self, event: tk.Event) -> None:
        if not self._setup_mode:
            return
        x1, y1 = self._start_x, self._start_y
        x2, y2 = event.x, event.y
        name = simpledialog.askstring("Field", "Field name:")
        if name:
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")
            self.layout.mapping[name] = (x1, y1, x2, y2)
        self.layout.save("form_layout.json")

    def extract_data(self) -> None:
        if not self.images:
            messagebox.showinfo("Info", "Load a PDF first")
            return
        if not self.layout.mapping:
            messagebox.showinfo("Info", "Setup form fields first")
            return
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self._setup_mode = False

        page = self.images[0]
        for widget in self.field_entries.values():
            widget.destroy()
        self.field_entries = {}

        for name, box in self.layout.mapping.items():
            region = page.crop(box)
            text = ocr_image(region)
            entry = tk.Entry(self)
            entry.insert(0, text.strip())
            self.field_entries[name] = entry
            self.canvas.create_window(box[0], box[1], anchor="nw", window=entry)

    def save_data(self) -> None:
        if not self.field_entries:
            return
        data = {name: entry.get() for name, entry in self.field_entries.items()}
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        Path(path).write_text(json.dumps(data, indent=2))
        messagebox.showinfo("Saved", f"Data saved to {path}")


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
