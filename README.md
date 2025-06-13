# PDF Form OCR

This project provides a small Tkinter GUI application to extract text from PDF forms using open source tools.

## Features

- Convert PDF pages to images using `pdf2image` and `poppler`.
- OCR images with Tesseract via `pytesseract` (supports printed and handwritten text).
- Setup mode to manually define form fields by drawing bounding boxes.
- Extract data for each field and edit before saving.

## Requirements

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and available on your PATH.
- `poppler` utilities for PDF rendering (required by `pdf2image`).
- Python packages from `requirements.txt`.

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m pdf_form_ocr
```

1. **Open PDF**: choose the PDF form you want to process.
2. **Setup Form**: draw rectangles around each field and provide a field name. The layout is saved in `form_layout.json`.
3. **Extract Data**: OCR runs on the defined fields and shows editable entries.
4. **Save Data**: export the field data to a JSON file.

The output format can be adjusted later by modifying the `save_data` function in `gui.py`.
