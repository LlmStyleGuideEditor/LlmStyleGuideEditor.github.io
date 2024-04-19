from tkinter import *
import upload_download
import home
import database
import datetime

translations = []


def history(history_window, fontstyle, current_user):

    # Access global variables
    global translations

    # Set title
    history_window.title("History")

    # Button command functions
    def cmd_back():

        # Forget all widgets
        btn_back.pack_forget()
        lbl_auto_ste.pack_forget()
        for frame in frame_arr:
            frame.pack_forget()
        
        home.home(history_window, fontstyle, current_user)

    def cmd_download(index):

        upload_download.prompt_user("Download", translations[index].out_text)

    # Add widgets
    btn_back = Button(history_window, text="Back", font=(fontstyle, 10), command=cmd_back)
    
    lbl_auto_ste = Label(history_window, text="AutoSTE", font=(fontstyle, 24))

    frame_arr = []
    time_labels_arr = []
    download_buttons_arr = []

    translations = database.get_translations(current_user)
    for i, translation in enumerate(translations):
        frame_arr.append(Frame(history_window))
        time_labels_arr.append(Label(frame_arr[i], text=str(datetime.datetime.fromtimestamp(translation.timestamp)),
                                     font=(fontstyle, 10)))
        download_buttons_arr.append(Button(frame_arr[i], text="Download", font=(fontstyle, 10),
                                           command=lambda idx=i: cmd_download(idx)))
    
    # Configure widget geometry
    btn_back.pack(anchor=W, padx=1, pady=1)
    lbl_auto_ste.pack(pady=40)

    for i in range(len(time_labels_arr)):
        frame_arr[i].pack(pady=10)
        time_labels_arr[i].pack(side='left', padx=20)
        download_buttons_arr[i].pack(side='left', padx=20)

    # Execute
    history_window.mainloop()

 
if __name__ == "__main__":

    # Set the font
    fontstyle_ = 'Courier New'

    # Create a root window and set dimensions
    root = Tk()
    root.geometry('1024x768')

    # Login to default user
    if (user := database.login_user("uid", 'upass')) is None:
        user = database.register_user('uid', 'upass')

    history(root, fontstyle_, user)
