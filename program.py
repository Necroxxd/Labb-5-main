import os
from flask import Flask, request, jsonify
import json
import requests
from bs4 import BeautifulSoup

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



#startar servern
if __name__ =='__main__':
    app.run(debug=True)