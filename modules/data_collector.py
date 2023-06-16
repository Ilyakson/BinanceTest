import os

import pandas as pd
import psycopg2
import requests


def collect_data(symbol, interval):
    try:
        csv_file = f"{symbol}_{interval}.csv"
        if os.path.exists(csv_file):
            print(f"Data file '{csv_file}' already exists. Skipping data collection.")
            return

        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
        response = requests.get(url)
        data = response.json()

        df = pd.DataFrame(data)
        df = df.iloc[:, :6]
        df.columns = ["Open time", "Open", "High", "Low", "Close", "Volume"]
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")

        df.to_csv(csv_file, index=False)

        print("Data saved successfully.")

        conn = psycopg2.connect(
            host="YOUR_HOST",
            port="YOUR_PORT",
            database="YOUR_NAME_DB",
            user="YOUR_USER",
            password="YOUR_PASSWORD",
        )

        cur = conn.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS candles (open_time TIMESTAMP, open NUMERIC, high NUMERIC, low NUMERIC, close NUMERIC, volume NUMERIC, csv_file TEXT)"
        )
        conn.commit()

        candles = []
        for _, row in df.iterrows():
            open_time = row["Open time"].strftime("%Y-%m-%d %H:%M:%S")
            open_price = row["Open"]
            high_price = row["High"]
            low_price = row["Low"]
            close_price = row["Close"]
            volume = row["Volume"]
            candles.append(
                (
                    open_time,
                    open_price,
                    high_price,
                    low_price,
                    close_price,
                    volume,
                    csv_file,
                )
            )

        cur.executemany(
            "INSERT INTO candles (open_time, open, high, low, close, volume, csv_file) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            candles,
        )
        conn.commit()

        cur.close()
        conn.close()

        print("Data saved successfully in the PostgreSQL database.")
    except requests.exceptions.RequestException as e:
        print("Error while making a request to the Binance API:", e)
    except ValueError as e:
        print("Error while processing data:", e)


def get_market_cap(symbols):
    market_caps = []

    for symbol in symbols:
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
            response = requests.get(url)
            data = response.json()
            market_cap = float(data["quoteVolume"]) * float(data["weightedAvgPrice"])
            market_caps.append((symbol, market_cap))
        except requests.exceptions.RequestException as e:
            print("Error while making a request to the Binance API:", e)
        except (KeyError, ValueError) as e:
            print("Error while processing data:", e)

    return market_caps
