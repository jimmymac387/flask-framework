# import simplejson as json
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show

alpha_path = "https://www.alphavantage.co/query?"
function = "function=TIME_SERIES_INTRADAY"
symbol = "&symbol=" + "GOOG"
interval = "&interval=5min"
api_key = "&apikey=FBSJ78DDZA5GWDKW"

api_request = alpha_path + function + symbol + interval + api_key

data = pd.read_json(api_request)[6:]
# t = [v for k, v in (t for t in data["Time Series (5min)"].items() for i in data.items())]
# [row for row in data["Time Series (5min)"]][0]

data

# From the internet -----------------------------------------------------------
# d = {'O1': [{'K1': 1}, {'K2': 2}, {'K3': 3}],
#      'O2': [{'K1': 4}, {'K2': 5}, {'K3': 6}]}
# d.items()
# pd.DataFrame.from_dict(d)
#
# d2 = {k: {k: v for d in L for k, v in d.items()} for k, L in d.items()}
# pd.DataFrame.from_dict(d2)
# -----------------------------------------------------------------------------

data2 = data["Time Series (5min)"].apply(pd.Series)
data3 = data2.rename(columns={col: col[3:] for col in data2.columns})

data3.head()

p = figure(x_axis_type="datetime")

# data.index
p.line(
    x=pd.to_datetime(data3.index),
    y=data3["open"],
    line_width=1,
    color="green"
)
# data["open"]

show(p)
data.head()
