from tkinter import *
from Home import home
from database import *


def login_register(login_window, fontstyle):

    # Set title
    login_window.title("Login")
    
    # Utility functions
    def forget_widgets():

        lbl_auto_ste.pack_forget()
        lbl_login.pack_forget()
        ent_user.pack_forget()
        ent_pass.pack_forget()
        frame1.pack_forget()
        err_login.pack_forget()
        err_register.pack_forget()

    def forget_errors():

        err_login.pack_forget()
        err_register.pack_forget()

    # Button command functions
    def cmd_login():

        username = ent_user.get()
        password = ent_pass.get()

        forget_errors()

        current_user = login_user(username, password)

        if current_user is None:
            err_login.pack(pady=5)
            return

        forget_widgets()
        home(login_window, fontstyle, current_user)

    def cmd_register():
        
        username = ent_user.get()
        password = ent_pass.get()

        forget_errors()

        current_user = register_user(username, password)

        if current_user is None:
            err_register.pack(pady=5)
            return

        forget_widgets()
        home(login_window, fontstyle, current_user)

    # Add widgets
    frame1 = Frame(login_window)

    lbl_auto_ste = Label(login_window, text="AutoSTE", font=(fontstyle, 24))
    lbl_login = Label(login_window, text="Please enter your UserID and Password", font=(fontstyle, 12))

    ent_user = Entry(login_window, font=(fontstyle, 14), width=20)
    ent_pass = Entry(login_window, font=(fontstyle, 14), width=20, show='*')

    btn_login = Button(frame1, text="Login", font=(fontstyle, 12), width=10, command=cmd_login)
    btn_register = Button(frame1, text="Register", font=(fontstyle, 12), width=10, command=cmd_register)

    err_login = Label(login_window, text="Invalid login details", font=(fontstyle, 10), foreground='red')
    err_register = Label(login_window, text="User ID already in use", font=(fontstyle, 10), foreground='red')

    # Configure widget geometry
    lbl_auto_ste.pack(pady=70)
    lbl_login.pack(pady=(90, 5))
    ent_user.pack(pady=5)
    ent_pass.pack(pady=5)

    frame1.pack(pady=5)
    btn_login.pack(side='left')
    btn_register.pack(side='left')
    
    # Execute
    login_window.mainloop()


if __name__ == "__main__":

    # Set the font
    fontstyle = 'Courier New'

    # Create a root window and set dimensions
    root = Tk()
    root.geometry('1024x768')

    login_register(root, fontstyle)
