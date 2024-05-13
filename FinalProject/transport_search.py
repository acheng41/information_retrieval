from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
from WUSearch import WUSearch
from expSearch import expSearch

import warnings

# Suppress future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def parse_mode(mode_string): 
    return [word.strip() for word in mode_string.split(',')]

def get_data(arrival_time, origin, destination, date, mode):
   
    mode = parse_mode(mode)
    print("These are the inputted modes:" + str(mode))
    expedia = []
    wanderu = []
    try: 
        if "all" in mode: 
                wanderu = WUSearch(origin, destination, date, "All")
                expedia = expSearch(origin, destination, date)
        else:  
            if "plane" in mode: 
                expedia = expSearch(origin, destination, date)
            if "bus" in mode and "train" in mode: 
                wanderu = WUSearch(origin, destination, date, "All")
            elif "bus" in mode: 
                wanderu = WUSearch(origin, destination, date, "Bus Only")
            else: 
                wanderu = WUSearch(origin, destination, date, "Train Only")

        combined = wanderu + expedia
        print("Total Results:" + str(len(combined)))

        df = pd.DataFrame(combined, columns=['Mode', 'Dept', 'Arr', 'Duration', 'Price', 'Company'])
    except: 
        df = pd.read_csv('dataframe/transport516.csv')

    df['Price_sort'] = df['Price'].str.replace('$', '').astype(float)

    # Convert arrival_time to datetime object
    arrival_time = pd.to_datetime(arrival_time)
    
    # Filter out rows with 'Arr' after arrival_time
    df['Arr'] = pd.to_datetime(df['Arr'])
    df['Dept'] = pd.to_datetime(df['Dept'])
    # Filter out rows where both Dept and Arr are before arrival_time
    df = df[(df['Dept'] <= arrival_time) & (df['Arr'] <= arrival_time)]

    df['Duration_min'] = df['Duration'].apply(lambda x: int(x.split('h')[0]) * 60 + int(x.split(' ')[1][:-1]))
    df.loc[df['Mode'] == 'Plane', 'added_arrival'] = df['Arr'] + pd.Timedelta(hours=1)
    df.loc[df['Mode'] == 'Bus', 'added_arrival'] = df['Arr'] + pd.Timedelta(hours=0.5)
    df.loc[df['Mode'] == 'Train', 'added_arrival'] = df['Arr'] + pd.Timedelta(hours=0.5)

    #Create Custome Weighting
    max_price = df['Price_sort'].max()
    min_price = df['Price_sort'].min()
    price_range = max_price - min_price
    max_duration = df['Duration_min'].max()
    min_duration = df['Duration_min'].min()
    duration_range = max_duration - min_duration
    weight_dur = 0.2
    weight_price = 0.8
    df['Custom_weighting'] = (df['Duration_min'] - min_duration)/duration_range * weight_dur + (df['Price_sort'] - min_price)/price_range * weight_price

    df.to_csv('dataframe/transport.csv', index=False)
    print('csv saved')
    print('Dataframe: ')
    print(df)
    return df

def get_sortedData(sort_type, dataframe):
    df = pd.read_csv('dataframe/transport.csv')
    if sort_type == '1':
        df = df.sort_values('Price_sort', ascending=True)
        print('Cheapest\n')
        print_results(df.head(10))
    elif sort_type == '2':
        df = df.sort_values('Duration_min', ascending=True)
        print('Fastest\n')
        print_results(df.head(10))
    elif sort_type == '3':
        df = df.sort_values('Custom_weighting', ascending=True)
        print('Recommended\n')
        print_results(df.head(10))
        
    df.to_csv('dataframe/transport.csv', index=False)
    return df

def print_results(df):
    print_df = pd.DataFrame()
    print_df['Dept'] = pd.to_datetime(df['Dept']).dt.strftime('%I:%M %p')
    print_df['Arr'] = pd.to_datetime(df['Arr']).dt.strftime('%I:%M %p')
    print_df['Mode'] = df['Mode']
    print_df['Price'] = df['Price']
    print_df['Duration'] = df['Duration']
    print_df['Company'] = df['Company']
    print(print_df[['Mode', 'Dept', 'Arr', 'Duration', 'Price', 'Company']].to_string(index=False))


if __name__ == '__main__':
    df = pd.read_csv('dataframe/transport.csv')
    #get_data('9:00 PM', 'BWI', 'JFK', '05/14/2024', 'plane,train')
    get_sortedData('3', df)
    #print_results(df)
