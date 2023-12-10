import numpy as np


def get_positions_and_order_book(e, inst_a, inst_b):
    return e.get_positions()[inst_a], e.get_positions()[inst_b], e.get_last_price_book(inst_a), e.get_last_price_book(inst_b)


def order_books_are_not_empty(order_book_a, order_book_b):
    return order_book_a.bids and order_book_a.asks and order_book_b.bids and order_book_b.asks


def print_new_trades(exchange, instrument_a, instrument_b):
        trades_a = exchange.poll_new_trades(instrument_a)
        trades_b = exchange.poll_new_trades(instrument_b)
        trades = trades_a + trades_b
        for t in trades:
            print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")


def unhedged(pos_a, pos_b, hedge_ratio):
    # Returns boolean value asserting whether hedge ratio still holds. Since rounding occurs, and infinite loops can happen in niche situations,
    # we have to be a bit lenient, which is fine as it is okay to not always be hedged perfectly. 
    return not(-pos_a == int(round(pos_b/hedge_ratio, 0)) or -pos_a + 1 == int(round(pos_b/hedge_ratio, 0)) or -pos_a - 1 == int(round(pos_b/hedge_ratio, 0)))

    
def try_hedge(e, pos_a, pos_b, order_book_a, instrument_a, hedge_ratio):
    # Calculate difference in terms of position A, which is always the smaller position.
    # This is a tad bit less precise, but allows for way easier prevention of limit breaches.
    delta = abs(pos_a + int(round(pos_b / hedge_ratio, 0)))
    if(delta): 
        if (hedge_ratio * pos_a + pos_b < 0):
            e.insert_order(instrument_a, price=order_book_a.asks[0].price, volume=delta, side='bid', order_type ='ioc')
        else:
            e.insert_order(instrument_a, price=order_book_a.bids[0].price, volume=delta, side='ask', order_type='ioc')
    else:
        print('NO DELTA')


class Pair:
    def __init__(self, name, inst_a, inst_b, const, slope, ratio, optimal_threshold):
        # Define pair class
        self.name = name
        self.instrument_a = inst_a
        self.instrument_b = inst_b
        self.constant = const
        self.gamma = slope
        self.hedge_ratio = ratio
        self.optimal_threshold = optimal_threshold

def get_tradeable_pairs_1200data():
    # Instantiate pair instances
    pair_adyen_kpn  = Pair(name='ADYEN_KPN',  inst_a='ADYEN',  inst_b='KPN',  const=-0.7573809565970522 , slope=1.2420757605342727,   ratio=1.6,  optimal_threshold= 0.0035)
    pair_adyen_tkwy = Pair(name='ADYEN_TKWY', inst_a='ADYEN',  inst_b='TKWY', const=0.7958558676955771 ,  slope=1.1083579545436058,   ratio=3.5,  optimal_threshold= 0.005)
    pair_kpn_tkwy   = Pair(name='KPN_TKWY',   inst_a='KPN',    inst_b='TKWY', const=1.4463379088181405 ,  slope=0.8339316378684012,   ratio=2.0,  optimal_threshold= 0.0072)
    return pair_adyen_kpn, pair_adyen_tkwy, pair_kpn_tkwy
        
def get_tradeable_pairs_10000data():
    # Instantiate pair instances
    pair_adyen_kpn  = Pair(name='ADYEN_KPN',  inst_a='ADYEN',  inst_b='KPN',  const=-0.6837659307875281 , slope=1.2240777878890614,   ratio=1.6,  optimal_threshold= 0.0026)
    pair_adyen_tkwy = Pair(name='ADYEN_TKWY', inst_a='ADYEN',  inst_b='TKWY', const=3.846962267590082 ,   slope=0.1949725708573791,   ratio=3.5,  optimal_threshold= 0.002)
    pair_kpn_tkwy   = Pair(name='KPN_TKWY',   inst_a='KPN',    inst_b='TKWY', const=3.716327538544213 ,  slope=0.15460993474008172,   ratio=2.0,  optimal_threshold= 0.0019)
    return pair_adyen_kpn, pair_adyen_tkwy, pair_kpn_tkwy
    
    
    