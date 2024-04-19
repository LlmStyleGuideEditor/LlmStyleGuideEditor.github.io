from tkinter import *
from datetime import datetime
import UploadDownload
import History
import database


def home(home_window, fontstyle, current_user):

    # Set title
    home_window.title("Home")

    # Utility functions
    def retrieve_pre_text():
        txt = txt_pre.get("1.0", "end-1c")
        return txt
    
    def retrieve_post_text():
        txt = txt_post.get("1.0", "end-1c")
        return txt

    # Button command functions
    def cmd_history():
    
        # Forget all widgets
        frame0.pack_forget()
        lbl_auto_ste.pack_forget()
        frame1.pack_forget()
        frame2.pack_forget()

        History.history(home_window, fontstyle, current_user)
    
    def cmd_convert():

        str_pre = retrieve_pre_text()

        # TODO Kick strPre to LLM here

        txt_post.configure(state=NORMAL)
        txt_post.delete("1.0", "end")
        txt_post.insert("1.0", str_pre)
        txt_post.configure(state=DISABLED)

        str_post = retrieve_post_text()

        database.add_translation(current_user, str_pre, str_post)

    def cmd_upload():
        
        str_upload = UploadDownload.prompt_user("Upload")
        txt_pre.delete("1.0", "end")
        txt_pre.insert("1.0", str_upload)
    
    def cmd_download():

        UploadDownload.prompt_user("Download", retrieve_post_text())

    # Add widgets
    frame0 = Frame(home_window)
    frame1 = Frame(home_window)
    frame2 = Frame(home_window)

    btn_history = Button(frame0, text="Conversion History", font=(fontstyle, 10), command=cmd_history)

    lbl_auto_ste = Label(home_window, text="AutoSTE", font=(fontstyle, 24))

    txt_pre = Text(frame1, width=36, height=25, font=(fontstyle, 10))
    txt_post = Text(frame1, width=36, height=25, font=(fontstyle, 10), state=DISABLED)
    scr_pre = Scrollbar(frame1, command=txt_pre.yview)
    scr_post = Scrollbar(frame1, command=txt_post.yview)

    btn_convert = Button(frame2, width=17, height=2, text="Convert", font=(fontstyle, 10), command=cmd_convert)
    btn_upload = Button(frame2, width=17, height=2, text="Upload", font=(fontstyle, 10), command=cmd_upload)
    btn_download = Button(frame2, width=36, height=2, text="Download", font=(fontstyle, 10), command=cmd_download)

    # Set yscrollcommand to scroll bars
    txt_pre.configure(yscrollcommand=scr_pre.set)
    txt_post.configure(yscrollcommand=scr_post.set)

    # Configure widget geometry
    frame0.pack(anchor=E)
    btn_history.pack(side='right', padx=1, pady=1)

    lbl_auto_ste.pack(pady=40)

    frame1.pack(pady=(0, 1))
    txt_pre.pack(side='left')
    scr_pre.pack(side='left', fill='y', padx=(0, 50))
    txt_post.pack(side='left', padx=(50, 0))
    scr_post.pack(side='left', fill='y')

    frame2.pack()
    btn_convert.pack(side='left', padx=(35, 0), pady=1)
    btn_upload.pack(side='left', padx=(0, 65), pady=1)
    btn_download.pack(side='left', padx=50, pady=1)

    # Execute
    home_window.mainloop()


if __name__ == "__main__":

    # Set the font
    fontstyle = 'Courier New'

    # Create a root window and set dimensions
    root = Tk()
    root.geometry('1024x768')

    # Login to default user
    if (user := database.login_user("uid", 'upass')) is None:
        user = database.register_user('uid', 'upass')

    home(root, fontstyle, user)
