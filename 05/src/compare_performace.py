import argparse
import cProfile
import time
from memory_profiler import profile

from stock_types import (
    Industry, DividendPolicy, StockSimple, StockSlots, StockWeakref
)


class Timer:
    def __init__(self, description: str):
        self._description = description

    def __enter__(self):
        self._start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        total_time = str(round(end - self._start, 5))
        print(f"{self._description}: {total_time}")


def create_stock(cls, *args, **kwargs):
    return cls(*args, **kwargs)


def create_stock_list(n_obj, cls, *args, **kwargs):
    stocks = []
    for _ in range(n_obj):
        stocks.append(create_stock(cls, *args, **kwargs))
    return stocks


def get_attributes(stock):
    _ = stock.ticker
    _ = stock.price
    _ = stock.industry
    _ = stock.dividend_policy
    return stock


def get_attributes_list(stocks):
    for stock in stocks:
        _ = get_attributes(stock)
    return stocks


def change_attributes(stock, **kwargs):
    stock.ticker = kwargs['ticker']
    stock.price = kwargs['price']
    stock.industry = kwargs['industry']
    stock.dividend_policy = DividendPolicy(stock, kwargs['pay_dividends'])
    return stock


def change_attributes_list(stocks, **kwargs):
    for stock in stocks:
        _ = change_attributes(stock, **kwargs)
    return stocks


def delete_attributes(stock):
    del stock.ticker
    del stock.price
    del stock.industry
    del stock.dividend_policy
    return stock


def delete_attributes_list(stocks):
    for stock in stocks:
        _ = delete_attributes(stock)
    return stocks


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("N", type=int, action="store")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    N = args.N

    kw_params = {
        "ticker": "TKR1",
        "issuer": "OJSC TransCompany",
        "industry": Industry.Agricultural,
        "pay_dividends": True,
        "price": 127.89,
    }
    kw_params_change = {
        "ticker": "TKR2",
        "industry": Industry.IT,
        "pay_dividends": False,
        "price": 223.44,
    }

    msg = "Timeit"
    print(f"{msg:=^100}")

    for cls in [StockSimple, StockSlots, StockWeakref]:
        msg = f"|Class: {cls.__name__}|"
        print(f"{msg:=^100}")

        with Timer(f"Total time for call create_stocks {N} times"):
            stocks = create_stock_list(N, cls, **kw_params)
        with Timer(f"Total time for call get_attributes {N} times"):
            stocks = get_attributes_list(stocks)
        with Timer(f"Total time for call change_attributes {N} times"):
            stocks = change_attributes_list(stocks, **kw_params_change)
        with Timer(f"Total time for call delete_attributes {N} times"):
            stocks = delete_attributes_list(stocks)

    print("\n\n\n")

    msg = "Function call profiling"
    print(f"{msg:=^100}")

    for cls in [StockSimple, StockSlots, StockWeakref]:
        msg = f"|Class: {cls.__name__}|"
        print(f"{msg:=^100}")
        stocks = []
        profiler = cProfile.Profile()
        profiler.enable()

        for _ in range(N):
            stocks.append(create_stock(cls, **kw_params))
        for stock in stocks:
            _ = get_attributes(stock)
            _ = change_attributes(stock, **kw_params_change)
            _ = delete_attributes(stock)

        profiler.disable()
        profiler.print_stats()

    del stocks
    print("\n\n\n")

    msg = "Memory profiling"
    print(f"{msg:=^100}")

    create_stock_list = profile(create_stock_list)
    get_attributes_list = profile(get_attributes_list)
    change_attributes_list = profile(change_attributes_list)
    delete_attributes_list = profile(delete_attributes_list)

    for cls in [StockSimple, StockSlots, StockWeakref]:
        msg = f"|Class: {cls.__name__}|"
        print(f"{msg:=^100}")

        stocks = create_stock_list(N, cls, **kw_params)
        stocks = get_attributes_list(stocks)
        stocks = change_attributes_list(stocks, **kw_params_change)
        stocks = delete_attributes_list(stocks)
        del stocks
