
import tkinter

def display():
    name = textVar.get()
    messageLabel.configure(text="Hello "+name)

top = tkinter.Tk()
top.title("This is my title")
top.geometry("500x500-600-100")
top.configure(bg="white")

textVar = tkinter.StringVar("")
textEntry = tkinter.Entry(top,textvariable=textVar,width=12, bg="white")
textEntry.grid(row=0,column=0)

messageLabel = tkinter.Label(top,text="",width=12, bg="white")
messageLabel.grid(row=1,column=0)

showButton = tkinter.Button(top,text="Show",command=display, bg="white", activebackground="white")
showButton.grid(row=1,column=1)

quitButton = tkinter.Button(top,text="Quit",command=top.destroy, bg="white", activebackground="white")
quitButton.grid(row=1,column=2)

tkinter.mainloop()
