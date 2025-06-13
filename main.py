from tkinter import Tk
from gui import PDFFormOCR


def main():
    root = Tk()
    app = PDFFormOCR(root)
    root.mainloop()


if __name__ == "__main__":
    main()
