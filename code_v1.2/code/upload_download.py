from tkinter import filedialog
from pathlib import Path


def prompt_user(operation, download_text=None):

    files = [("Text Document", "*.txt*")]
    
    # Depending on upload vs download, call different functions
    if operation == "Upload":

        filename = filedialog.askopenfilename(initialdir=Path.home() / "Downloads",
                                              title="Select a File", filetypes=files)
        return upload_file(filename)

    elif operation == "Download":
        
        filename = filedialog.asksaveasfilename(initialdir=Path.home() / "Downloads", initialfile="ste.txt",
                                                title="Create a file", filetypes=files)
        download_file(filename, download_text)


def download_file(fullpath, contents):

    # Write converted text to file
    file = open(fullpath, 'w')
    file.write(contents)
    file.close()


def upload_file(fullpath):

    # Read text file
    file = open(fullpath, 'r')
    contents = file.read()
    file.close()

    return contents
