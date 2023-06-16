from flask import Flask, render_template, request, redirect
import pandas as pd
import plotly.graph_objects as go
from modules.data_collector import collect_data, get_market_cap

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/collect_data", methods=["POST"])
def handle_collect_data():
    symbol = request.form["symbol"]
    interval = request.form["interval"]
    collect_data(symbol, interval)
    return redirect(f"/chart/{symbol}_{interval}.csv")


@app.route("/chart/<filename>")
def show_chart(filename):
    df = pd.read_csv(filename)

    candlestick = go.Candlestick(
        x=df["Open time"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
    )

    candlestick_chart = go.Figure(data=[candlestick])
    candlestick_chart.update_layout(title=f"{filename[:-4]} Candlestick Chart")

    symbols = ["LUNA", "BAND", "XRP", "ANT", "BCH", "ADA", "DOT", "LINK", "DEXE", "MTL"]
    market_caps = get_market_cap(symbols)

    labels = [symbol for symbol, _ in market_caps]
    values = [cap for _, cap in market_caps]

    market_cap_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
    market_cap_chart.update_layout(title="Top 10 Market Capitalization")

    return render_template(
        "chart.html",
        candlestick_chart=candlestick_chart,
        market_cap_chart=market_cap_chart,
        show_home_button=True,
    )


if __name__ == "__main__":
    app.run()
