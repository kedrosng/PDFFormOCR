from pdf2image import convert_from_path
from typing import Optional
from PIL import Image


def convert_page(path: str, page: int = 1) -> Optional[Image.Image]:
    """Convert a specific page of a PDF to a PIL Image.

    Parameters
    ----------
    path : str
        Path to the PDF file.
    page : int, optional
        Page number to convert, starting from 1.

    Returns
    -------
    PIL.Image or None
        The converted page image, or None if conversion failed.
    """
    if page < 1:
        raise ValueError("page must be >= 1")
    images = convert_from_path(path, first_page=page, last_page=page)
    return images[0] if images else None
