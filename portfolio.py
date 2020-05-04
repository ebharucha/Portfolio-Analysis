################################################################################################################################
# ebharucha, 1/5/2020, 4/5/2020
################################################################################################################################

import argparse
import json
from yahooquery import Ticker
import numpy as np
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

def market_summary(market_config):
    print ('=========Markets=========')
    for m, s in market_config.items():
        print(f'{m} => Price={Ticker(s).price[s]["regularMarketPrice"]}, Change={Ticker(s).price[s]["regularMarketChange"]:.2f}, \
%age change={Ticker(s).price[s]["regularMarketChangePercent"]:.2f}%')
        
if __name__ == "__main__":
    config = read_config()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action='store_true')
    parser.add_argument("-m", action='store_true')
    args = parser.parse_args()
    if (args.p == True):
        portfolio_summary(config["Portfolio"])
    elif (args.m == True):
        market_summary(config["Markets"])
    else:
        portfolio_summary(config["Portfolio"])
        market_summary(config["Markets"])