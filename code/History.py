from tkinter import *
import UploadDownload
import Home

convTimeHistory = []
convTextHistory = []

def history(historyWindow, fontstyle):

    #Access global variables
    global convTimeHistory
    global convTextHistory

    #Set title
    historyWindow.title("History")

    #Button command functions
    def cmdBack():

        #Forget all widgets
        btnBack.pack_forget()
        lblAutoSTE.pack_forget()
        for i in range(len(frameArr)):
            frameArr[i].pack_forget()
        
        Home.home(historyWindow, fontstyle)

    def cmdDownload(index):

        UploadDownload.promptUser("Download", convTextHistory[-1-index])

    #Add widgets
    btnBack = Button(historyWindow, text="Back", font=(fontstyle, 10), command=cmdBack)
    
    lblAutoSTE = Label(historyWindow, text="AutoSTE", font=(fontstyle, 24))

    frameArr = []
    timeLabelsArr = []
    downloadButtonsArr = []
    for i in range(len(convTimeHistory)):
        frameArr.append(Frame(historyWindow))
        timeLabelsArr.append(Label(frameArr[i], text=convTimeHistory[-1-i], font=(fontstyle, 10)))
        downloadButtonsArr.append(Button(frameArr[i], text="Download", font=(fontstyle, 10), command=lambda idx = i: cmdDownload(idx)))
    
    #Configure widget geometry
    btnBack.pack(anchor=W, padx=1, pady=1)
    lblAutoSTE.pack(pady=40)

    for i in range(len(timeLabelsArr)):
        frameArr[i].pack(pady=10)
        timeLabelsArr[i].pack(side = 'left', padx=20)
        downloadButtonsArr[i].pack(side = 'left', padx=20)

    
    #Execute
    historyWindow.mainloop()


def addConversion(convTime, convText):
    global convTimeHistory
    global convTextHistory

    #Only store 10 recent conversions
    if len(convTimeHistory)==10:
        convTimeHistory.pop(0)
        convTextHistory.pop(0)

    convTimeHistory.append(convTime)
    convTextHistory.append(convText)

 
if __name__ == "__main__":

    #Set the font
    fontstyle = 'Courier New'

    #Create a root window and set dimensions
    root = Tk()
    root.geometry('1024x768')

    history(root, fontstyle)
    
