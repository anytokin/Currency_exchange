from itertools import permutations

supported_currencies = ['EUR', 'USD', 'JPY', 'PLN']
''' I think that is better to keep rates for both ways
e.g. PLN to USD and USD to PLN - cost of "duplicated"
records in db are negligible, rounding errors not so much'''
supported_currencies_pairs = set(pair for pair in permutations(supported_currencies, 2) if len(set(pair)) != 1)
