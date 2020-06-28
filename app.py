import datetime
import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.resources import CDN
from bokeh.embed import file_html
from flask import Flask, render_template, request


app = Flask(__name__)


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

    df["date"] = pd.to_datetime(df.index)
    dft = df[["date", feature]]
    # numlines = len(dft.columns - 1)
    source = ColumnDataSource(dft)
    p = figure(x_axis_type="datetime")
    p.line(source=source, x="date", y=feature)
    p.title.text = "Daily Stock Price"
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = feature
    return p


def make_html(plot):
    html = file_html(plot, CDN, "myplot")
    f = open("./templates/output.html", "w")
    f.write(html)
    f.close()


@app.route('/')
def index():
    return render_template('input.html')


@app.route('/output', methods=["POST"])
def output():
    symbol = request.form["ticker"]
    feature = request.form["features"]
    result_plot = get_plot(symbol, feature)
    make_html(result_plot)
    return render_template('output.html')
    # script, div = components(result_plot)
    # return render_template("output.html", script=script, div=div)


if __name__ == '__main__':
    app.run(port=33507)
