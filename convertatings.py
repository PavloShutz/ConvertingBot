"""Converting Files to different format"""

import os
from pathlib import Path

import PIL  # type: ignore
from PIL import Image  # type: ignore
import pandas as pd  # type: ignore
import aspose.words as aw  # type: ignore


class DocumentConvertor:

    def __init__(self, file: str, output_file: str):
        self.file = file
        self.output_file = output_file

    def convert_to_csv(self) -> str:
        """Converts to csv"""
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
        """Converting files to PDF"""
        try:
            document = aw.Document(self.file)
            document.save(self.output_file, aw.SaveFormat.PDF)
            return self.output_file
        except RuntimeError:
            return "Couldn't convert this file to PDF 😥"

    def convert_to_docx(self) -> str:
        """Converts to docx"""
        try:
            document = aw.Document(self.file)
            document.save(self.output_file)
            return self.output_file
        except RuntimeError:
            return "Couldn't convert this file to DOCX 😥"

    def convert_to_doc(self) -> str:
        """Converts to doc"""
        try:
            document = aw.Document(self.file)
            document.save(self.output_file)
            return self.output_file
        except RuntimeError:
            return "Couldn't convert this file to DOC 😥"

    def convert_to_txt(self) -> str:
        """Converts to txt"""
        try:
            document = aw.Document(self.file)
            document.save(self.output_file)
            return self.output_file
        except RuntimeError:
            return "Couldn't convert this file to TXT 😥"


class ImageConvertor:

    def __init__(self, file: str, extension: str):
        self.file = file
        self.extension = extension

    def __convert_to_ico(self) -> str:
        try:
            image = Image.open(self.file)
            image.save(os.path.splitext(self.file)[0] + self.extension,
                       format='ICO', sizes=[(255, 255)])
            return os.path.splitext(self.file)[0] + self.extension
        except FileNotFoundError:
            return "Couldn't convert this file to ICO 😥"

    def __convert_to_jpg(self) -> str:
        try:
            image = Image.open(self.file)
            rgb_image = image.convert("RGB")
            rgb_image.save(os.path.splitext(self.file)[0] + self.extension)
            return os.path.splitext(self.file)[0] + self.extension
        except (FileNotFoundError, AttributeError):
            return "Couldn't convert this file to JPG 😥"

    def convert_to_image_format(self) -> str:
        """Converting for image formats"""
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
            return f"Couldn't convert this file to {self.extension.upper()[1:]} 😥"


class VideoConvert:

    def __init__(self, file: str, extension: str):
        self.file = file
        self.extension = extension
        self.command = f'ffmpeg -i "{self.file}" ' \
                       f'"{os.path.splitext(self.file)[0] + self.extension}"'

    def make_video_file_convert(self) -> str:
        """Returns converted video file"""
        os.system(self.command)
        return os.path.splitext(self.file)[0] + self.extension
