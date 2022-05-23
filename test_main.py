import os

from tkinter import filedialog
import tkinter as tk
from pathlib import Path

root = tk.Tk()
root.withdraw()

print(os.path.splitext(Path(filedialog.askopenfilename(title="Select a File")))[0] + ".mp4")

root.mainloop()
