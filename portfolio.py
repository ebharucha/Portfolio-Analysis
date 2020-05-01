###########################
# ebharucha, 1/5/2020
###########################

import json
from yahooquery import Ticker
import numpy as np
import pandas as pd

# Read portfolio configutation
with open('portfolio_cfg.json') as f:
    portfolio_cfg = json.load(f)

df_port_cfg = pd.DataFrame.from_dict(portfolio_cfg, orient='index', columns=['Quantity'])

# price = []
# value = []
# for stock, quantity in portfolio_cfg.items():
#     quote = Ticker(stock).price[stock]['regularMarketPrice']
#     price.append(quote)
#     value.append(f'{quote*quantity:.2f}')
    
df_port_cfg['Price'] = [Ticker(stock).price[stock]['regularMarketPrice'] for stock, quantity in portfolio_cfg.items()]
df_port_cfg['Value'] = [f'{p*q:.2f}' for p, q in zip(df_port_cfg.Price, portfolio_cfg.values())]
df_port_cfg['Value'] = df_port_cfg['Value'].astype(float)
total_value = df_port_cfg.Value.sum()
df_port_cfg['Portfolio %age'] = [f'{(val/total_value)*100:.2f}%' for val in df_port_cfg.Value]

df_port_cfg.to_csv('portfolio.csv')
print(df_port_cfg)
print (f'\nTotal value = ${total_value:,.2f}')