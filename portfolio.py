################################################################################################################################
# ebharucha, 1/5/2020, 4/5/2020, 6/5/2020
################################################################################################################################

import argparse
import json
from yahooquery import Ticker
import pandas as pd

def read_config():
    # Read portfolio configutation
    try:   
        with open('per_portfolio_cfg.json') as f:
            config = json.load(f)
    except:
        with open('portfolio_cfg.json') as f:
            config = json.load(f)
    return (config)

def portfolio_summary(portfolio_cfg):
    print ('=========Portfolio=========')
    df_port_cfg = pd.DataFrame.from_dict(portfolio_cfg, orient='index', columns=['Quantity'])
    df_port_cfg['Price'] = [Ticker(stock).price[stock]['regularMarketPrice'] for stock, quantity in portfolio_cfg.items()]
    df_port_cfg['Value'] = [f'{p*q:.2f}' for p, q in zip(df_port_cfg.Price, portfolio_cfg.values())]
    df_port_cfg['Value'] = df_port_cfg['Value'].astype(float)
    total_value = df_port_cfg.Value.sum()
    df_port_cfg['Portfolio %age'] = [f'{(val/total_value)*100:.2f}%' for val in df_port_cfg.Value]

    df_port_cfg.to_csv('portfolio.csv')
    print(df_port_cfg)
    print(f'\nTotal value = ${total_value:,.2f}\n')

def get_info(symbol):
    price = f'{Ticker(symbol).price[symbol]["regularMarketPrice"]:.2f}'
    change = f'{Ticker(symbol).price[symbol]["regularMarketChange"]:.2f}'
    per_change = f'{Ticker(symbol).price[symbol]["regularMarketChangePercent"]:.2f}'
    return (symbol, price, change, per_change)

def market_summary(market_config):
    print ('=========Markets=========')
    for m, s in market_config.items():
        (symbol, price, change, per_change) = get_info(s)
        print(f'{m} => Price={price}, Change={change}, %age change={per_change}%')
        
def get_quotes(symbols):
    symbols = symbols.split(',')
    for s in symbols:
        s = s.strip()
        (symbol, price, change, per_change) = get_info(s)
        print(f'{symbol} => Price={price}, Change={change}, %age change={per_change}%')

if __name__ == "__main__":
    config = read_config()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action='store_true')
    parser.add_argument("-m", action='store_true')
    parser.add_argument("-q", help='list symbol(s) separated by commas & enclosed in quotes\
        e.g. "AAPL, GOOG, AMZN" ')
    args = parser.parse_args()
    symbols = args.q
    if (args.p == True):
        portfolio_summary(config["Portfolio"])
    elif (args.m == True):
        market_summary(config["Markets"])
    elif (args.q != None):
        get_quotes(symbols)
    else:
        portfolio_summary(config["Portfolio"])
        market_summary(config["Markets"])