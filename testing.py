import datetime
import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components
from bokeh.palettes import Spectral11
# from flask import Flask, render_template, request


def get_plot(symbol, feature):
    # symbol = "GOOG"
    # feature = "close"
    alpha_path = "https://www.alphavantage.co/query?"
    function = "function=TIME_SERIES_DAILY_ADJUSTED"
    symbol = "&symbol=" + symbol
    size = "&outputsize=full&datatype=json"
    api_key = "&apikey=FBSJ78DDZA5GWDKW"
    api_request = alpha_path + function + symbol + size + api_key

    r = requests.get(api_request)
    response = r.json()

    data = pd.DataFrame.from_dict(
        response["Time Series (Daily)"],
        orient="index"
    )

    data = data.sort_index(axis=1)
    data = data.rename(columns={col: col[3:] for col in data.columns})

    df = data.astype({
        'open': 'float',
        'high': 'float',
        'low': 'float',
        'close': 'float',
        'adjusted close': 'float',
        'volume': 'int32'
    })

    feature = ["open", "close"]
    features = [f for f in feature]
    features.append("date")
    fcol = features

    # date = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dft.index]
    # df["date"] = date
    df["date"] = pd.to_datetime(df.index)
    dft = df[["date", feature]]
    dft = df[fcol]
    numlines = len(dft.columns) - 1
    mypalette = Spectral11[0:numlines]

    p.multi_line(
        xs=[pd.to_datetime(dft.index.values)] * numlines,
        ys=[dft[name].values for name in dft.drop(columns="date")],
        line_color=mypalette,
        line_width=5
    )
    source = ColumnDataSource(dft)
    p = figure(x_axis_type="datetime")
    p.line(source=source, x="date", y=feature)
    p.title.text = "Daily Stock Price"
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Price"
    show(p)
    return p


get_plot("GOOG", "open")
result_plot = get_plot("GOOG", "open")
# components(result_plot)
html = file_html(result_plot, CDN, "myplot")
f = open("./templates/output.html", "w")
f.write(html)
f.close()
