
import tkinter

def display():
    rates=[1,0.78,0.85,0.0072,0.034,0.58]
    currencies=["£","$","€","¥","CZK","CAD"]
    try:
        amount=float(textVar.get())
        currency_from=c_from.get()
        rate_from=rates[currency_from]
        currency_to=c_to.get()
        rate_to=rates[currency_to]
        res=amount*rate_from/rate_to
        #messageLabel.configure(text="{:.2f}".format(res))
        fromLabel.configure(text=str(amount) + " " + str(currencies[currency_from]))
        toLabel.configure(text="{:.2f}".format(res) + " " + str(currencies[currency_to]))
        messageLabel.configure(text="")
    except:
        messageLabel.configure(text="Please enter a number.")
        currency_from=c_from.get()
        currency_to=c_to.get()
        fromLabel.configure(text=str(currencies[currency_from]))
        toLabel.configure(text=str(currencies[currency_to]))

def on_enter(event):
	display()

top = tkinter.Tk()

textVar = tkinter.StringVar("")
textEntry = tkinter.Entry(top,textvariable=textVar)
textEntry.grid(row=0,column=0,columnspan=2)
textEntry.bind('<Return>',on_enter)

messageLabel = tkinter.Label(top,text="")
messageLabel.grid(row=3,column=0,columnspan=2)

fromLabel = tkinter.Label(top, text="")
fromLabel.grid(row=2,column=0)

toLabel= tkinter.Label(top, text="")
toLabel.grid(row=2, column=1)

c_from = tkinter.IntVar(0)
c_to = tkinter.IntVar(0)

convertButton = tkinter.Button(top,text="Convert",command=display,width=6)
convertButton.grid(row=2,column=2)

#---------------------------------------------------------------------------#

fromMenuButton = tkinter.Menubutton(top,text="From")
fromMenuButton.grid(row=1,column=0)
fromMenu = tkinter.Menu(fromMenuButton,tearoff=0)
fromMenuButton.configure(menu=fromMenu)

fromMenu.add_radiobutton(label="£",variable=c_from,value=0,command=display)
fromMenu.add_radiobutton(label="$",variable=c_from,value=1,command=display)
fromMenu.add_radiobutton(label="€",variable=c_from,value=2,command=display)
fromMenu.add_radiobutton(label="¥",variable=c_from,value=3,command=display)
fromMenu.add_radiobutton(label="CZK",variable=c_from,value=4,command=display)
fromMenu.add_radiobutton(label="CAD",variable=c_from,value=5,command=display)

#---------------------------------------------------------------------------#

toMenuButton = tkinter.Menubutton(top,text="To")
toMenuButton.grid(row=1,column=1)
toMenu = tkinter.Menu(toMenuButton,tearoff=0)
toMenuButton.configure(menu=toMenu)

toMenu.add_radiobutton(label="£",variable=c_to,value=0,command=display)
toMenu.add_radiobutton(label="$",variable=c_to,value=1,command=display,state=tkinter.ACTIVE)
toMenu.add_radiobutton(label="€",variable=c_to,value=2,command=display)
toMenu.add_radiobutton(label="¥",variable=c_to,value=3,command=display)
toMenu.add_radiobutton(label="CZK",variable=c_to,value=4,command=display)
toMenu.add_radiobutton(label="CAD",variable=c_to,value=5,command=display)

#--------------------------------------------------------------------------#

quitButton = tkinter.Button(top,text="Quit",command=top.destroy,width=6)
quitButton.grid(row=3,column=2)

tkinter.mainloop()
