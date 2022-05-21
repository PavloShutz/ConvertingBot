from tkinter import filedialog
import tkinter as tk
from pathlib import Path

root = tk.Tk()
root.withdraw()

print(Path(filedialog.askopenfilename(title="Select a File")))

root.mainloop()
