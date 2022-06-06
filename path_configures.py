"""Module for configuring files"""

import os
from pathlib import Path

from convertatings import VideoConvert as Vc, convert_to_pdf, \
    convert_to_image_format, convert_to_docx, \
    convert_to_csv, convert_to_txt, \
    convert_to_doc
from file_formats import IMAGES_FORMATS, VIDEO_FORMATS, DOCUMENT_FORMATS


# initializing dicts for three types of file formats
FUNCTIONS_FOR_VIDEO_FORMATS = {'.mp4': Vc.convert_to_mp4,
                               '.mp3': Vc.convert_to_mp3, }

FUNCTIONS_FOR_IMAGE_FORMATS = {'image': convert_to_image_format, }

FUNCTIONS_FOR_DOCUMENT_FORMATS = {'.csv': convert_to_csv,
                                  'docx': convert_to_docx,
                                  '.doc': convert_to_doc,
                                  '.pdf': convert_to_pdf,
                                  '.txt': convert_to_txt, }


def _set_target_path(file: str, extension: str) -> str:
    original_path = f"{Path(file)}"
    target_path = \
        f"{os.path.splitext(original_path)[0]}".split("\\")[-1] + extension
    return target_path


def convert_file(file: str, extension: str) -> str:
    """
    Converts an existing file,
    creating a new copy with another extension if input file
    and extension are valid.
    """
    # setting original path and target path for our file
    target_path = _set_target_path(file, extension)
    if extension in DOCUMENT_FORMATS:
        return FUNCTIONS_FOR_DOCUMENT_FORMATS[extension](file, target_path)
    elif extension in IMAGES_FORMATS:
        return FUNCTIONS_FOR_IMAGE_FORMATS['image'](file, extension)
    elif extension in VIDEO_FORMATS:
        return FUNCTIONS_FOR_VIDEO_FORMATS[extension](file, extension)
    return f"Couldn't convert this file to {extension.upper()[1:]} 😥"
