import os
from flask import Blueprint, jsonify, render_template
from bs4 import BeautifulSoup
import json
import requests

category_bp = Blueprint('category_bp', __name__)
CATEGORY_CACHE_FILE = 'category_cache.json'


@category_bp.route('/', methods=['Get']) #/categories
def get_categories():
    #kontrollerar om data finns i cachefilen
    if os.path.exists(CATEGORY_CACHE_FILE):
        with open(CATEGORY_CACHE_FILE, 'r') as category_file:
            category_data = json.load(category_file)
            source = "Cachad fil"
    #om filen inte finns skrapar vi data från webbsidan och sparar det i cachefilen
    else:
        print("Ingen fil hittad, skrapar data från bookstoscrape.com...")
        category_data = scrape_categories()
        source = "Skrapad data från bookstoscrape.com"
        #sparar resultatet i cachefilen
        if category_data:
            with open(CATEGORY_CACHE_FILE, 'w') as category_file:
                json.dump(category_data, category_file, ensure_ascii=False, indent=4)
    #returnerar resultat som JSON till webbläsaren
    return jsonify({
        "webbsida": "Books to Scrape",
        "källa": source,
        "antal kategorier": len(category_data),
        "kategorier": category_data
    })

@category_bp.route('/ui', methods=['GET']) #/categories/ui
def category_view():
    if os.path.exists(CATEGORY_CACHE_FILE):
        with open(CATEGORY_CACHE_FILE, 'r') as category_file:
            category_data = json.load(category_file)
            source = "Cachad fil"
    else:
        data = scrape_categories()
        source = "Skrapad data från bookstoscrape.com"
        if data:
            with open(CATEGORY_CACHE_FILE, 'w') as category_file:
                json.dump(data, category_file, ensure_ascii=False, indent=4)
    return render_template('categories.html', categories=category_data, source=source)

#skrapningsfunktion som hämtar kategorier från bookstoscrape.com
def scrape_categories():
    url= "https://books.toscrape.com"
    #lurar hemsidan eftersom vissa sidor kan blockera skript eftersom de ser ut som robotar
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    #skapar en lista med dicst där varje dict innehåller kategorier
    categories=[]

    try:
        #requests.get hämtar html-koden från URL'en
        response= requests.get(url, headers=headers, timeout=10)
        #skapar soup-objekt för att kunna navigera i HTML-koden
        soup = BeautifulSoup(response.text, 'html.parser')
        #letar efter alla div med klassen side_categories
        #side_categories = soup.find_all('div', class_='side_categories ul li ul li')
        side_categories = soup.select('.side_categories ul li ul li a')

        for category in side_categories:
            category_name = category.get_text(strip=True)
            category_name = category_name.replace(" ", "-")
            #.get href hämtar själva länkadressen från a-taggen
            relative_link = category.get('href')
            #klistrar ihop den relativa länken med bas-länken för att få en "full_link"
            full_link= f"https://books.toscrape.com/{relative_link}" #if relative_link.startswith('/') else relative_link
            #lägger till kategorin och dess länk i listan "categories"
            categories.append({
                "kategori": category_name,
                "url": full_link
            })
    except Exception as e:
        print(f"Ett fel uppstod vid skrapning: {e}")
    #returnerar listan med kategorier och url:er
    return categories
