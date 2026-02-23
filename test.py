from datetime import datetime, date

test_date = date.weekday(date(2026, 2, 20))
todays_date = datetime.now().strftime("%Y-%m-%d")

if test_date < 5:
    print('Weekday')
else:
    print('Weekend')
    

