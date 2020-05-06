# Portfolio Analysis
Display portfolio information, market summary as specified in portfolio_cfg.json.
Display quote details for symbols specified on the command line

Usage:<br>
usage: python portfolio.py [-h] [-p] [-m] [-q Q]<br><br>

default(no arg): Print both portfolio & market details<br>
optional arguments:<br>
  -h, --help  show this help message and exit<br>
  -p, Print only portfolio details<br>
  -m, Print only market details<br>
  -q, list symbol(s) separated by commas & enclosed in quotes e.g. "AAPL, GOOG, AMZN"
