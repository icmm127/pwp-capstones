class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        a = "@" in address
        b = ".com" in address
        c = ".edu" in address
        d = ".org" in address
        if a and (b or c or d):
            self.email = address
            print("{}'s email has been updated.".format(self.name))
        else:
            print("Email address is invalid.")

    def __repr__(self):
        return "User {user_name}, email: {email_address}, books read: {book_no}".format(user_name=self.name, email_address=self.email, book_no=len(self.books))

    def __eq__(self, other_user):
        if (self.name == other_user.name) and (self.email == other_user.email):
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total_rating = 0
        for value in self.books.values():
            if value is not None:
                total_rating += value
        average_rating = (total_rating / len(self.books)) if len(self.books) != 0 else 0
        return average_rating

    def __hash__(self):
        return hash((self.name, self.email))


class Book:
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("{}'s ISBN has been updated.".format(self.title))

    def add_rating(self, rating):
        if rating is not None:
            if 0 <= rating <= 4:
                self.ratings.append(rating)
            else:
                print("Invalid Rating")

    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

    def get_average_rating(self):
        total_rating = 0
        for rating in self.ratings:
            total_rating += rating
        average_rating = total_rating / len(self.ratings)
        return average_rating

    def __repr__(self):
        return self.title + ", ISBN: " + str(self.isbn)

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)


class NonFiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)


class TomeRater:
    def __init__(self, name="We"):
        self.name = name
        self.users = {}
        self.books = {}
        self.isbn_list = []

    def create_book(self, title, isbn, price=0):
        if isbn in self.isbn_list:
            print("ISBN already exists.")
        else:
            book = Book(title, isbn, price)
            self.books[book] = 0
            self.isbn_list.append(isbn)
            return book

    def create_novel(self, title, author, isbn, price=0):
        if isbn in self.isbn_list:
            print("ISBN already exists.")
        else:
            novel = Fiction(title, author, isbn, price)
            self.books[novel] = 0
            self.isbn_list.append(isbn)
            return novel

    def create_non_fiction(self, title, subject, level, isbn, price=0):
        if isbn in self.isbn_list:
            print("ISBN already exists.")
        else:
            non_fiction = NonFiction(title, subject, level, isbn, price)
            self.books[non_fiction] = 0
            self.isbn_list.append(isbn)
            return non_fiction

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email, "No user with email {email}!".format(email=email))
        if type(user) == User:
            user.read_book(book, rating)
            book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print(user)

    def add_user(self, name, email, user_books=None):
        a = "@" in email
        b = ".com" in email
        c = ".edu" in email
        d = ".org" in email
        if a and (b or c or d):
            if email not in self.users:
                user = User(name, email)
                self.users[email] = user
                if user_books is not None:
                    for book in user_books:
                        self.add_book_to_user(book, email)
                return user
            else:
                print("User already exists.")
        else:
            print("Email address is invalid.")

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        highest = 0
        most_read_books = {}
        for times_read in self.books.values():
            if times_read > highest:
                highest = times_read
        for key, value in self.books.items():
            if value == highest:
                most_read_books[key] = value
        return most_read_books

    def highest_rated_book(self):
        highest_rating = 0
        books_and_rating = {}
        highest_rated_books = {}
        for book in self.books:
            books_and_rating[book] = book.get_average_rating()
        for rating in books_and_rating.values():
            if rating > highest_rating:
                highest_rating = rating
        for key, value in books_and_rating.items():
            if value == highest_rating:
                highest_rated_books[key] = value
        return highest_rated_books

    def most_positive_user(self):
        highest_rating = 0
        users_and_rating = {}
        most_positive_users = {}
        for user in self.users.values():
            users_and_rating[user] = user.get_average_rating()
        for rating in users_and_rating.values():
            if rating > highest_rating:
                highest_rating = rating
        for key, value in users_and_rating.items():
            if value == highest_rating:
                most_positive_users[key] = value
        return most_positive_users

    def get_n_most_read_books(self, n):
        books_sorted = sorted(self.books.items(), key=lambda x: x[1])
        books_descending = list(reversed(books_sorted))
        m = len(books_descending) if len(books_descending) < n else n
        return books_descending[:m]

    def get_n_most_prolific_readers(self, n):
        user_and_book_no = {}
        for user in self.users.values():
            user_and_book_no[user] = len(user.books)
        users_sorted = sorted(user_and_book_no.items(), key=lambda x: x[1])
        users_descending = list(reversed(users_sorted))
        m = len(users_descending) if len(users_descending) < n else n
        return users_descending[:m]

    def get_n_most_expensive_books(self, n):
        book_and_price = {}
        for book in self.books:
            book_and_price[book] = book.price
        price_sorted = sorted(book_and_price.items(), key=lambda x: x[1])
        price_descending = list(reversed(price_sorted))
        m = len(price_descending) if len(price_descending) < n else n
        return price_descending[:m]

    def get_worth_of_user(self, user_email):
        user = self.users.get(user_email, "No user with email {email}".format(email=user_email))
        if type(user) == User:
            worth = 0
            for book in user.books:
                worth += book.price
            return worth
        else:
            print(user)

    def __repr__(self):
        return "{name} have {no_of_user} users and a collection of {no_of_book} books!".format(name=self.name, no_of_user=len(self.users), no_of_book=len(self.books))

    def __eq__(self, other_tomerater):
        if (self.users == other_tomerater.users) and (self.books == other_tomerater.books):
            return True
        else:
            return False
