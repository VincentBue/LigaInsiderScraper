import schedule
import time
from scraper import update_data, get_date_string, Player

def scrape():
    print("Executing job at ", get_date_string())
    update_data()

schedule.every().day.at('00:05').do(scrape)

while True:
    schedule.run_pending()
    time.sleep(60)
