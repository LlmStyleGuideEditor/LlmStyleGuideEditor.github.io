from tkinter import *
from database import *
import upload_download
import translator
import database
import datetime


class GUI:

    translations = []

    def login_register(self, login_window, fontstyle):

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
            self.home(login_window, fontstyle, current_user)

        def cmd_register():
            
            username = ent_user.get()
            password = ent_pass.get()

            forget_errors()

            current_user = register_user(username, password)

            if current_user is None:
                err_register.pack(pady=5)
                return

            forget_widgets()
            self.home(login_window, fontstyle, current_user)

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


    def home(self, home_window, fontstyle, current_user):

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

            self.history(home_window, fontstyle, current_user)
        
        def cmd_convert():

            str_pre = retrieve_pre_text()

            str_post = translator.translate(str_pre)
            # Failsafe: just copy
            #str_post = str_pre

            txt_post.configure(state=NORMAL)
            txt_post.delete("1.0", "end")
            txt_post.insert("1.0", str_post)
            txt_post.configure(state=DISABLED)

            database.add_translation(current_user, str_pre, str_post)

        def cmd_upload():
            
            str_upload = upload_download.prompt_user("Upload")
            txt_pre.delete("1.0", "end")
            txt_pre.insert("1.0", str_upload)
        
        def cmd_download():

            upload_download.prompt_user("Download", retrieve_post_text())

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

    def history(self, history_window, fontstyle, current_user):

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
            
            self.home(history_window, fontstyle, current_user)

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
