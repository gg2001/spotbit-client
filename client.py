import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
import sys
from datetime import datetime, timedelta
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates

HOST = sys.argv[1]
if HOST == None:
    print("no host given")
    exit()

session = requests.session()
session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
result = session.get(f"http://{HOST}/configure")
raw_data = result.json()
print(f"available exchanges: {raw_data['exchanges']}")
exchanges = raw_data['exchanges']
selection = input("please type the name of an exchange here:")
if selection not in exchanges:
    print("not available!")
    exit()
print(f"available base currencies are: {raw_data['currencies']}")
currency = input("please type the name of a currency (not all exchanges support all currencies!):")
begin_raw = input("how many days of history do you want?:")
begin = None
end = int((datetime.now()).timestamp()*1e3)
try:
    begin = int((datetime.now() - timedelta(days=int(begin_raw))).timestamp()*1e3)
except Exception as e:
    print(e)
    print("invalid input.")
    exit()
result = session.get(f"http://{HOST}/hist/{currency}/{selection}/{begin}/{end}")
raw_data = result.json()
df = pd.DataFrame(raw_data['data'], columns=list(dict.fromkeys(raw_data['columns'])))
ohlc = df.loc[:, ['datetime', 'open', 'high', 'low', 'close']]
ohlc['datetime'] = pd.to_datetime(ohlc['datetime'])
ohlc['datetime'] = ohlc['datetime'].apply(mpl_dates.date2num)
ohlc = ohlc.astype(float)
fig, ax = plt.subplots()

candlestick_ohlc(ax, ohlc.values, width=0.0001, colorup='green', colordown='red', alpha=0.9)

# Setting labels & titles
ax.set_xlabel('Date')
ax.set_ylabel('Price')
fig.suptitle(f"{selection}")

# Formatting Date
date_format = mpl_dates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

fig.tight_layout()

plt.show()
'''
ax = plt.gca()
df.to_csv("test.csv")
df.plot(kind='line', x='datetime', y='open', color='blue', ax=ax)
df.plot(kind='line', x='datetime', y='high', color='green', ax=ax)
df.plot(kind='line', x='datetime', y='low', color='red', ax=ax)
df.plot(kind='line', x='datetime', y='close', color='black', ax=ax)
plt.title(selection)
plt.show()
'''
