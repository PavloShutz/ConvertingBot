"""Module for configuring files"""

import os
from pathlib import Path

from convertatings import convert_to_mp4, convert_to_pdf, \
    convert_to_image_format, convert_to_docx, \
    convert_to_csv, convert_to_txt, convert_to_mp3, \
    convert_to_doc
from file_formats import IMAGES_FORMATS, VIDEO_FORMATS, DOCUMENT_FORMATS


# creates a copy of a file, then return new file's path
def convert_file(file: str, extension: str) -> str:
    """
    Converts an existing file,
    creating a new copy with another extension.
    """
    original_path = f"{Path(file)}"
    target_path = \
        f"{os.path.splitext(original_path)[0]}".split("\\")[-1] + extension
    if extension == '.csv':
        return convert_to_csv(file)
    elif extension in IMAGES_FORMATS:
        return convert_to_image_format(file, extension)
    elif extension in VIDEO_FORMATS:
        if extension == '.mp3':
            return convert_to_mp3(file)
        elif extension == '.mp4':
            return convert_to_mp4(file)
    elif extension in DOCUMENT_FORMATS:
        if extension == '.docx':
            return convert_to_docx(file, target_path)
        elif extension == '.txt':
            return convert_to_txt(file, target_path)
        elif extension == '.pdf':
            return convert_to_pdf(file, target_path)
        elif extension == '.doc':
            return convert_to_doc(file, target_path)
    return f"Couldn't convert this file to {extension.upper()[1:]} 😥"
