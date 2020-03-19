from solution import *
from tkinter import *
from functools import partial
import tkinter


file_with_books = "./Assessment_setup_files/books.txt"
books = read_titles_of_books(file_with_books)
file_with_ratings = "./Assessment_setup_files/ratings.txt"
ratings = read_ratings(file_with_ratings)
	#name = input("What is your name?\n")
	#if not name in ratings:
	#	add_new_user(name,ratings,books)
	#n_recommendations=int(input("How many recommendations do you want?\n"))
	#similar=calculate_similarity(ratings,name,1)
	#recommend(books,ratings,ratings[name],similar,n_recommendations,1)

def on_enter(event):
	eval_username()

def eval_number():
	n_recommendations = int(textVar.get().strip())
	print(n_recommendations-1)

def eval_username():
	username = textVar.get().strip()
	print(len(username))
	messageLabel.configure(text="Hello, {}!".format(username))
	if username in ratings:
		usernameLabel.configure(text="How many recommendations do you want?")
		textVar = StringVar("")
		intButton = Button(window, text="Submit", command=partial(eval_number,window))
		intButton.grid(row=3, column=1,sticky="n")

if __name__ == "__main__":
	app_name = "Need-a-book"
	window = Tk()
	window.title(app_name)
	window.grid_rowconfigure(0, weight=1)
	window.grid_columnconfigure(1, weight=1)
	window.geometry("600x300")
	messageLabel = Label(window,text="Welcome to Need-a-book app!",font=("Helvetica", 16))
	messageLabel.grid(row=0,column=1,sticky="nsew")

	usernameLabel = Label(window, text="Username:")
	usernameLabel.grid(row=1,column=1,sticky="s")
	textVar = StringVar("")
	textEntry = Entry(window,textvariable=textVar)
	textEntry.grid(row=2,column=1)
	textEntry.bind('<Return>',on_enter)
	loginButton = Button(window, text="Login", command=partial(eval_username,window))
	loginButton.grid(row=3, column=1,sticky="n")
	window.mainloop()