import os
import json
import csv
from tkinter import (
    Tk,
    Canvas,
    Button,
    filedialog,
    simpledialog,
    Toplevel,
    Label,
    Entry,
    messagebox,
    Spinbox,
)
from PIL import Image, ImageTk
from ocr_utils import convert_page
import pytesseract


class PDFFormOCR:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Form OCR")
        self.canvas = Canvas(root, width=800, height=600, bg="gray")
        self.canvas.pack(expand=True, fill="both")

        self.open_btn = Button(root, text="Open PDF", command=self.open_pdf)
        self.open_btn.pack(side="left")
        self.page_spin = Spinbox(root, from_=1, to=9999, width=5)
        self.page_spin.pack(side="left")
        self.setup_btn = Button(root, text="Setup Fields", command=self.setup_fields)
        self.setup_btn.pack(side="left")
        self.extract_btn = Button(root, text="Extract Data", command=self.extract_data)
        self.extract_btn.pack(side="left")

        self.pdf_path = None
        self.image = None
        self.photo = None
        self.fields = []
        self.rect = None
        self.start_x = self.start_y = 0

    # Utility methods
    def load_mapping(self):
        if not self.pdf_path:
            return
        mapping_path = self.pdf_path + ".fields.json"
        if os.path.exists(mapping_path):
            with open(mapping_path, "r") as f:
                self.fields = json.load(f)
        else:
            self.fields = []

    def save_mapping(self):
        if not self.pdf_path:
            return
        mapping_path = self.pdf_path + ".fields.json"
        with open(mapping_path, "w") as f:
            json.dump(self.fields, f, indent=2)

    # GUI actions
    def open_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        self.pdf_path = path
        try:
            page = int(self.page_spin.get())
        except Exception:
            page = 1
            self.page_spin.delete(0, "end")
            self.page_spin.insert(0, "1")

        img = convert_page(path, page)
        if img:
            self.image = img
            self.display_image()
        self.load_mapping()

    def display_image(self):
        if not self.image:
            return
        img = self.image.copy()
        img.thumbnail((800, 600))
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

    def setup_fields(self):
        if not self.image:
            messagebox.showinfo("Info", "Open a PDF first")
            return
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        messagebox.showinfo("Setup", "Draw rectangles over each field")

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        name = simpledialog.askstring("Field Name", "Enter name for this field:")
        if name:
            self.fields.append({"name": name, "bbox": [x1, y1, x2, y2]})
            self.save_mapping()
        self.rect = None

    def extract_data(self):
        if not self.image:
            messagebox.showinfo("Info", "Open a PDF first")
            return
        if not self.fields:
            messagebox.showinfo("Info", "No field mapping found. Use Setup Fields first.")
            return
        results = {}
        for field in self.fields:
            x1, y1, x2, y2 = field["bbox"]
            cropped = self.image.crop((x1, y1, x2, y2))
            text = pytesseract.image_to_string(cropped).strip()
            results[field["name"]] = text
        self.show_results(results)

    def show_results(self, data):
        win = Toplevel(self.root)
        entries = {}
        row = 0
        for name, value in data.items():
            Label(win, text=name).grid(row=row, column=0, sticky="e")
            e = Entry(win, width=40)
            e.grid(row=row, column=1)
            e.insert(0, value)
            entries[name] = e
            row += 1
        def save():
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
            if not save_path:
                return
            with open(save_path, "w", newline="") as f:
                writer = csv.writer(f)
                for name, entry in entries.items():
                    writer.writerow([name, entry.get()])
            messagebox.showinfo("Saved", f"Data saved to {save_path}")
        Button(win, text="Save CSV", command=save).grid(row=row, column=0, columnspan=2)


def main():
    root = Tk()
    app = PDFFormOCR(root)
    root.mainloop()


if __name__ == "__main__":
    main()
