import weakref
from enum import Enum


Industry = Enum(
    'Industry',
    [
        'Mining',
        'Manufacturing',
        'Agricultural',
        'Financial',
        'Logistics',
        'Communication',
        'IT',
        'Retail'
    ]
)


class DividendPolicy:
    def __init__(self, stock, pay: bool):
        self.policy = "We pay dividends." if pay else "We don't pay dividends."
        self.stock = stock


class DividendPolicyWeakref:
    def __init__(self, stock, pay: bool):
        self.policy = "We pay dividends." if pay else "We don't pay dividends."
        self.stock = weakref.ref(stock)


class StockSimple:
    def __init__(self, ticker: str, issuer: str, industry: Industry,
                 pay_dividends: bool, price: float):
        self.ticker = ticker
        self.issuer = issuer
        self.industry = industry
        self.dividend_policy = DividendPolicy(self, pay_dividends)
        self.price = price


class StockSlots:
    __slots__ = ("ticker", "issuer", "industry", "dividend_policy", "price")

    def __init__(self, ticker: str, issuer: str, industry: Industry,
                 pay_dividends: bool, price: float):
        self.ticker = ticker
        self.issuer = issuer
        self.industry = industry
        self.dividend_policy = DividendPolicy(self, pay_dividends)
        self.price = price


class StockWeakref:
    def __init__(self, ticker: str, issuer: str, industry: Industry,
                 pay_dividends: bool, price: float):
        self.ticker = ticker
        self.issuer = issuer
        self.industry = industry
        self.dividend_policy = DividendPolicyWeakref(self, pay_dividends)
        self.price = price
