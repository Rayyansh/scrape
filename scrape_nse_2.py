import requests
import json

import pandas as pd


class OptionChain:

    def __init__(self, symbol, expiry_date):
        self.symbol = symbol
        self.expiry_date = expiry_date
        self.url = f'https://www.nseindia.com/api/option-chain-indices?symbol={self.symbol}'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.records = None
        self.calls = None
        self.puts = None

    def get_option_chain(self):
        response = requests.get(self.url, headers=self.headers)
        data = json.loads(response.text)
        self.records = data['records']['data']

    def filter_by_expiry(self):
        self.calls = pd.DataFrame([record['CE'] for record in self.records if record['expiryDate'] == self.expiry_date])  # using list comprehensive
        self.puts = pd.DataFrame([record['PE'] for record in self.records if record['expiryDate'] == self.expiry_date])  # using list comprehensive
        print(self.calls, self.puts)

    def export_to_excel(self):
        call_file = f'{self.symbol}_{self.expiry_date}_calls.csv'
        self.calls.to_csv(call_file, index=False)
        print(f"Call option data for {self.symbol} expiring on {self.expiry_date} has been exported to {call_file}.")

        put_file = f'{self.symbol}_{self.expiry_date}_puts.csv'
        self.puts.to_csv(put_file, index=False)
        print(f"Put option data for {self.symbol} expiring on {self.expiry_date} has been exported to {put_file}.")


if __name__ == '__main__':
    symbol = 'BANKNIFTY'
    expiry_date = '06-Apr-2023'

    oc = OptionChain(symbol, expiry_date)
    oc.get_option_chain()
    oc.filter_by_expiry()
    oc.export_to_excel()