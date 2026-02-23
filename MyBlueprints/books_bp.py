import os
from flask import Flask, request, jsonify, Blueprint
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

books_bp = Blueprint('books_bp', __name__)


@books_bp.route('/<category>', methods=['GET']) #127.0.0.1:5000/books/<category>
def get_books(category): # Själva funktionen för routen, kallar på 2 andra funktioner längre ner. 
    # Hämtar urln för den kategorin vi lagt in ovan. 
    try:
        category_url = get_category_url(category)

        # Liten felhantering, om den inte hittar en viss kategori
        if not category_url:
            return jsonify({"Error": "Hittade inte kategorin"}), 404
        
        # Hämtar värdena som returneras från funktionen "books_file"
        book_data, source = books_file(category, category_url)

        # returnerar värden som vi vill visa.
        return jsonify(
            {        
            "Kategori": category,
            "Source": source,
            "antal böcker": len(book_data),
            "böcker": book_data
            }
        ), 200
    except FileNotFoundError:
        return jsonify({
            "Error": "File Not Found"
        })


def get_category_url(category):
    # Hämtar URL från category_cache för en specifik kategori
    with open('category_cache.json', 'r') as category_file:
                category_data = json.load(category_file)
        # Loopar igenom varje dictionary i filen och kollar på nycklarna om det finns någon som stämmer med det vi lagt in och hämtar sedan urln.
    for cat in category_data:
        if cat['kategori'] == category:
            category_url= cat['url']
            return category_url


        

# Fixar en json fil med datetime och kategori, finns den redan, öppnar den upp den, annars skrapar den information och gör en ny
def books_file(category, category_url):
    dagens_datum = datetime.now().strftime("%Y%m%d")
    BOOK_CACHE_FILE = f"{category}_{dagens_datum}.json"

    if os.path.exists(BOOK_CACHE_FILE):
        with open(BOOK_CACHE_FILE, 'r', encoding="utf-8") as book_file:
            book_data = json.load(book_file)
            source = "Cachad fil"
    #om filen inte finns skrapar vi data från webbsidan och sparar det i cachefilen
    else:
        print("Ingen fil hittad. Skrapar data från bookstoscrape.com...")
        # Kallar på funktionen scrape_books och lägger in den url vi fått tidigare
        book_data = scrape_books(category_url)
        source = "Skrapad data från bookstoscrape.com"
        # sparar resultatet i cachefilen
        if book_data:
            with open(BOOK_CACHE_FILE, 'w', encoding='utf-8') as book_file:
                json.dump(book_data, book_file, ensure_ascii=False, indent=4)
    # returnerar all data från skrapningen eller från cache, samt source beroende på vart den hämtat ifrån.
    return book_data, source

def scrape_books(category_url):
    #user-agent lurar hemsidan eftersom vissa sidor kan blockera skript eftersom de ser ut som robotar
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    #skapar en lista med dicts där varje dict innehåller information om en bok
    books= []

    try:
        #request-get hämtar html-koden från URL'en
        response = requests.get(category_url, headers=headers, timeout=10)
        # La till denna kod för att se till att allt såg rätt ut på hemsidan med pund, detta kommer kanske inte behövas efter vi omvandlat till kronor
        response.encoding = 'utf-8' 
        #skapar soup-objekt för att kunna navigera i HTML-koden
        soup = BeautifulSoup(response.text, 'html.parser')
        books_divs = soup.select('.product_pod')
        for book in books_divs:
            title = book.h3.a['title']
            price = book.select_one('.price_color').get_text(strip=True)
            rating_class = book.select_one('.star-rating')['class']

            books.append({
                "titel": title,
                "pris": price,
                "betyg": rating_class[1] if len(rating_class) > 1 else "Inget betyg"
            })
    except Exception as e:
        print(f"Ett fel inträffade: {e}")
    # Returnerar listan med titel pris och betyg.
    return books

'''
def convert_currency():
    date = datetime.today().weekday()
    yesterdays_date = datetime.now().strftime("%Y-%m-%d")
    if date < 5:
        
    else:
        print('Weekend')
        '''
    

