import threading
import pandas as pd
import requests
from datetime import datetime, timedelta


class CryptoDataThread(threading.Thread):
    def __init__(self, symbol):
        threading.Thread.__init__(self)
        self.symbol = symbol

    def run(self):
        data = self.get_data()
        self.df = self.convert_to_dataframe(data)

    def get_data(self):
        start_time = int((datetime(2021, 1, 1) - datetime(1970, 1, 1)).total_seconds())
        end_time = int((datetime(2022, 12, 31) - datetime(1970, 1, 1)).total_seconds())
        url = f"https://api.bybit.com/v2/public/kline/list?symbol={self.symbol}&interval=15&from={start_time}&to={end_time}"
        response = requests.get(url)
        data = response.json()['result']
        return data

    def convert_to_dataframe(self, data):
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
        df = df.set_index('timestamp')
        return df


def main():
    symbols = ['BTCUSD', 'ETHUSD', 'BITUSD', 'SOLUSD', 'XRPUSD']
    threads = []
    for symbol in symbols:
        thread = CryptoDataThread(symbol)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    dataframes = [thread.df for thread in threads]
    result_df = pd.concat(dataframes, keys=symbols, names=['symbol', 'timestamp'])
    print(result_df)


if __name__ == '__main__':
    main()