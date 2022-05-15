"""Module for configuring files"""

import os
from pathlib import Path
import shutil


# creates a copy of a file, then return new file's path
def convert_file(file, extension):
    """
    Converts an existing file,
    creating a new copy with another extension.
    """

    bash_files = '\\'.join(os.getcwd().split("\\"))
    original_path = f"{Path(file)}"
    target_path = f"{os.path.splitext(original_path)[0]}".split("\\")[-1] + extension
    with open(f"{bash_files}{target_path}", "w") as f:
        shutil.copyfile(original_path, f"{bash_files}{target_path}")
        f.seek(0)
    return f"{bash_files}{target_path}"
