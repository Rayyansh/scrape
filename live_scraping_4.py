import requests
from bs4 import BeautifulSoup
import threading
import time


class BitcoinPriceScraper:
    def __init__(self, url):
        self.url = url
        self.price = None
        self._stop_event = threading.Event()

    def start(self):
        self._thread = threading.Thread(target=self._fetch_price)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _fetch_price(self):
        while not self._stop_event.is_set():
            try:
                response = requests.get(self.url)
                soup = BeautifulSoup(response.content, 'html.parser')
                self.price = soup.find('span', {'data-test': 'instrument-price-last'}).text
            except:
                print('Failed to fetch price')
            time.sleep(5)


if __name__ == '__main__':
    url = 'https://www.investing.com/crypto/bitcoin/btc-usd?cid=1035793'
    scraper = BitcoinPriceScraper(url)
    scraper.start()

    while True:
        if scraper.price:
            print(f'Live Bitcoin Price: {scraper.price}')
        time.sleep(5)