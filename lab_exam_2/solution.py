import random


def read_titles_of_books(path_to_file):
	books = []
	with open(path_to_file) as f:
		for line in f:
			book = line.strip().split(",")
			author = book[0]
			title = book[1]
			books.append((author,title))
	return books

def read_ratings(path_to_file):
	ratings = {}
	with open(path_to_file) as f:
		user = ""
		for line in f:
			line = line.strip()
			if not user == "":
				current_user_ratings = line.split()
				current_user_ratings = [int(x) for x in current_user_ratings]
				ratings[user] = current_user_ratings
				user = ""
			else:
				user = line
	return ratings

def calculate_dot_product(v1,v2):
	dot_product = 0
	for i in range(len(v1)):
		dot_product += v1[i]*v2[i]
	return dot_product

def calculate_similarity(ratings,name,mode=0):
	similarity = []
	for user in ratings:
		if not user == name:
			similarity_with_user = calculate_dot_product(ratings[name],ratings[user])
			
			add = False
			i = 0
			while not add and i != len(similarity):
				add = similarity_with_user < similarity[i][1]
				if not add:
					i +=  1
			similarity.insert(i,(user,similarity_with_user))
	if mode == 0:
		with open("output.txt","a") as output:
			for user in similarity:
				output.write("{} similarity with {}: {}\n".format(user[0],name,user[1]))
	return similarity

def add_new_user(name,ratings,books):
	new_ratings = [0]*len(books)
	for i in range(len(books)//5):
		r = random.randint(0,len(books))
		while not new_ratings[r] == 0:
			r=random.randint(0,len(books))
		book = books[r]
		rating = int(input("What is your rating of {} by {}?\n".format(book[1],book[0])))
		new_ratings[r] = rating
	ratings[name] = new_ratings
	with open(file_with_ratings,"a") as f:
		f.write(name+"\n")
		f.write(" ".join([str(n) for n in ratings[name]]))

def recommend(books,ratings,user,similar,n,mode=0):
	s="\nRecommending based on similarity algorithm\n"+"+"*36	
	print(s)
	if mode == 0:
		output = open("output.txt","a")
		output.write(s+"\n")
	recommended = []
	other = 1
	first = True
	while n > 0:
		found = False
		while not found:
			subject_name=similar[-other][0]
			for i in range(len(books)):
				if ratings[subject_name][i] >= 3 and user[i] == 0 and not books[i] in recommended and not found:
					if first:
						s="Recommended by user: "+subject_name
						if mode == 0:
							output.write(s+"\n")
						print(s)
						first = False
					recommended.append(books[i])
					book = books[i]
					s = "\t{} by {}".format(book[1],book[0])
					if mode == 0:
						output.write(s+"\n")
					print(s)
					found = True
			if not found:
				other += 1
				first = True
		n -= 1
	if mode == 0:
		output.close()

if __name__ == "__main__":
	file_with_books = "./Assessment_setup_files/books.txt"
	books = read_titles_of_books(file_with_books)
	file_with_ratings = "./Assessment_setup_files/ratings.txt"
	ratings = read_ratings(file_with_ratings)
	output = open("output.txt","w")
	q="What is your name?"
	name = input(q+"\n")
	output.write("{} {}\n".format(q,name))
	if not name in ratings:
		add_new_user(name,ratings,books)
	q="How many recommendations do you want?"
	n_recommendations=int(input(q+"\n"))
	output.write("{} {}\n".format(q,n_recommendations))
	output.write("\n")
	output.close()
	similar=calculate_similarity(ratings,name)
	recommend(books,ratings,ratings[name],similar,n_recommendations)