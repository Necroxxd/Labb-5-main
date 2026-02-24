from datetime import datetime,  timedelta

    
date = datetime.today() - timedelta(days=1) # TA BORT TIMEDELTA HÄR BARA FÖR TESTNING
earlier_dates = date
#.weekday används för att sätta ett "värde" mellan 1-6 på ett datum. Är värdet 5 eller 6 = helg, annars veckodag. 
date = date.weekday()
count = 1

    #helg
while date > 4:
    # Använder count för att kunna subtrahera dagar, är det söndag kommer loopen gå 2 gånger och få fredagens datum. Lördag loopar 1 gång och får också fredagens datum.
    count += 1
    earlier_dates = datetime.today() - timedelta(days=count) # .strftime("%Y-%m-%d")
    date = earlier_dates.weekday()
else:
    latest_working_date = earlier_dates.strftime("%Y-%m-%d")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    url = f"https://www.riksbank.se/sv/statistik/rantor-och-valutakurser/sok-rantor-och-valutakurser/?s=g130-SEKGBPPMI&a=D&from={latest_working_date}&to={latest_working_date}&fs=3#result-section"

print(url)