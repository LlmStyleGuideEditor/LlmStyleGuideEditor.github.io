import GUI
from tkinter import *

if __name__ == '__main__':
    # Set the font
    fontstyle = 'Courier New'

    # Create a root window and set dimensions
    root = Tk()
    root.geometry('1024x768')

    instance = GUI.GUI()
    instance.login_register(root, fontstyle)