from flask import jsonify


class Book:
    def __init__(self, title, author, isbn, genre):
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__genre = genre
        self.__collection = ""
        

    def getTitle(self):
        return self.__title

    def getISBN(self):
        return int(self.__isbn)

    def getAuthor(self):
        return self.__author
    
    def getGenre(self):
        return self.__genre
    
    def getCollection(self):
        return self.__collection
    
    def setCollection(self, collection):
        self.__collection = collection

    def serialize(self):
        return {"title": self.__title, "author": self.__author, "isbn": self.__isbn, "genre": self.__genre, "collection": self.__collection}
    
class Collection:
    def __init__(self, nom):
        self.__books = []
        self.__nom = nom
    
    def getName(self):
        return self.__nom
        
    def addBook(self, title, author, isbn, genre):
        book = Book(title, author, isbn, genre)
        exist = self.getBook(isbn)
        if exist == False:
            book.setCollection(self.getName())
            self.__books.append(book)
            return True
        else: 
            return False
        
    def getBook(self, i):
        result = list(filter(lambda l: l.getISBN() == i, self.__books))
        if len(result) != 0:
            return result
        else:
            return False

    def allBooks(self):
        return self.__books

    def delBook(self, i):
        previous_size = len(self.__books)
        self.__books = list(filter(lambda l: not l.getISBN() == i, self.__books))
        new_size = len(self.__books)
        return not(new_size == previous_size)

    def serialize(self):
        return jsonify(books=[book.serialize() for book in self.__books])


class Library:
    def __init__(self):
        self.__books = []

    def addBook(self, title, author, isbn, genre):
        self.__books.append(Book(title, author, isbn, genre))

    def getBookByIsbn(self, i):
        result = list(filter(lambda l: l.getISBN() == i, self.__books))
        if len(result) != 0:
            return result
        else:
            return False
        
    def getBookByAuthor(self, i):
        result = list(filter(lambda l: l.getAuthor() == i, self.__books))
        if len(result) != 0:
            return result
        else:
            return False
        
    def getBookByGenre(self, i):
        result = list(filter(lambda l: l.getGenre() == i, self.__books))
        if len(result) != 0:
            return result
        else:
            return False
        
    def getBookByCollection(self, i):
        result = list(filter(lambda l: l.getCollection() == i, self.__books))
        if len(result) != 0:
            return result
        else:
            return False

    def allBooks(self):
        return self.__books

    def delBook(self, i):
        previous_size = len(self.__books)
        self.__books = list(filter(lambda l: not l.getISBN() == i, self.__books))
        new_size = len(self.__books)
        return not(new_size == previous_size)

    def serialize(self):
        return jsonify(books=[book.serialize() for book in self.__books])
