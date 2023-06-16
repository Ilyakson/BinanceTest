# Data Collection Project
The Data Collection project is a web application for collecting financial quote data and market capitalization information.

## Installation
```
git clone https://github.com/Ilyakson/BinanceTest.git
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

## PostgreSQL Database Setup
1. Install PostgreSQL on your computer if you haven't already. You can download and install PostgreSQL from the official website.
2. Create a new database in PostgreSQL. You can use a command-line interface such as psql or any other method available to you for creating a database.
3. In the modules.data_collector.py file, in the collect_data function, locate the following code snippet:
```
conn = psycopg2.connect(
            host="YOUR_HOST",
            port="YOUR_PORT",
            database="YOUR_NAME_DB",
            user="YOUR_USER",
            password="YOUR_PASSWORD",
        )
```
Replace the values with the corresponding settings of your PostgreSQL database.
## Running the Application

1. Start the web application by running the following command: python app.py.
2. Open a web browser and go to http://localhost:5000.

## Usage

1. On the home page, enter the symbol (e.g., BTCUSDT) and interval (e.g., 1d, 4h, 1h) for data collection.
2. Click the "Collect Data" button.
3. Wait for the data collection process to complete. Upon successful execution, the data will be saved in CSV format and added to the PostgreSQL database.
4. After data collection, a candlestick chart and market capitalization chart will be displayed.
5. You can return to the home page by clicking the "Main Page" button.
