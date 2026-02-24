from flask import Flask, request, jsonify
import json
from datetime import datetime

#importerar blueprints
from MyBlueprints.category_bp import category_bp
from MyBlueprints.books_bp import books_bp

#skapar instans av Flask
app = Flask(__name__)
app.json.ensure_ascii = False

#registrering av blueprints
app.register_blueprint(category_bp, url_prefix='/categories') #127.0.0.1:5000/categories/
app.register_blueprint(books_bp, url_prefix='/books') #127.0.0.1:5000/books/

@app.route('/')
def home():
    return "Hello from flask!"

#uppdatera bok
@app.route('/books/<category>/<int:id>', methods=['PUT']) #http://127.0.0.1:5000/books/<category>/id
def editbook(category, id):
    file = f"{category}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(file, 'r', encoding="utf-8") as book_file:
        books = json.load(book_file)
    #hämtar uppdaterade boken från requesten
    edited_book = request.get_json()
    #hittar boken i listan och uppdaterar den
    for book in books:
        if book['id'] == id:
            book.update(edited_book)
            break
    #sparar den uppdaterade listan i filen
    with open(file, 'w', encoding='utf-8') as book_file:
        json.dump(books, book_file, ensure_ascii=False, indent=4)
    return jsonify({"message": "Boken har uppdaterats"})

#ta bort bok
@app.route('/books/<category>/<int:id>', methods=['DELETE']) #http://127.0.0.1:5000/books/<category>/id
def deletebook(category, id):
    file = f"{category}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(file, 'r', encoding="utf-8") as book_file:
        books = json.load(book_file)
    #hittar boken i listan och tar bort den
    for book in books:
        if book['id'] == id:
            books.remove(book)
            break
    #sparar den uppdaterade listan i filen
    with open(file, 'w', encoding='utf-8') as book_file:
        json.dump(books, book_file, ensure_ascii=False, indent=4)
    return jsonify({"message": "Boken har tagits bort"})

#lägg till bok
@app.route('/books/<category>', methods=['POST']) #http://127.0.0.1:5000/books/<category>
def addbook(category):
    file = f"{category}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(file, 'r', encoding="utf-8") as book_file:
        books = json.load(book_file)
    #hämtar nya boken från requesten och lägger till den i listan med append
    new_book = request.get_json()
    books.append(new_book)
    #sparar den uppdaterade listan i filen
    with open(file, 'w', encoding='utf-8') as book_file:
        json.dump(books, book_file, ensure_ascii=False, indent=4)
    return jsonify({"message": "Boken har lagts till i kategorin"})

#startar servern
if __name__ =='__main__':
    app.run(debug=True)