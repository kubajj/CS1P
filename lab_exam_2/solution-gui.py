from solution import *
from tkinter import *
from functools import partial
import tkinter


def display():
	file_with_books = "./Assessment_setup_files/books.txt"
	books = read_titles_of_books(file_with_books)
	file_with_ratings = "./Assessment_setup_files/ratings.txt"
	ratings = read_ratings(file_with_ratings)
	name = input("What is your name?\n")
	if not name in ratings:
		add_new_user(name,ratings,books)
	n_recommendations=int(input("How many recommendations do you want?\n"))
	similar=calculate_similarity(ratings,name,1)
	recommend(books,ratings,ratings[name],similar,n_recommendations,1)

def login(app_name,main_window):
	login_popup = Tk()
	main_window.lower(login_popup)
	login_popup.title("{}: Login".format(app_name))
	login_popup.geometry("400x200")
	login_popup.grid_rowconfigure(1, weight=1)
	login_popup.grid_columnconfigure(1, weight=1)
	leftLabel = Label(login_popup,text="")
	leftLabel.grid(row=0,column=0,rowspan=2)
	rightLabel = Label(login_popup,text="")
	rightLabel.grid(row=0,column=2,rowspan=2)
	usernameLabel = Label(login_popup, text="User Name")
	usernameLabel.grid(row=0,column=1,sticky="s")
	textVar = StringVar("")
	textEntry = Entry(login_popup,textvariable=textVar)
	textEntry.grid(row=1,column=1)
	loginButton = Button(login_popup, text="Login", command=evaluate_username(textVar.get()))
	loginButton.grid(row=2, column=1,sticky="n")
	login_popup.mainloop()

def on_enter(event):
	eval()

def eval():
	username = textVar.get()
	print(len(username))

if __name__ == "__main__":
	app_name = "Need-a-book"
	window = Tk()
	window.title(app_name)
	window.grid_rowconfigure(0, weight=1)
	window.grid_columnconfigure(1, weight=1)
	window.geometry("600x300")
	messageLabel = Label(window,text="Welcome to Need-a-book app!",font=("Helvetica", 16))
	messageLabel.grid(row=0,column=1,sticky="nsew")
	#loginButton = Button(window, text="Login", command=partial(login,app_name,window))
	#loginButton.grid(row=1, column=0)
	#signinButton = Button(window, text="SignIn", command=partial(login,app_name,window))
	#signinButton.grid(row=1, column=2)
	usernameLabel = Label(window, text="Username:")
	usernameLabel.grid(row=1,column=1,sticky="s")
	textVar = StringVar("")
	textEntry = Entry(window,textvariable=textVar)
	textEntry.grid(row=2,column=1)
	textEntry.bind('<Return>',on_enter)
	loginButton = Button(window, text="Login", command=eval)
	loginButton.grid(row=3, column=1,sticky="n")
	window.mainloop()