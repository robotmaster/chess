from tkinter import *


def getInput():
    def exit(event):
        master.destroy()
    master=Tk()
    master.bind("<Escape>", exit)

    global f,e
    f=None

    def callback():
        global f,e
        f=e.get()

    def close_program():
        global f
        if f.lower() in ['queen','knight','rook','bishop']:
            master.destroy()

    def disable_event():
        pass
    class ABC(Frame):
        def __init__(self,parent=None):
            Frame.__init__(self,parent)
            self.parent = parent
            self.make_widgets()

        def make_widgets(self):
            # don't assume that self.parent is a root window.
            # instead, call `winfo_toplevel to get the root window
            self.winfo_toplevel().title("Promotion")

            # this adds something to the frame, otherwise the default
            # size of the window will be very small
            label = Entry(self)
            label.pack(side="top",fill="x")
    ABC(master)
    e=Entry(master)
    e.pack()
    e.focus_set()

    #makes the button
    master.protocol("WM_DELETE_WINDOW",disable_event)
    b=Button(master,text="promote",width=100,command=lambda:[callback(),close_program()])
    b.pack()
    #pop up new window
    mainloop()
    return f
def checkflipboard():
    def exit(event):
        master.destroy()
        quit()
    master=Tk()
    master.bind("<Escape>", exit)

    global answer,answer_e
    answer=None

    def callback():
        global answer,answer_e
        answer=answer_e.get()

    def close_program():
        global answer
        if answer.lower() in ['no','yes']:
            master.destroy()

    def disable_event():
        pass
    class ABC(Frame):
        def __init__(self,parent=None):
            Frame.__init__(self,parent)
            self.parent = parent
            self.make_widgets()

        def make_widgets(self):
            # don't assume that self.parent is a root window.
            # instead, call `winfo_toplevel to get the root window
            self.winfo_toplevel().title("Would you like your board flipped when you move?")

            # this adds something to the frame, otherwise the default
            # size of the window will be very small
            label = Entry(self)
            label.pack(side="top",fill="x")
    ABC(master)
    answer_e=Entry(master)
    answer_e.pack()
    answer_e.focus_set()

    #makes the button
    master.protocol("WM_DELETE_WINDOW",disable_event)
    b=Button(master,text="ok",width=100,command=lambda:[callback(),close_program()])
    b.pack()
    #pop up new window
    mainloop()
    return answer
