"""Converting Files to different formats"""

import os
from pathlib import Path

import PIL  # type: ignore
from PIL import Image  # type: ignore
import pandas as pd  # type: ignore
import aspose.words as aw  # type: ignore


class DocumentConvertor:
    """Class implementing document files converting."""

    def __init__(self, file: str, output_file: str):
        """
        Args:
            file (str): absolute path to file for converting.
            output_file (str): expected output_file after converting.
        """
        self.file = file
        self.output_file = output_file

    def convert_to_csv(self) -> str:
        """Converts to csv.
        Returns:
            valid csv file if input file format is valid.
        """
        try:
            with open(self.output_file, "w") as f:
                read_file = pd.read_csv(self.file, encoding='utf-8')
                read_file.to_csv(self.output_file, index=None)
                f.seek(0)
            return self.output_file
        except (UnicodeDecodeError, FileNotFoundError,
                pd.errors.ParserError, pd.errors.EmptyDataError):
            os.remove(self.output_file)
            return "Couldn't convert this file to CSV 😥"

    def convert_to_pdf(self) -> str:
        """Converting files to pdf.
        Returns:
            valid pdf file if input file format is valid.
        """
        try:
            document = aw.Document(self.file)
            document.save(self.output_file, aw.SaveFormat.PDF)
            return self.output_file
        except RuntimeError:
            return "Couldn't convert this file to PDF 😥"

    def convert_to_docx(self) -> str:
        """Converts to docx.
        Returns:
            valid docx file if input file format is valid.
        """
        try:
            document = aw.Document(self.file)
            document.save(self.output_file)
            return self.output_file
        except RuntimeError:
            return "Couldn't convert this file to DOCX 😥"

    def convert_to_doc(self) -> str:
        """Converts to doc.
        Returns:
            valid doc file if input file format is valid.
        """
        try:
            document = aw.Document(self.file)
            document.save(self.output_file)
            return self.output_file
        except RuntimeError:
            return "Couldn't convert this file to DOC 😥"

    def convert_to_txt(self) -> str:
        """Converts to txt.
        Returns:
            valid txt file if input file format is valid.
        """
        try:
            document = aw.Document(self.file)
            document.save(self.output_file)
            return self.output_file
        except RuntimeError:
            return "Couldn't convert this file to TXT 😥"


class ImageConvertor:
    """Class implementing image files converting."""

    def __init__(self, file: str, extension: str):
        """
        Args:
            file (str): absolute path to file for converting.
            extension (str): expected extension to convert input file.
        """
        self.file = file
        self.extension = extension

    def __convert_to_ico(self) -> str:
        """
        Returns:
            converted image with '.ico' format is input file format is valid.
        """
        try:
            image = Image.open(self.file)
            image.save(os.path.splitext(self.file)[0] + self.extension,
                       format='ICO', sizes=[(255, 255)])
            return os.path.splitext(self.file)[0] + self.extension
        except FileNotFoundError:
            return "Couldn't convert this file to ICO 😥"

    def __convert_to_jpg(self) -> str:
        """
        Returns:
            converted image with '.jpg' format is input file format is valid.
        """
        try:
            image = Image.open(self.file)
            rgb_image = image.convert("RGB")
            rgb_image.save(os.path.splitext(self.file)[0] + self.extension)
            return os.path.splitext(self.file)[0] + self.extension
        except (FileNotFoundError, AttributeError):
            return "Couldn't convert this file to JPG 😥"

    def convert_to_image_format(self) -> str:
        """Converting for image formats.
        Returns:
            converted image file if input file format is valid.
        """
        try:
            if self.extension not in ('.ico', '.jpg'):
                image = Image.open(self.file).convert("RGB")
                image.save(self.file.replace(
                    os.path.splitext(f"{Path(self.file)}")[1], self.extension),
                    self.extension.upper()[1:])
                return os.path.splitext(self.file)[0] + self.extension
            else:
                if self.extension == '.ico':
                    return self.__convert_to_ico()
                return self.__convert_to_jpg()
        except PIL.UnidentifiedImageError:
            return "Couldn't convert this " \
                   f"file to {self.extension.upper()[1:]} 😥"


class VideoConvert:
    """Class implementing video files converting."""

    def __init__(self, file: str, extension: str):
        """
        Args:
            file (str): absolute path to file for converting.
            extension (str): expected extension to convert input file.
        """
        self.file = file
        self.extension = extension
        self.command = f'ffmpeg -i "{self.file}" ' \
                       f'"{os.path.splitext(self.file)[0] + self.extension}"'

    def make_video_file_convert(self) -> str:
        """
        Returns:
            converted video file.
        """
        os.system(self.command)
        return os.path.splitext(self.file)[0] + self.extension
