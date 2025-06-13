from __future__ import annotations

import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def pdf_to_images(pdf_path: str) -> list[Image.Image]:
    """Convert a PDF to a list of PIL images."""
    images = convert_from_path(pdf_path)
    return images


def ocr_image(image: Image.Image) -> str:
    """Extract text from a PIL image using Tesseract."""
    return pytesseract.image_to_string(image)


def ocr_pdf(pdf_path: str) -> list[str]:
    """Extract text from each page of a PDF."""
    images = pdf_to_images(pdf_path)
    texts = [ocr_image(img) for img in images]
    return texts
