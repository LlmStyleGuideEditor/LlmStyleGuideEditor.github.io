import re
from tkinter import *
from Home import home
from database import *


def LoginRegister(loginWindow, fontstyle):

    # Set title
    loginWindow.title("Login")
    
    # Utility functions
    def forgetWidgets():

        lblAutoSTE.pack_forget()
        lblLogin.pack_forget()
        entUser.pack_forget()
        entPass.pack_forget()
        frame1.pack_forget()
        errEmpty.pack_forget()
        errLogin.pack_forget()
        errRegister.pack_forget()

    def forgetErrors():

        errLogin.pack_forget()
        errRegister.pack_forget()
        errEmpty.pack_forget()
        errSpace.pack_forget()

    # Button command functions
    # TODO: Authenticate user with database, currently programmed for demo
    def cmdLogin():

        id = entUser.get()
        password = entPass.get()

        forgetErrors()

        currentUser = login_user(id, password)

        if currentUser is None:
            errLogin.pack(pady=5)
            return

        forgetWidgets()
        home(loginWindow, fontstyle)

    def cmdRegister():
        
        id = entUser.get()
        password = entPass.get()

        forgetErrors()

        currentUser = register_user(id, password)

        if currentUser is None:
            errRegister.pack(pady=5)
            return

        forgetWidgets()
        home(loginWindow, fontstyle)

    # Add widgets
    frame1 = Frame(loginWindow)

    lblAutoSTE = Label(loginWindow, text="AutoSTE", font=(fontstyle, 24))
    lblLogin = Label(loginWindow, text="Please enter your UserID and Password", font=(fontstyle, 12))

    entUser = Entry(loginWindow, font=(fontstyle, 14), width = 20)
    entPass = Entry(loginWindow, font=(fontstyle, 14), width = 20, show = '*')

    btnLogin = Button(frame1, text="Login", font=(fontstyle, 12), width = 10, command=cmdLogin)
    btnRegister = Button(frame1, text="Register", font=(fontstyle, 12), width = 10, command=cmdRegister)

    errLogin = Label(loginWindow, text="Invalid login details", font=(fontstyle, 10), foreground='red')
    errRegister = Label(loginWindow, text="User ID already in use", font=(fontstyle, 10), foreground='red')
    errEmpty = Label(loginWindow, text="Entries must be populated", font=(fontstyle, 10), foreground='red')
    errSpace = Label(loginWindow, text="User ID and Password can not contain whitespaces", font=(fontstyle, 10), foreground='red')

    # Configure widget geometry
    lblAutoSTE.pack(pady=70)
    lblLogin.pack(pady=(90, 5))
    entUser.pack(pady=5)
    entPass.pack(pady=5)

    frame1.pack(pady=5)
    btnLogin.pack(side='left')
    btnRegister.pack(side='left')
    
    # Execute
    loginWindow.mainloop()


if __name__ == "__main__":

    # Set the font
    fontstyle = 'Courier New'

    # Create a root window and set dimensions
    root = Tk()
    root.geometry('1024x768')

    LoginRegister(root, fontstyle)
