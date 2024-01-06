from flask import Flask, jsonify, make_response
from flask_cors import CORS
from library import Library, Collection

app = Flask(__name__)
CORS(app)
bib = Library()
collection = []

@app.route('/', methods=['GET'])
def index():
    return "welcome to my library"

@app.route('/allbooks', methods=['GET'])
def allBooks():
    if bib.allBooks() == []:
        response = make_response({"error": "No books found"}, 200)
    else:
        response = make_response(bib.serialize(), 200)
    return response
    
@app.route('/addbook/<string:title>/<string:author>/<int:isbn>/<string:genre>', methods=['GET', 'POST'])
def addBook(title, author, isbn, genre):
    exist = list(filter(lambda l: l.getISBN() == isbn, bib.allBooks()))
    if len(exist) !=0:
        return make_response({"error": "Ce livre existe déjà"}, 200)
    bib.addBook(title, author,isbn, genre)
    return make_response({"message": "Livre ajouté"}, 200)

@app.route('/getBookA/<string:author>', methods=['GET'])
def getBookA(author):
    books = bib.getBookByAuthor(author)
    if books == False:
        return make_response({"error": "No books found"}, 200)
    else:
        return make_response(jsonify(allbooks=[book.serialize() for book in books]), 200)

@app.route('/getBookG/<string:genre>', methods=['GET'])
def getBookG(genre):
    books = bib.getBookByGenre(genre)
    if books == False:
        return make_response({"error": "No books found"}, 200)
    else:
        return make_response(jsonify(allbooks=[book.serialize() for book in books]), 200)

@app.route('/getBookI/<string:isbn>', methods=['GET'])
def getBookI(isbn):
    books = bib.getBookByIsbn(isbn)
    if books == False:
        return make_response({"error": "No books found"}, 200)
    else:
        return make_response(jsonify(allbooks=[book.serialize() for book in books]), 200)

@app.route('/getBookC/<string:collection>', methods=['GET'])
def getBookC(collection):
    books = bib.getBookByCollection(collection)
    if books == False:
        return make_response({"error": "No books found"}, 200)
    else:
        return make_response(jsonify(allbooks=[book.serialize() for book in books]), 200)

def delBookFromCollectionOnly(isbn):
    hasdel = False
    for col in collection:
        res = col.delBook(isbn)
        if res:
            hasdel = True
    return hasdel

@app.route('/delbook/<int:isbn>', methods=['GET', 'DELETE'])
def delBook(isbn):
    book = bib.getBookByIsbn(isbn)
    if book == False:
        return make_response({"error": "Peut pas supprimer ce qui n'existe pas"}, 200)
    else:
        bib.delBook(isbn)
        col = delBookFromCollectionOnly(isbn)
        if col == True:
            return make_response({"message": "Livre supprimé de la bibliothèque"}, 200)
        else:
            return make_response({"error": "Impossible de supprimer"}, 200)

@app.route('/createCollection/<string:nom>', methods=['GET', 'POST'])
def createCollection(nom):
    exist = list(filter(lambda l: l.getName() == nom, collection))
    if len(exist) !=0:
        return make_response({"error": "collection déjà existante"}, 200) 
    else:
        collection.append(Collection(nom))
        return make_response({"message": "Collection créée"}, 200)
    
@app.route('/allcollections', methods=['GET'])
def allCollection():
    mycol = []
    for col in collection:
        mycol.append(col.getName())
    return make_response(jsonify(mycol), 200)
    
@app.route('/allbooksCollection/<string:nom>', methods=['GET'])
def allBooksCollection(nom):
    col = list(filter(lambda l: l.getName() == nom, collection))
    if len(col) == 0:
        response = make_response({"error": "Collection not found"}, 200)
    else:
        response = make_response(jsonify(allbooks=[book.serialize() for book in col[0].allBooks()]), 200)
        
    return response


@app.route('/addBookToCollection/<string:nom>/<int:isbn>', methods=['GET', 'POST'])
def addBookToCollection(nom, isbn):
    col = list(filter(lambda l: l.getName() == nom, collection))
    book = list(filter(lambda l: l.getISBN() == isbn, bib.allBooks()))
    if len(col) != 0:
        if len(book) != 0:
            # check if book is already in any collection trough all collections
            existsomewhere = False
            for coll in collection:
                if coll.getBook(isbn) != False:
                    existsomewhere = True
            if existsomewhere:
                return make_response({"error": "Livre déjà dans une collection"}, 200)
            else:
                added = col[0].addBook(book[0].getTitle(), book[0].getAuthor(), book[0].getISBN(), book[0].getGenre())
                if added:
                    book[0].setCollection(nom)
                    return make_response({"message": "Livre ajouté à la collection"}, 200) 
                else:
                    return make_response({"error": "N'a pas pu ajouter dans la collection"}, 200)
        else:
            
            return make_response({"error": "Livre non trouvé"}, 200)  
    else:
        return make_response({"error": "Collection not found"}, 200)
    
@app.route('/delBookFromCollection/<string:nom>/<int:isbn>', methods=['GET', 'DELETE'])
def delBookFromCollection(nom, isbn):
    col = list(filter(lambda l: l.getName() == nom, collection))
    if len(col) != 0:
        book = list(filter(lambda l: l.getISBN() == isbn, col[0].allBooks()))
        if len(book) != 0:
            deleted = col[0].delBook(isbn)
            if deleted:
               books = bib.getBookByIsbn(isbn)
               books[0].setCollection("")
               return make_response({"message": "Livre supprimé de la collection"}, 200)  
            else:
                return make_response({"error": "Livre non supprimé"}, 200)
        else:
            return make_response({"error": "Livre non trouvé dans la collection"}, 200)  
    else:
        return make_response({"error": "Collection not found"}, 200)
    
@app.route('/delCollection/<string:nom>', methods=['GET', 'DELETE'])
def delCollection(nom):
    col = list(filter(lambda l: l.getName() == nom, collection))
    if len(col) != 0:
        try: 
            for book in bib.allBooks():
                if book.getCollection() == nom:
                    book.setCollection("")
            collection.pop(collection.index(col[0]))
            return make_response({"message": "Collection supprimée"}, 200)
        except:
            return make_response({"error": "n'a pas pu supprimé la collectio,"}, 200)
    else:
        return make_response({"error": "Collection not found"}, 200)
 
if __name__ == "__main__":
    app.run()