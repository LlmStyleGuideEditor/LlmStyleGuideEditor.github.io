from tkinter import *
from datetime import datetime
import UploadDownload
import History


def home(homeWindow, fontstyle):

    # Set title
    homeWindow.title("Home")

    # Utility functions
    def retrievePreText():
        txt = txtPre.get("1.0", "end-1c")
        return txt
    
    def retrievePostText():
        txt = txtPost.get("1.0", "end-1c")
        return txt

    # Button command functions
    def cmdHistory():
    
        # Forget all widgets
        frame0.pack_forget()
        lblAutoSTE.pack_forget()
        frame1.pack_forget()
        frame2.pack_forget()

        History.history(homeWindow, fontstyle)
    
    def cmdConvert():

        time = datetime.now()
        strPre = retrievePreText()

        # Kick strPre to LLM here

        txtPost.configure(state=NORMAL)
        txtPost.delete("1.0", "end")
        txtPost.insert("1.0", strPre)
        txtPost.configure(state=DISABLED)

        strPost = retrievePostText()

        History.addConversion(time, strPost)

    def cmdUpload():
        
        strUpload = UploadDownload.promptUser("Upload")
        txtPre.delete("1.0", "end")
        txtPre.insert("1.0", strUpload)
    
    def cmdDownload():

        UploadDownload.promptUser("Download", retrievePostText())

    # Add widgets
    frame0 = Frame(homeWindow)
    frame1 = Frame(homeWindow)
    frame2 = Frame(homeWindow)

    btnHistory = Button(frame0, text="Conversion History", font=(fontstyle, 10), command=cmdHistory)

    lblAutoSTE = Label(homeWindow, text="AutoSTE", font=(fontstyle, 24))

    txtPre = Text(frame1, width=36, height=25, font=(fontstyle, 10))
    txtPost = Text(frame1, width=36, height=25, font=(fontstyle, 10), state=DISABLED)
    scrPre = Scrollbar(frame1, command=txtPre.yview)
    scrPost = Scrollbar(frame1, command=txtPost.yview)

    btnConvert = Button(frame2, width=17, height=2, text="Convert", font=(fontstyle, 10), command=cmdConvert)
    btnUpload = Button(frame2, width=17, height=2, text="Upload", font=(fontstyle, 10), command = cmdUpload)
    btnDownload = Button(frame2, width=36, height=2, text="Download", font=(fontstyle, 10), command=cmdDownload)

    # Set yscrollcommand to scroll bars
    txtPre.configure(yscrollcommand=scrPre.set)
    txtPost.configure(yscrollcommand=scrPost.set)

    # Configure widget geometry
    frame0.pack(anchor=E)
    btnHistory.pack(side='right', padx= 1, pady = 1)

    lblAutoSTE.pack(pady=40)

    frame1.pack(pady=(0,1))
    txtPre.pack(side='left')
    scrPre.pack(side='left', fill='y', padx=(0,50))
    txtPost.pack(side='left', padx=(50,0))
    scrPost.pack(side='left', fill='y')

    frame2.pack()
    btnConvert.pack(side='left', padx=(35,0), pady=1)
    btnUpload.pack(side='left', padx=(0,65), pady=1)
    btnDownload.pack(side='left', padx=50, pady=1)

    # Execute
    homeWindow.mainloop()


if __name__ == "__main__":

    # Set the font
    fontstyle = 'Courier New'

    # Create a root window and set dimensions
    root = Tk()
    root.geometry('1024x768')

    home(root, fontstyle)