"""Module for configuring files"""

import os
from pathlib import Path

from convertatings import VideoConvert as Vc, DocumentConvertor as Dc, \
    ImageConvertor as Ic
from file_formats import IMAGES_FORMATS, VIDEO_FORMATS, DOCUMENT_FORMATS


class ConvertedFile:
    """Class that returns converted file."""

    def __init__(self, file: str, extension: str):
        """
        Args:
            file (str): absolute path to file for converting.
            extension (str): expected extension to convert input file.
        """
        self.file = file
        self.extension = extension
        self.__target_path = self.__set_target_path()
        docs_formatter = Dc(self.file, self.__target_path)
        # initializing dicts for three types of file formats
        self.FUNCTIONS_FOR_VIDEO_FORMATS = {'video':
                                                Vc(self.file,
                                                   self.extension).
                                                    make_video_file_convert}

        self.FUNCTIONS_FOR_IMAGE_FORMATS = \
            {'image': Ic(self.file, self.extension).convert_to_image_format}

        self.FUNCTIONS_FOR_DOCUMENT_FORMATS = {
            '.csv': docs_formatter.convert_to_csv,
            '.docx': docs_formatter.convert_to_docx,
            '.doc': docs_formatter.convert_to_doc,
            '.pdf': docs_formatter.convert_to_pdf,
            '.txt': docs_formatter.convert_to_txt,
        }

    def __set_target_path(self) -> str:
        """Creating target path for input file.
        Returns:
            formed target path.
        """
        original_path = f"{Path(self.file)}"
        target_path = \
            f"{os.path.splitext(original_path)[0]}".split("\\")[-1] \
            + self.extension
        return target_path

    def convert_file(self) -> str:
        """Converts an existing file,
        creating a new copy with another extension if input file
        and extension are valid."""
        # setting original path and target path for our file
        if self.extension in DOCUMENT_FORMATS:
            return self.FUNCTIONS_FOR_DOCUMENT_FORMATS[self.extension]()
        elif self.extension in IMAGES_FORMATS:
            return self.FUNCTIONS_FOR_IMAGE_FORMATS['image']()
        elif self.extension in VIDEO_FORMATS:
            return self.FUNCTIONS_FOR_VIDEO_FORMATS['video']()
        return f"Couldn't convert this file to {self.extension.upper()[1:]} 😥"
