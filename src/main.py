from pandas import read_pickle
from yfinance import Ticker
# import numpy as np
from csv import reader
from os import path
from datetime import date, datetime
from math import ceil

def read_symbols_csv():

    file_path = path.join("static", "symbols.csv")
   
    result = []
    
    # Check if the file exists
    if not path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return result
    
    with open(file_path, 'r') as file:
        csv_reader = reader(file)
        
        for row in csv_reader:
            # Assuming the CSV file has two columns: symbol and date
            if len(row) == 2:
                symbol, date = row
                result.append((symbol, date))
            else:
                print(f"Skipping invalid row: {row}")
    
    return result


def current_time():
    
    today = date.today()
    now = datetime.now().strftime("%H:%M:%S")
    
    return f'{today} {now}'
    


def download_tables(stock_list = read_symbols_csv()):
    
    start_time = current_time()
    
    ctn = 0
    
    for item in stock_list:
        
        stock = Ticker(item[0])
        
        #get max 1 day data
        stock_1d_df = stock.history(start = item[1], 
                                    end = None,
                                    interval = '1d',
                                    period='max',
                                   )
        stock_1d_df.to_pickle(f'./data/{item[0]}_1d_df.pkl')
        
        #get max 1 hour data
        stock_1h_df = stock.history(interval = '1h',
                                    period='730d',
                                   )
        stock_1h_df.to_pickle(f'./data/{item[0]}_1h_df.pkl')
        
        ctn += 1
    
    end_time = current_time()
        
    return print(f'Start time: {start_time}\nDownloaded {ctn} max daily and hourly stock data\nEnd Time: {end_time}')


def compute_up_down(begin, end):
    if abs((end - begin) / begin) <= 187:
        return 0
    elif ((end - begin) / begin) > 187:
        return 1
    else:
        return 2

    
def compute_volume_per_dollar(vol, begin, end):
    if begin - end == 0:
        return vol
    else:
        return vol / abs(begin - end)
    
    
def compute_pct_change(num1, num2, dem):
    if dem == 0:
        return 0
    else:
        return (num2 - num1) / dem

    
def week_of_month(dt):
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()
    return int(ceil(adjusted_dom/7.0))



