import random
from typing import TextIO


# This function prints error messages, it is used to reduce the size of strings in the exception handling
# and to have a handy lookup table of all the handled exceptions
def print_error_message(error_message, *args):
    default_message = "Error occurred: "
    if error_message == "Not found":
        print(default_message + "File {} not found.".format(args[0]))
    elif error_message == "File empty":
        print(default_message + "File {} is empty which was not expected.".format(args[0]))
    elif error_message == "Wrong format":
        print(default_message + "File {} is in wrong format.".format(args[0]))
    elif error_message == "Vector size error":
        print(default_message + "Vectors passed to the dot product function were not of the same size.")
    else:
        # This should not be used
        print("Error occurred.")
    print("Terminating execution.")
    exit(1)


# This function reads the file with books and return the list with author, title tuples
def read_books_file(path_to_file):
    # Create an empty list for the return value
    books = []
    try:
        with open(path_to_file) as f:
            for line in f:
                # Split the entry and store it in variable book
                book = line.strip().split(",")
                # If the book entry is in the wrong format, print error message and stop execution
                if not len(book) == 2:
                    print_error_message("Wrong format", path_to_file)
                    f.close()
                # First part is expected to be the author of the book
                author = book[0]
                # Second part is expected to be the title of the book
                title = book[1]
                # Add tuple of author and title to the books
                books.append((author, title))
        # If the file is empty, print error message and stop execution because we cannot recommend any books
        if len(books) == 0:
            print_error_message("File empty", path_to_file)
        return books
    except FileNotFoundError:
        print_error_message("Not found", path_to_file)


# This function reads the file with ratings and returns a dictionary with usernames as keys and their ratings in a list
# of integers as value
def read_ratings_file(path_to_file, number_of_books):
    # Create an empty dictionary for the return value
    ratings = {}
    try:
        with open(path_to_file) as f:
            # First line of each pair is expected to contain username
            # User is a variable which will store the username and is also used as a flag
            user = ""
            for line in f:
                # Remove '\n' from the end of the line
                line = line.strip()
                # If user is not "", then the program knows that it is reading the second line
                # of the user, ratings pair, so it expects the line to contain ratings
                if not user == "":
                    current_user_ratings = line.split()
                    try:
                        # Convert all the ratings to integers
                        current_user_ratings = [int(x) for x in current_user_ratings]
                    except TypeError:
                        # At least one of the ratings was not an integer
                        print_error_message("Wrong format", path_to_file)
                        f.close()
                    # If nothing is wrong with types, check if there are as many ratings as they are books,
                    # then add user with ratings to the ratings dictionary
                    else:
                        if not len(current_user_ratings) == number_of_books:
                            print_error_message("Wrong format", path_to_file)
                            f.close()
                        # If the entry is in correct format, add it to ratings dictionary
                        ratings[user] = current_user_ratings
                        # Reset user variable(/flag)
                        user = ""
                else:
                    # If user is "", we are reading the first line of the pair
                    user = line
        # Return
        return ratings
    except FileNotFoundError:
        # File was not found, print error message and stop execution
        print_error_message("Not found", path_to_file)


# This function calculates the dot product of two lists
def calculate_dot_product(v1, v2):
    # Initialize the variable to return
    dot_product = 0
    # This error should not happen in this usage as the sizes of the rating lists are checked in read_ratings_file
    # and so they should match the length of books list.
    if not len(v1) == len(v2):
        print_error_message("Vector size error")
    # Calculate the dot product
    for i in range(len(v1)):
        dot_product += v1[i] * v2[i]
    return dot_product


# This function calculates the similarity of each of the users ratings with the user given and returns a list of tuples
# (user, similarity with the given user)
def calculate_similarity(ratings_dict, name_of_current_user, mode=0):
    # Initialize an empty list for the result
    similarity = []
    # loop through all the users
    for user in ratings_dict:
        # If user is the user given, do not include him in the result
        if not user == name_of_current_user:
            # Call the dot product function on the ratings of both users
            similarity_with_user = calculate_dot_product(ratings_dict[name_of_current_user], ratings_dict[user])

            # Insert the new entry to the sorted similarity list
            add = False
            i = 0
            # This loop finds the first user in the list that has bigger similarity than the currently considered user
            # and inserts the currently considered user entry to that place
            while not add and i != len(similarity):
                add = similarity_with_user < similarity[i][1]
                if not add:
                    i += 1
            similarity.insert(i, (user, similarity_with_user))
    # If mode is not 0, the output is not written to a file (could be used in a gui)
    if mode == 0:
        with open("output.txt", "a") as output:
            for user in similarity:
                output.write("{} similarity with {}: {}\n".format(user[0], name_of_current_user, user[1]))
    return similarity


# This function gives user the opportunity to rate books
# It asks him for his rating of each of n books and then stores his ratings in the ratings file
def rate_books(name_of_user, books, n):
    # Print the expected input for the ratings
    print("\tRating\tMeaning\n",
          "\t-5\tHate it!\n",
          "\t-3\tDidn't like it\n",
          "\t0\tHaven't read it\n",
          "\t1\tOK\n",
          "\t3\tLiked it\n",
          "\t5\tReally liked it!\n")
    # Update will be True if the user is just rating more books, so he was already in the ratings dictionary
    update = False
    if name_of_user in ratings:
        # If he was in the ratings dictionary, load his ratings
        new_ratings = ratings[name_of_user]
        update = True
    else:
        # if not, create a list of zeros
        new_ratings = [0] * len(books)
    # Calculate the maximum number of books to be rated (number of zeros in new_ratings)
    max_n_ratings = 0
    for rating in new_ratings:
        if rating == 0:
            max_n_ratings += 1
    # If user wants to rate more books than possible, give him opportunity to rate only as many books as is possible
    if n > max_n_ratings:
        n = max_n_ratings
    # Let user rate a book n times
    for i in range(n):
        # r is a random index in the new_ratings list
        r = random.randint(0, len(books))
        # If the book with that index was already rated, randomly choose different r and try again
        # This cannot be infinite loop, because we calculated the maximum number of ratings, so there
        # has to be at least one 0 in new_ratings
        while not new_ratings[r] == 0:
            r = random.randint(0, len(books))
        # Load corresponding title of the book and its author
        book = books[r]
        # Ask for user input and make sure that the value is one of the values from the table
        possible_ratings = ["-5", "-3", "0", "1", "3", "5"]
        # Do not repeat that the user should use only one of the possible values if he did not
        # make a mistake yet
        first = True
        not_an_option = True
        print("What is your rating of {} by {}?".format(book[1], book[0]))
        while not_an_option:
            if not first:
                print("Please use only the values from the table above.")
            else:
                first = False
            # Ask for the user rating
            rating = input("Your rating:").strip()
            # Check if it is one of the options
            if rating in possible_ratings:
                # Terminate the iteration
                not_an_option = False
                # Cast rating to integer
                rating = int(rating)
        # Add the new rating to the list
        new_ratings[r] = rating
    # Update the user entry in ratings dictionary
    ratings[name_of_user] = new_ratings
    # If user was already in ratings, update the line at which he is in the file
    # I did not figure out any other option, than overwriting the whole file
    if update:
        # Overwrite the ratings file with ratings dictionary
        with open(file_with_ratings, "w") as f:
            for user in ratings:
                f.write(user + "\n")
                f.write(" ".join([str(n) for n in ratings[user]]) + "\n")
    # If user was not in ratings, just append his entry to the end of the file
    else:
        with open(file_with_ratings, "a") as f:
            f.write(name_of_user + "\n")
            f.write(" ".join([str(n) for n in ratings[name_of_user]]) + "\n")
    # Terminate the execution of the function with a message
    print("Thank you for your ratings.\n\n")


# This function recommends the user books based on the similarity algorithm and prints them out grouped by the user
# who recommmended it
def recommend(books, ratings, user, similar, n, mode=0):
    # Mode 0 means that the program should print outputs to the output file as well
    if mode == 0:
        output_file = open("output.txt", "a")
    # Initialize an empty list which stores already recommended books
    recommended = []
    # Other is a variable which contains index of the user which we are considering now
    # (1 means that it is the last one)
    other = 1
    # If we did not recommend any book by current subject yet, first remains true
    first = True
    while n > 0:
        found = False
        while not found:
            # If we ran out of users that read other books than the current user, exit with an apology
            if other == len(ratings):
                if len(recommended) == 0:
                    s = "\nI am sorry, I cannot recommend you any books now."
                else:
                    s = "\nI am sorry, I cannot recommend you more books now."
                if mode == 0:
                    output_file.write(s + "\n")
                print(s)
                found = True
                n = 0
            else:
                # Load the considered subject
                # (the most similar ones are at the end, which is the reason for using -other)
                subject_name = similar[-other][0]
                # Try to find a book
                for i in range(len(books)):
                    # Which other user rated with 3 or 5 and our user have not read yet and was not recommended yet
                    if ratings[subject_name][i] >= 3 and user[i] == 0 and not books[i] in recommended and not found:
                        # If this is the first book overall, print the introduction to recommendations
                        if len(recommended) == 0 and mode == 0:
                            s = "\nRecommending based on similarity algorithm\n" + "+" * 36
                            print(s)
                            output_file.write(s + "\n")
                        # If this is the first book recommended by current subject, print subjects name
                        if first:
                            s = "Recommended by user: " + subject_name
                            if mode == 0:
                                output_file.write(s + "\n")
                            print(s)
                            first = False
                        # Add this book to already recommended books to prevent recommending it again
                        book = books[i]
                        recommended.append(book)
                        # Print the recommendation
                        s = "\t{} by {}".format(book[1], book[0])
                        if mode == 0:
                            output_file.write(s + "\n")
                        print(s)
                        found = True
            # If current subject does not have any recommendations, try the next one
            if not found:
                other += 1
                first = True
        # Prepare the next iteration
        n -= 1
    if mode == 0:
        output_file.close()


# The following executes if the recommendations are called on their own (without gui, which I did not implement)
if __name__ == "__main__":
    # Define the books file
    file_with_books = "books.txt"
    # Read books
    books = read_books_file(file_with_books)
    # Define ratings file
    file_with_ratings = "ratings.txt"
    # Read ratings
    ratings = read_ratings_file(file_with_ratings, len(books))
    # Define output file and open it
    output_file = open("output.txt", "w")
    # Ask for username
    q = "What is your name?"
    # Handle user's response
    name = input(q + "\n")
    output_file.write("{} {}\n".format(q, name))
    # New user - ask for rating of ~ 20 % of books
    if not name in ratings:
        print("Before we start, I need you to rate some books.")
        rate_books(name, books, len(books) // 5)
    # Existing user - ask if he wants to rate more books
    else:
        not_answered = True
        recommend_more = ""
        print("Do you want to rate more books?")
        while not_answered:
            recommend_more = input("[Please insert Y/N]").strip()
            if recommend_more == "Y" or recommend_more == "y":
                not_answered = False
                recommend_more = True
            elif recommend_more == "N" or recommend_more == "n":
                not_answered = False
                recommend_more = False
            # If none of the previous options is matched, continue
        # The variable recommend more has to be either True or False when the user answered
        if recommend_more:
            not_given_int = True
            print("How many more books do you want to rate?")
            while not_given_int:
                n_ratings = input("[Please insert number]").strip()
                try:
                    n_ratings = int(n_ratings)
                    not_given_int = False
                except:
                    not_given_int = True
            # Call rate books function
            rate_books(name, books, n_ratings)
    # Ask how many recommendations does the user want
    q = 'How many recommendations do you want?'
    # Default one is 10
    n_recommendations: int = 10
    # This error is not a reason to stop execution so it does not call print error message function
    try:
        n_recommendations = int(input(q + "\n"))
    except:
        print("I am sorry, I did not understand that.\nI will recommend 10 books.\n")
    # Write the response to the output file
    output_file.write("{} {}\n".format(q, n_recommendations))
    output_file.write("\n")
    output_file.close()
    # Apply similarity algorithm
    similar = calculate_similarity(ratings, name)
    # Recommend books
    recommend(books, ratings, ratings[name], similar, n_recommendations)
    # Terminate
    exit(0)
