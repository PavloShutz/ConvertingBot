"""Converting Files to different format"""

import os
from pathlib import Path

import PIL  # type: ignore
from PIL import Image  # type: ignore

import pandas as pd  # type: ignore
import aspose.words as aw  # type: ignore
import imageio.v2 as imageio  # type: ignore


def convert_to_csv(file: str) -> str:
    """Converts to csv"""
    bash_files = '\\'.join(os.getcwd().split("\\"))
    original_path = f"{Path(file)}"
    target_path = \
        f"{os.path.splitext(original_path)[0]}".split("\\")[-1] + '.csv'
    try:
        with open(f"{bash_files}{target_path}", "w") as f:
            read_file = pd.read_csv(original_path, encoding='utf-8')
            read_file.to_csv(f"{bash_files}{target_path}")
            f.seek(0)
        return f"{bash_files}{target_path}"
    except UnicodeDecodeError:
        os.remove(f"{bash_files}{target_path}")
        return "Couldn't convert this file to CSV 😥"


def convert_to_pdf(file: str, output_file: str) -> str:
    """Converting files to PDF"""
    try:
        document = aw.Document(file)
        document.save(output_file, aw.SaveFormat.PDF)
        return output_file
    except RuntimeError:
        return "Couldn't convert this file to PDF 😥"


def convert_to_image_format(file: str, extension: str) -> str:
    """Converting for image formats"""
    try:
        if extension != '.ico':
            image = Image.open(file).convert("RGB")
            image.save(file.replace(
                os.path.splitext(f"{Path(file)}")[1], extension),
                extension.upper()[1:])
            return os.path.splitext(file)[0] + extension
        image = imageio.imread(file)
        imageio.imwrite(file.replace(
            os.path.splitext(f"{Path(file)}")[1], extension), image)
        return os.path.splitext(file)[0] + extension
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


def convert_to_mp3(file: str) -> str:
    """Converts to mp3 file format"""
    new_file = os.path.dirname(os.path.realpath(file)) + '\\' + ''.join(
        [i for i in os.path.basename(file).split()])
    os.rename(file, new_file)
    os.system(f'ffmpeg -i {new_file} {os.path.splitext(new_file)[0] + ".mp3"}')
    return os.path.splitext(new_file)[0] + ".mp3"


def convert_to_mp4(input_file: str) -> str:
    """Converts to mp4 file format"""
    new_file = os.path.dirname(os.path.realpath(input_file)) + '\\' + ''.join(
        [i for i in os.path.basename(input_file).split()])
    os.rename(input_file, new_file)
    command = f'ffmpeg -i {new_file} -crf 23 ' \
        f'{os.path.splitext(new_file)[0] + ".mp4"}'
    os.system(command)
    return os.path.splitext(new_file)[0] + ".mp4"
