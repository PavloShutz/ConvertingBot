"""Converting Files to different format"""

import os
from pathlib import Path
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
    with open(f"{bash_files}{target_path}", "w") as f:
        read_file = pd.read_csv(original_path, encoding='utf-8')
        read_file.to_csv(f"{bash_files}{target_path}")
        f.seek(0)
    return f"{bash_files}{target_path}"


def convert_to_pdf(file: str, output_file: str) -> str:
    """Converting files to PDF"""
    document = aw.Document(file)
    document.save(output_file, aw.SaveFormat.PDF)
    return output_file


def convert_to_image_format(file: str, extension: str) -> str:
    """Converting for image formats"""
    if extension != '.ico':
        image = Image.open(file).convert("RGB")
        image.save(file.replace(
            os.path.splitext(f"{Path(file)}")[1], extension))
        return os.path.splitext(file)[0] + extension
    image = imageio.imread(file)
    imageio.imwrite(file.replace(
        os.path.splitext(f"{Path(file)}")[1], extension), image)
    return os.path.splitext(file)[0] + extension


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
    pass


def convert_to_mp4(input_file: str, output_file: str) -> str:
    """Converts to mp4 file format"""
    pass
