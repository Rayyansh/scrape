import pandas as pd
import requests

class BTCUSDDataset:
    def __init__(self, start_date='2021-01-01', end_date='2023-3-31'):
        self.start_date = pd.Timestamp(start_date, tz='UTC')
        self.end_date = pd.Timestamp(end_date, tz='UTC')
        self.interval = '15'
        self.category = 'inverse'
        self.symbol = 'BTCUSD'
        self.data = None

    def fetch_data(self):
        # Define the API endpoint and parameters
        endpoint = 'https://api.bybit.com/v5/market/kline'

        print(self.start_date.timestamp(), self.end_date.timestamp())
        params = {
            'category':f'{self.category}',
            'symbol': 'BTCUSD',
            'interval': f'{self.interval}',
            'start': int(self.start_date.timestamp()),
            # 'end': int(self.end_date.timestamp())
        }

        # Send a GET request to the API endpoint
        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        # Convert the response data to a pandas DataFrame
        data = response.json()['result']['list']
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume','turnover'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], origin='unix' ,unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
        df.set_index('timestamp', inplace=True)

        self.data = df

    def get_data(self):
        if self.data is None:
            self.fetch_data()
        return self.data


if __name__ == '__main__':
    kline_api = BTCUSDDataset()
    print(kline_api.get_data())

# dataset = BTCUSDDataset(start_date='2021-01-01', end_date='2022-12-31')
# df = dataset.get_data()
# print(df)