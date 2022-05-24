"""Converting Files to different format"""

import os
from pathlib import Path

import PIL  # type: ignore
from PIL import Image  # type: ignore

import pandas as pd  # type: ignore
import aspose.words as aw  # type: ignore
import imageio.v2 as imageio  # type: ignore


def convert_to_csv(file: str, target_path: str) -> str:
    """Converts to csv"""
    try:
        with open(target_path, "w") as f:
            read_file = pd.read_csv(file, encoding='utf-8')
            read_file.to_csv(target_path, index=None)
            f.seek(0)
        return target_path
    except (UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError):
        os.remove(target_path)
        return "Couldn't convert this file to CSV 😥"


def convert_to_pdf(file: str, output_file: str) -> str:
    """Converting files to PDF"""
    try:
        document = aw.Document(file)
        document.save(output_file, aw.SaveFormat.PDF)
        return output_file
    except RuntimeError:
        return "Couldn't convert this file to PDF 😥"


def convert_to_ico(file: str, extension: str) -> str:
    image = imageio.imread(file)
    imageio.imwrite(file.replace(
        os.path.splitext(f"{Path(file)}")[1], extension), image)
    return os.path.splitext(file)[0] + extension


def convert_to_image_format(file: str, extension: str) -> str:
    """Converting for image formats"""
    try:
        if extension != '.ico':
            image = Image.open(file).convert("RGB")
            image.save(file.replace(
                os.path.splitext(f"{Path(file)}")[1], extension),
                extension.upper()[1:])
            return os.path.splitext(file)[0] + extension
        return convert_to_ico(file, '.ico')
    except PIL.UnidentifiedImageError:
        return f"Couldn't convert this file to {extension.upper()[1:]} 😥"


def convert_to_docx(file: str, output_file: str) -> str:
    """Converts to docx"""
    try:
        document = aw.Document(file)
        document.save(output_file)
        return output_file
    except RuntimeError:
        return "Couldn't convert this file to DOCX 😥"


def convert_to_doc(file: str, output_file: str) -> str:
    """Converts to doc"""
    try:
        document = aw.Document(file)
        document.save(output_file)
        return output_file
    except RuntimeError:
        return "Couldn't convert this file to DOC 😥"


def convert_to_txt(file: str, output_file: str) -> str:
    """Converts to txt"""
    try:
        document = aw.Document(file)
        document.save(output_file)
        return output_file
    except RuntimeError:
        return "Couldn't convert this file to TXT 😥"


class VideoConvert:

    @staticmethod
    def make_video_file_convert(input_file: str, extension: str) -> str:
        """Returns converted video file"""
        command = \
            f'ffmpeg -i "{input_file}" ' \
            f'"{os.path.splitext(input_file)[0] + extension}"'
        os.system(command)
        return os.path.splitext(input_file)[0] + extension

    @staticmethod
    def convert_to_mp3(file: str, extension: str) -> str:
        """Converts to mp3 file format"""
        return VideoConvert.make_video_file_convert(file, extension)

    @staticmethod
    def convert_to_mp4(file: str, extension: str) -> str:
        """Converts to mp4 file format"""
        return VideoConvert.make_video_file_convert(file, extension)
