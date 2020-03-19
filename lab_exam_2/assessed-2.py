class User():
    # instance of user object has name and rating
    def __init__(self, name=None, user_ratings=None):
        self.name = name
        self.user_ratings = user_ratings

#########################################################################################################################

def read_book_file(file_name):
    import sys
    books = {}
    book_list = []
    # start of try - except  block
    try:
        # opening file for reading
        with open(file_name, "r") as file:
            # getting every line in the file
            lines = file.readlines()
            # iterating through each and every line
            for line in lines:
                # removing \n character at the end of every string
                line = line.replace("\n", "")
                # splitting string where "," appears
                line = line.split(",")
                # getting book and author value
                author = line[0]
                book = line[1]
                # adding book to the list
                if book not in book_list:
                    book_list.append(book)
                # if author already in the dict. we append book to the book list
                if author in books.keys():
                    books[author].append(book)
                # if author not in dict. we create new author:[book] pair
                else:
                    books[author] = [book]
        return books, book_list
    # exception handling part
    except:
        # informing user about the error, printing the error using sys library
        print("An unexpected error has occurred. Displaying error message and closing the file: " + str(sys.exc_info()))
        try:
            # attempting to close the file
            file.close()
            sys.exit("File successfully closed.")
        except:
            # if file failed to close, informing the user
            print("Failed to close the file.")
            return 0


#########################################################################################################################

def read_user_file(file_name):
    import sys
    user_rating = {}
    # start of try - except  block
    try:
        # opening file for reading
        with open(file_name, "r") as file:
            # getting every line in the file
            lines = file.readlines()
            # iterating over the lines, we jump by two every iteration since we have name - rating pair separated by \n
            for i in range(0, len(lines), 2):
                # retrieving the user name
                user_name = lines[i]
                user_name = user_name.replace("\n", "")
                # getting string of ratings
                string = lines[i + 1]
                # removing \n and splitting string where " " appears
                string = string.replace("\n", "")
                string = string.split(" ")
                # we parse string, removing the last element which is empty string
                string = string[0:len(string) - 2]
                # saving each value of rating in list by iterating over string and changing str to int
                ratings = [int(x) for x in string]
                # making name:User.object pair
                user_rating[user_name.lower()] = User(name=user_name.lower(), user_ratings=ratings)

        return user_rating

    # exception handling part
    except:
        # informing user about the error, printing the error using sys library
        print("An unexpected error has occurred. Displaying error message and closing the file: " + str(sys.exc_info()))
        try:
            # attempting to close the file
            file.close()
            sys.exit("File successfully closed.")
        except:
            # if file failed to close, informing the user
            print("Failed to close the file.")
            return 0


#########################################################################################################################
                                      ##### THE MAIN PROGRAM FUNCTION #####
def the_program():
    import sys
    users = read_user_file("ratings.txt")
    authors, book = read_book_file("books.txt")

    print("Welcome to the book recommendation program.")
    print("If you wish to close the program during any procedure, please enter 'exit'.")
    # asking user if he has and existing account and acting upon it
    is_new = input("If you are existing user, please enter 0, if you are new user, please enter 1: ")
    # checking if the user input is valid
    if is_new not in "0123456789":
        is_new = input_validator(_input=is_new, _type=1)
    else:
        is_new = int(is_new)
        while is_new != 0 and is_new != 1:
            is_new = input("Incorrect number, please try again: ")
            if type(is_new) == type("") and is_new.lower() == "exit":
                sys.exit("Closing the program.")
    is_new = input_validator(_input=is_new, _type=1)
    # if its a new user, call function to create new account
    if is_new:
        print("Creating new user account")
        new_user,new_user_ratings = get_user_info(users, book)
        # due to formatting convention used, we save username without capital letters
        new_user = new_user.lower()
        users[new_user] = User(name=new_user, user_ratings=new_user_ratings)
        user_name = new_user
    # if user claims to be existing user, execute this
    else:
        user_name = input("Welcome back! Please, enter your name: ")
        # checking if the users input is valid
        user_name = input_validator(_input=user_name, _type="")
        # if entered name is not in database, ask user if they want to try again or create a new account
        while user_name.lower() not in users.keys():
            choice = input("We were not able to match your name with any existing record. If you wish to try again,"
                              "enter 0, if you wish to create new account, enter 1: ")
            # checking if users input is valid
            if choice not in "0123456789":
                choice = input_validator(_input=choice, _type=1)
            else:
                # is choice is a number, validate if its 0 or 1
                choice = int(choice)
                while choice != 0 and choice != 1:
                    choice = input("Incorrect number, please try again: ")
                    # if users decides to exit the program, execute the following if statement
                    if type(choice) == type("") and choice.lower() == "exit":
                        sys.exit("Closing the program.")
            # if 0 entered, ask user for name again
            if choice == 0:
                user_name = input("Enter your name: ")
            # if 1 entered, call a function to create new account
            elif choice:
                print("Creating new user account.")
                new_user, new_user_ratings = get_user_info(users, book)
                # due to formatting convention used, we save username without capital letters
                new_user = new_user.lower()
                users[new_user] = User(name=new_user, user_ratings=new_user_ratings)
                user_name = new_user
    # call the similarity algorithm function
    recommendation_list = similarity_alg(user=user_name, users=users, books=book, authors=authors)
    # printing out the result
    with open("output.txt","a") as file:
        file.write("\nRecomending based on similarity ratings")
        file.write("\n###############################################")
        for user in recommendation_list:
            file.write("\nRecommended by " + user.title() + ": ")
            for recom_books in recommendation_list[user]:
                for author,book in authors.items():
                    if recom_books in book:
                        file.write("\n        " + recom_books + " by " + author)

    print("Result stored in output.txt")
    # returning 0 to inform of successful run of the program
    return 0


#########################################################################################################################

def similarity_alg(user=None,users=None,books=None,authors=None):
    import sys
    user = user.lower()
    # getting the list of ratings of the user
    r1 = users[user].user_ratings
    similarity_list = []
    # getting number of recommendations from user
    recommendations = input("Please, enter the number of recommendations (max number {number}): ".format(number=len(books)-1))
    # validating user input
    try:
        recommendations = int(recommendations)
    except:
        recommendations = input_validator(_input=recommendations, _type=1)
    # validate if recom. number is larger than 0 and smaller then overall number of books
    if recommendations < 0 or recommendations > len(books):
        print("Recommendation number is too large, please enter number smaller or equal to " + str(len(books)-1))
        # ask users to input correct number until he does
        while recommendations < 0 or recommendations > len(books):
            recommendations = input("Incorrect number, please try again: ")
            if type(recommendations) == type("") and recommendations.lower() == "exit":
                sys.exit("Closing the program.")
            recommendations = input_validator(_input=recommendations, _type=1)
    # iterating over users in users.dict
    for u in users:
        similarity = 0
        # we do not count similarity if we have the same user
        if u == user:
            continue
        else:
            # getting ratings of the other user
            r2 = users[u].user_ratings
            # iterating over the ziped list of ratings of both users
            for x,y in zip(r1,r2):
                # calculating the similarity
                similarity += int(x)*int(y)
            # appending the result to the list as a (name,rating) tuple
            similarity_list.append((u,similarity))
    # sorting the similarity list based on the similarity number
    similarity_list = sorted(similarity_list, reverse=True, key=lambda x: x[1])
    print("\n")
    # print out similarity
    with open("output.txt","w") as file:
        # reversing the similarity list from the lowest to highest
        # we store result in different variable as we do not want to change similarity list itself due to
        # later implementation
        write_out_list = similarity_list[::-1]
        for e in write_out_list:
            file.write(user.title() + " similarity with " + e[0].title() + " : " + str(e[1])+"\n")
    # create recommended list to store recommended books
    recommended = {}
    # we will use g to count number of recommended books
    g = 0
    # we use rating list in order to iterate over ratings
    rate_list = [5, 3, 1, 0, -1, -3, -5]
    while True:
        # we iterate over ratings to change in case we cant find enough 5 ratings to recommend
        # we then iterate over books rated 3 to recommend and in case there are not enough books we repeat the process
        for rate in rate_list:
            # we iterate over the number of users already in database
            for k in range(len(users.keys())-1):
                # get recommenders name
                recommender = similarity_list[k][0]
                # get rating r1 of recommender and rating r2 of our users to whom we recommend books
                r1 = users[recommender].user_ratings
                r2 = users[user].user_ratings
                # iterate over all the books
                for i in range(len(books)-1):
                    # rating1 and rating2 correspond to specific rating in rating list of users and since ratings are in
                    # the same order as books, index of rating corresponds to index of book in books list
                    rating1 = r1[i]
                    rating2 = r2[i]
                    # if the recommended book has rating 5 and recommendee has not yet read it,
                    # append to recommended list
                    if rating1 == rate and rating2 == 0:
                        # since the format of recommended dict is recommender:[recom. books]
                        # in case the recommender is not
                        # yet in the dict, create new pair
                        if recommender not in recommended.keys():
                            recommended[recommender] = [books[i]]
                        # if recommender is already in list, only append the book to his recom. books list
                        else:
                            recommended[recommender].append(books[i])
                        # increase g if book is recommended
                        g += 1
                        # if g equals number of recmmendations, return the dict.
                        if g == recommendations:
                            return recommended



#########################################################################################################################

def input_validator(_input,_type):
    import sys
    # this function validates user input given _input parameter and desired _type parameter
    # we have separate checking for int and str
    if type(_type) == type(1):
        # we enter the try block
        try:
            # ask user for input until its valid
            while type(_input) != type(1):
                _input = input("Inccorrect input format, please try again: ")
                # in case users enters exit raise SystemExit
                if type(_input) == type("") and _input.lower() == "exit":
                    sys.exit()
                # assert if the types match if not, raise AssertionError
                assert type(_type) == type(_input)
        except SystemExit:
            sys.exit("Closing the program.")
        except AssertionError:
            # in case of assertion error, we just call the function again
            _input = input_validator(_input, _type)

    # we do the same with string type
    if type(_type) == type(""):
        try:
            while type(_input) != type(""):
                _input = input("Inccorrect input format, please try again: ")
                if type(_input) == type("") and _input.lower() == "exit":
                    sys.exit()
                assert type(_type) == type(_input)
        except SystemExit:
            sys.exit("Closing the program.")
        except AssertionError:
            _input = input_validator(_input, _type)
    # if inout is correct, return it
    return _input

#########################################################################################################################

def get_user_info(users, book):
    user_name = input("Please enter your name: ")
    user_name = input_validator(_input=user_name, _type="")

    # checking if there is a user with the same name, if there is, append number to the end of the new user (user1, user2...)
    i = 0
    new_name = user_name
    executed = False
    while new_name in users.keys():
        new_name = user_name + " " + str(i)
        i += 1
        # if this part of code was executed, we inform user about change of his user name
        executed = True
    if executed:
        print("Due to existing user name " + user_name + " we have modified your name to: " + new_name)
    user_name = new_name

    # we call a function to generate ratings for the user
    ratings = get_ratings(book)
    return user_name,ratings

#########################################################################################################################

def get_ratings(book):
    import random as rn
    import sys
    ratings = []
    book_number = len(book)
    # getting number representing about 20% of the books
    choice_number = int((book_number/100)*20)

    print("Please rate the following books using this scale: \n")
    print("Rating      Meaning")
    print('-5          Hated it!')
    print("-3          Didn’t like it")
    print(" 0          Haven’t read it")
    print(' 1          OK')
    print(" 3          Liked it!")
    print(" 5          Really liked it!")

    # we create list to check if rating input is valid
    rate_list = ['-5','-3','0','1','3','5']
    # initializing ratings list with all elements 0 to represent book that haven't been read yet
    rating = [0 for x in range(book_number)]

    for i in range(choice_number):
        # we generate random number to pick a book
        choice = rn.randint(0, book_number-1)
        # we select a book from the list of books
        chosen_book = book[choice]
        # asking for an input
        rate = input("Rate the following book " + chosen_book + ": ")
        # while input number is incorrect, we keep asking for input or exit the program upon entering "exit"
        while rate not in rate_list:
            rate = input("Incorrect rating, please try again: ")
            if type(rate) == type("") and rate.lower() == "exit":
                sys.exit("Closing the program.")

        rating[choice] = rate
    return rating

#########################################################################################################################