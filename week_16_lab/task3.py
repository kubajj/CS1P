
import tkinter

def display():
    rates=[1,0.78,0.85,0.0072,0.034,0.58]
    try:
        amount=float(textVar.get())
        currency_from=rates[c_from.get()]
        currency_to=rates[c_to.get()]
        res=amount*currency_from/currency_to
        messageLabel.configure(text="{:.2f}".format(res))
    except:
        messageLabel.configure(text="Please enter a number.")



top = tkinter.Tk()

textVar = tkinter.StringVar("")
textEntry = tkinter.Entry(top,textvariable=textVar,width=12)
textEntry.grid(row=0,column=0)

messageLabel = tkinter.Label(top,text="",width=30)
messageLabel.grid(row=1,column=0)

c_from = tkinter.IntVar(0)
c_to = tkinter.IntVar(0)

poundButton_from = tkinter.Radiobutton(top,text="£",variable=c_from,value=0,command=display)
poundButton_from.grid(row=1,column=1)

poundButton_to = tkinter.Radiobutton(top,text="£",variable=c_to,value=0,command=display)
poundButton_to.grid(row=1,column=2)

dollarButton_from = tkinter.Radiobutton(top,text="$",variable=c_from,value=1,command=display)
dollarButton_from.grid(row=2,column=1)

dollarButton_to = tkinter.Radiobutton(top,text="$",variable=c_to,value=1,command=display)
dollarButton_to.grid(row=2,column=2)

euroButton_from = tkinter.Radiobutton(top,text="€",variable=c_from,value=2,command=display)
euroButton_from.grid(row=3,column=1)

euroButton_to = tkinter.Radiobutton(top,text="€",variable=c_to,value=2,command=display)
euroButton_to.grid(row=3,column=2)

yenButton_from = tkinter.Radiobutton(top,text="¥",variable=c_from,value=3,command=display)
yenButton_from.grid(row=3,column=1)

yenButton_to = tkinter.Radiobutton(top,text="¥",variable=c_to,value=3,command=display)
yenButton_to.grid(row=3,column=2)

czkButton_from = tkinter.Radiobutton(top,text="CZK",variable=c_from,value=4,command=display)
czkButton_from.grid(row=4,column=1)

czkButton_to = tkinter.Radiobutton(top,text="CZK",variable=c_to,value=4,command=display)
czkButton_to.grid(row=4,column=2)

cadButton_from = tkinter.Radiobutton(top,text="CAD",variable=c_from,value=5,command=display)
cadButton_from.grid(row=5,column=1)

cadButton_to = tkinter.Radiobutton(top,text="CAD",variable=c_to,value=5,command=display)
cadButton_to.grid(row=5,column=2)

quitButton = tkinter.Button(top,text="Quit",command=top.destroy)
quitButton.grid(row=6,column=1)

tkinter.mainloop()
