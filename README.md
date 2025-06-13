# PDFFormOCR

A simple Python tool with a graphical user interface to extract text from PDF forms using free OCR tools.

## Features

- Convert PDF pages to images using `pdf2image`.
- Perform OCR using open-source Tesseract.
- Setup mode allows manually defining form fields by drawing rectangles on the PDF page.
- Extract text from defined fields and edit the values before saving.
- Export results to CSV.

## Requirements

- Python 3
- Tesseract OCR installed and available in the system path.
- Python packages listed in `requirements.txt`.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

1. Use **Open PDF** to select a file.
2. Choose **Setup Fields** the first time you process a form. Draw rectangles over each field and provide a name. The field layout is saved for future runs.
3. Select **Extract Data** to OCR the fields and edit the extracted values.
4. Export the data to CSV when finished.
