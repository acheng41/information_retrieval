from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
from WUSearch import WUSearch
from expSearch import expSearch

from datetime import timedelta

import warnings

# # Suppress future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def parse_mode(mode_string): 
    return [word.strip() for word in mode_string.split(',')]

def round_5(number): 
    return round(number / 5) * 5

def get_data(arrival_time, origin, destination, date, mode, filter, raw):
   
    mode = parse_mode(mode)
    print("\n")
    print("These are the inputted modes:" + str(mode))
    print(" ")

    if origin == "BWI": 
        origin_print = "Baltimore, MD"
    else: 
        origin_print = "New York, NY"
        
    if destination == "BWI": 
        destination_print = "Baltimore, MD"
    else: 
        destination_print = "New York, NY"
    
    print("destination:" + destination_print)
    print("origin:" + origin_print)

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
        print(" ")
        print("Total Results:" + str(len(combined)))

        df = pd.DataFrame(combined, columns=['Mode', 'Dept', 'Arr', 'Duration', 'Price', 'Company'])
    except: 
        print(" ")
        print("Unable to Complete Search")
        print("To Demonstrate Ranking, Pre-Saved Results for 5/16/2024 will be used")
        df = pd.read_csv('dataframe/transport516.csv')
        df['Dept'] = pd.to_datetime(df['Dept']).dt.strftime('%I:%M %p')
        df['Arr'] = pd.to_datetime(df['Arr']).dt.strftime('%I:%M %p')

    df['Price_sort'] = df['Price'].str.replace('$', '').astype(float)

    # Convert arrival_time to datetime object
    arrival_string = arrival_time
    arrival_time = pd.to_datetime(arrival_time)
    
    # Filter out rows with 'Arr' after arrival_time
    df['Arr'] = pd.to_datetime(df['Arr'])
    df['Dept'] = pd.to_datetime(df['Dept'])
    # Filter out rows where both Dept and Arr are before arrival_time
    df = df[(df['Dept'] <= arrival_time) & (df['Arr'] <= arrival_time)]

    print("Number of Trips Arriving Before " + arrival_string + ": " + str(len(df)))

    if len(df) == 0: 
        print(" ")
        print("There were no trips arriving before " + arrival_string )
        print("Please search for an earlier departure time")
        

    df['Duration_min'] = df['Duration'].apply(lambda x: int(x.split('h')[0]) * 60 + int(x.split(' ')[1][:-1]))
    df.loc[df['Mode'] == 'Plane', 'added_arrival'] = df['Arr'] + pd.Timedelta(hours=1)
    df.loc[df['Mode'] == 'Bus', 'added_arrival'] = df['Arr'] + pd.Timedelta(hours=0.5)
    df.loc[df['Mode'] == 'Train', 'added_arrival'] = df['Arr'] + pd.Timedelta(hours=0.5)

    if filter == 'yes':
        df = df[(df['added_arrival'] <= arrival_time)]

    #Create Custome Weighting
    max_price = df['Price_sort'].max()
    min_price = df['Price_sort'].min()
    price_range = max_price - min_price
    max_duration = df['Duration_min'].max()
    min_duration = df['Duration_min'].min()
    duration_range = max_duration - min_duration
    weight_dur = 0.2
    weight_price = 0.8
    df['Custom_weighting'] = (round_5(df['Duration_min']) - min_duration)/duration_range * weight_dur + (round_5(df['Price_sort']) - min_price)/price_range * weight_price

    df.to_csv('dataframe/transport.csv', index=False)
    print('csv saved')

    if raw == 'yes':
        print('Raw Dataframe: ')
        print(df)
    return df

def get_sortedData(sort_type, dataframe, arrival_time):
    df = pd.read_csv('dataframe/transport.csv')
    print(" ")
    if sort_type == '1':
        df = df.sort_values('Price_sort', ascending=True)
        print('Cheapest\n')
        print_results(df.head(10))
    elif sort_type == '2':
        df = df.sort_values('Duration_min', ascending=True)
        print('Fastest\n')
        print_results(df.head(10))
    elif sort_type == '3':
        df = df.sort_values(by =['Custom_weighting', 'Arr'], ascending=[True, False])
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
