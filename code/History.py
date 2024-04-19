from tkinter import *
import UploadDownload
import Home
import database
import datetime

translations = []


def history(historyWindow, fontstyle, currentUser):

    # Access global variables
    global translations

    # Set title
    historyWindow.title("History")

    # Button command functions
    def cmdBack():

        # Forget all widgets
        btnBack.pack_forget()
        lblAutoSTE.pack_forget()
        for frame in frameArr:
            frame.pack_forget()
        
        Home.home(historyWindow, fontstyle, currentUser)

    def cmdDownload(index):

        UploadDownload.promptUser("Download", translations[index].out_text)

    # Add widgets
    btnBack = Button(historyWindow, text="Back", font=(fontstyle, 10), command=cmdBack)
    
    lblAutoSTE = Label(historyWindow, text="AutoSTE", font=(fontstyle, 24))

    frameArr = []
    timeLabelsArr = []
    downloadButtonsArr = []

    translations = database.get_translations(currentUser)
    for index, translation in enumerate(translations):
        frameArr.append(Frame(historyWindow))
        timeLabelsArr.append(Label(frameArr[index], text=str(datetime.datetime.fromtimestamp(translation.timestamp)),
                                   font=(fontstyle, 10)))
        downloadButtonsArr.append(Button(frameArr[index], text="Download", font=(fontstyle, 10),
                                         command=lambda idx=index: cmdDownload(idx)))
    
    # Configure widget geometry
    btnBack.pack(anchor=W, padx=1, pady=1)
    lblAutoSTE.pack(pady=40)

    for i in range(len(timeLabelsArr)):
        frameArr[i].pack(pady=10)
        timeLabelsArr[i].pack(side = 'left', padx=20)
        downloadButtonsArr[i].pack(side = 'left', padx=20)

    # Execute
    historyWindow.mainloop()

 
if __name__ == "__main__":

    # Set the font
    fontstyle = 'Courier New'

    # Create a root window and set dimensions
    root = Tk()
    root.geometry('1024x768')

    # Login to default user
    if (user := database.login_user("uid", 'upass')) is None:
        user = database.register_user('uid', 'upass')

    history(root, fontstyle, user)
