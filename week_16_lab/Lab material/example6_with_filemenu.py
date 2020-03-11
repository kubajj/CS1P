
import tkinter

def display():
    name = textVar.get()
    ch = choice.get()
    if ch == 1:
        message = "Hello "+name
    elif ch == 2:
        message = "Goodbye "+name
    else:
        message = ""
    messageLabel.configure(text=message)

top = tkinter.Tk()

fileMenuButton = tkinter.Menubutton(top,text="File")
fileMenuButton.grid(row=0,column=0,sticky="W")
fileMenu = tkinter.Menu(fileMenuButton,tearoff=0)
fileMenuButton.configure(menu=fileMenu)
fileMenu.add_command(label="Exit",command=top.destroy)

textVar = tkinter.StringVar("")
textEntry = tkinter.Entry(top,textvariable=textVar,width=12)
textEntry.grid(row=1,column=0)

messageLabel = tkinter.Label(top,text="",width=12)
messageLabel.grid(row=2,column=0)

choice = tkinter.IntVar(0)

helloButton = tkinter.Radiobutton(top,text="Hello",
                                  variable=choice,value=1,command=display)
helloButton.grid(row=2,column=1)

goodbyeButton = tkinter.Radiobutton(top,text="Goodbye",
                                    variable=choice,value=2,command=display)
goodbyeButton.grid(row=2,column=2)

quitButton = tkinter.Button(top,text="Quit",command=top.destroy)
quitButton.grid(row=3,column=3)

tkinter.mainloop()
