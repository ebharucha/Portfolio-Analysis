################################################################################################################################
# ebharucha: 1/5/2020, 4/5/2020, 6/5/2020, 6/6/2020
################################################################################################################################

import argparse
import json
from yahooquery import Ticker     # Use the yahooquery api wrapper (https://pypi.org/project/yahooquery/)
import pandas as pd

# Function to read portfolio configutation
def read_config():
    try:   
        with open('./portfolio_personal_cfg.json') as f:
            config = json.load(f)
    except:
        with open('./portfolio_public_cfg.json') as f:
            config = json.load(f)
    return (config)

# Function to output basic quote details for supplied symbol 
def get_info(symbol):
    price = f'{Ticker(symbol).price[symbol]["regularMarketPrice"]:.2f}'
    change = f'{Ticker(symbol).price[symbol]["regularMarketChange"]:.2f}'
    per_change = f'{Ticker(symbol).price[symbol]["regularMarketChangePercent"]:.2f}'
    return (symbol, price, change, per_change)

# Function to out portfolio summary
def portfolio_summary(portfolio_cfg, flag):
    print ('=========Portfolio=========')
    df_port_cfg = pd.DataFrame.from_dict(portfolio_cfg, orient='index', columns=['Quantity'])
    df_port_cfg['Price'] = [Ticker(stock).price[stock]['regularMarketPrice'] for stock, quantity in portfolio_cfg.items()]
    df_port_cfg['%age change'] = [f'{Ticker(stock).price[stock]["regularMarketChangePercent"]:.2f}%' for stock, quantity in portfolio_cfg.items()]
    df_port_cfg = df_port_cfg.round(2)
    df_port_cfg['Value'] = [f'{p*q:.2f}' for p, q in zip(df_port_cfg.Price, portfolio_cfg.values())]
    df_port_cfg['Value'] = df_port_cfg['Value'].astype(float)
    total_value = df_port_cfg.Value.sum()
    df_port_cfg['Portfolio %age'] = [f'{(val/total_value)*100:.2f}%' for val in df_port_cfg.Value]
    
    if (flag == 'personal'):
        df_port_cfg.to_csv('./portfolio_personal.csv')
    else:
        df_port_cfg.to_csv('portfolio_public.csv')
    print(df_port_cfg)
    print(f'\nTotal value = ${total_value:,.2f}\n')

# Function to output market summary
def market_summary(market_config):
    print ('=========Markets=========')
    for m, s in market_config.items():
        (symbol, price, change, per_change) = get_info(s)
        print(f'{m} => Price={price}, Change={change}, %age change={per_change}%')

# Function to get quote details for supplied symbol(s) 
def get_quotes(symbols):
    symbols = symbols.split(',')
    for s in symbols:
        s = s.strip()
        (symbol, price, change, per_change) = get_info(s)
        print(f'{symbol} => Price={price}, Change={change}, %age change={per_change}%')

# Main function
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
        portfolio_summary(config["Portfolio"], config["Flag"])
    elif (args.m == True):
        market_summary(config["Markets"])
    elif (args.q != None):
        get_quotes(symbols)
    else:
        portfolio_summary(config["Portfolio"], config["Flag"])
        market_summary(config["Markets"])