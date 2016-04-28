from Tkinter import Tk, BOTH, RIGHT, RAISED, Text, TOP, X, N, W, LEFT, BooleanVar, Checkbutton, Frame
from Tkinter import Frame as interFrame
from ttk import Frame, Button, Style, Label, Entry


class Example(Frame):
    def __init__(self, parent):
        # Frame.__init__(self, parent, background="white")
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Data Entry")
        self.style = Style()
        self.style.theme_use("default")
        self.style.configure("TButton", padding=(1,5,1,5), font='serif 12')

        self.pack(fill=BOTH, expand=True)  #
        self.placeWindow()

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text='First Name', width=8)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        entry1 = Entry(frame1)
        entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Last Name", width=8)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        entry2 = Entry(frame2)
        entry2.pack(fill=X, padx=5, expand=True)


        frame_notes = Frame(self)
        frame_notes.pack(fill=BOTH)

        self.bool_notes = BooleanVar(master=frame_notes)
        cb = Checkbutton(self, text="Notes on the Resume", variable=self.bool_notes, command=self.onClick())
        cb.select()
        # cb.place(x=50, y=50)
        cb.pack(side=TOP, anchor=W)



        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=True)

        lblnotes = Label(frame3, text="Alt e-mail", width=8)
        lblnotes.pack(side=LEFT, anchor=N, padx=5, pady=5)

        txt = Text(frame3)
        txt.pack(fill=BOTH, pady=5, padx=5, expand=True)
        txt.

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)




        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=RIGHT, padx=5, pady=5)
        # quitButton.place(x=100, y=700)
        exportButton = Button(self, text="Export to CSV")
        exportButton.pack(side=RIGHT)

    def onClick(self):
        if self.bool_notes.get() == True:
            pass
        else:
            pass





    def placeWindow(self):

        w = 450
        h = 800

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = sw - w
        y = 0
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
    root = Tk()
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()