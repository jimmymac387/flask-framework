from flask import Flask, render_template, request, redirect

app = Flask(__name__)

alpha_path = "https://www.alphavantage.co/query?"
function = "function=TIME_SERIES_INTRADAY"
symbol = "&symbol=IBM"
interval = "&interval=5min"
api_key = "&apikey=demo"

alpha_path + function + symbol + interval + api_key

app.vars = {}


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        app.vars["ticker"] = request.form["ticker"]
        app.vars["feature"] = request.form["feature"]
        print(app.vars["ticker"])
        return "Surprise!"


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(port=33507)
