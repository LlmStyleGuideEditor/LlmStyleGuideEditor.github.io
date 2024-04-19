from tkinter import *
from tkinter import filedialog
from pathlib import Path

def promptUser(type, *args):

    files = [("Text Document", "*.txt*")]
    
    # Depending on upload vs download, call different functions
    if type == "Upload":

        filename = filedialog.askopenfilename(initialdir=Path.home() / "Downloads", title="Select a File", filetypes=files)
        return(uploadFile(filename))
        
        
    elif type == "Download":
        
        filename = filedialog.asksaveasfilename(initialdir=Path.home() / "Downloads",initialfile="ste.txt", title="Create a file", filetypes=files, defaultextension=files)
        downloadFile(filename, args[0])      

def downloadFile(fullpath, contents):

    # Write converted text to file
    downloadFile = open(fullpath, 'w')
    downloadFile.write(contents)
    downloadFile.close()

def uploadFile(fullpath):

    # Read text file
    uploadFile = open(fullpath, 'r')
    contents = uploadFile.read()
    uploadFile.close

    return contents
