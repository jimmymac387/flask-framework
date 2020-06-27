from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_file, show
import pandas as pd

app = Flask(__name__)

app.vars = {}


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/blank', methods=["GET", "POST"])
def blank():
    app.vars["ticker"] = request.form["ticker"]
    app.vars["features"] = request.form["features"]
    # print(app.vars["ticker"])
    alpha_path = "https://www.alphavantage.co/query?"
    function = "function=TIME_SERIES_INTRADAY"
    symbol = "&symbol=" + app.vars["ticker"]
    interval = "&interval=5min"
    api_key = "&apikey=FBSJ78DDZA5GWDKW"

    api_request = alpha_path + function + symbol + interval + api_key

    data = pd.read_json(api_request)[6:]

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
    return show(p)
    # render_template('about.html')


# @app.route('/about')
# def about():
#     return render_template('about.html')


if __name__ == '__main__':
    app.run(port=33507)
