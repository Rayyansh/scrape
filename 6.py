import time
import random
import threading

class TradingBot:
    def __init__(self, symbol, entry_time, price):
        # check that the entry time is in the future
        if entry_time <= time.time():
            raise ValueError("Entry time must be in the future.")
        self.symbol = symbol
        self.entry_time = entry_time
        self.price = price
        self.order_placed = False

    def place_order(self):
        current_time = time.time()
        if current_time >= self.entry_time and not self.order_placed:
            # place the order
            print(f"Order placed for {self.symbol} at {self.price} at {time.ctime(current_time)}")
            self.order_placed = True
            return True
        return False

# create 5 trading bot objects with different entry times and prices
bots = [
    TradingBot("AAPL", time.time() + 5, 145.0),
    TradingBot("MSFT", time.time() + 10, 240.0),
    TradingBot("GOOG", time.time() + 15, 2000.0),
    TradingBot("AMZN", time.time() + 20, 3000.0),
    TradingBot("FB", time.time() + 25, 350.0),
]

def run_trading_bots(bots):
    # loop until all orders have been placed
    while not all(bot.order_placed for bot in bots):
        # place orders for all bots whose entry time has passed
        for bot in bots:
            bot.place_order()
        # sleep for a random interval to simulate delay between orders
        time.sleep(random.uniform(0.5, 1))

# run the trading bots using threading
threads = [threading.Thread(target=run_trading_bots, args=(bots,)) for _ in range(5)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
