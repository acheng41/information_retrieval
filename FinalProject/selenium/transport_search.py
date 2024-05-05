from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

# from selenium.WUSearch import WUSearch
# from selenium.expSearch import expSearch

def get_data(arrival_time, origin, destination, date):
    wanderu = [{'Mode' : 'Train', 'Dept': '8:30 AM', 'Arr': '11:30 AM', 'Duration': '3h 0m', 'Price': '$30.00', 'Company': 'Amtrak Northeast Regional'},
               {'Mode' : 'Train', 'Dept': '10:00 AM', 'Arr': '1:30 PM', 'Duration': '3h 30m', 'Price': '$30.00', 'Company': 'Amtrak Northeast Regional'},
               {'Mode' : 'Train', 'Dept': '12:00 PM', 'Arr': '3:45 PM', 'Duration': '3h 45m', 'Price': '$30.00', 'Company': 'Amtrak Northeast Regional'},
               {'Mode' : 'Train', 'Dept': '4:00 PM', 'Arr': '6:56 PM', 'Duration': '2h 56m', 'Price': '$30.00', 'Company': 'Amtrak Northeast Regional'},
               {'Mode' : 'Train', 'Dept': '10:51 PM', 'Arr': '1:57 AM', 'Duration': '3h 6m', 'Price': '$30.00', 'Company': 'Amtrak Northeast Regional'}]
    expedia = [{'Mode': 'Plane', 'Dept': '6:05am', 'Arr': '7:25am', 'Duration': '1h 20m', 'Price': '$216', 'Company': 'Delta'}, 
               {'Mode': 'Plane', 'Dept': '5:17pm', 'Arr': '6:45pm', 'Duration': '1h 28m', 'Price': '$349', 'Company': 'Delta'}, 
               {'Mode': 'Plane', 'Dept': '6:50pm', 'Arr': '11:50pm', 'Duration': '5h 0m', 'Price': '$272', 'Company': 'Delta'}, 
               {'Mode': 'Plane', 'Dept': '2:04pm', 'Arr': '8:26pm', 'Duration': '6h 22m', 'Price': '$272', 'Company': 'Delta'}, 
               {'Mode': 'Plane', 'Dept': '4:43pm', 'Arr': '11:50pm', 'Duration': '7h 7m', 'Price': '$272', 'Company': 'Delta'}]
    #wanderu = WUSearch(origin, destination, date)
    #expedia = expSearch(origin, destination, date)
    combined = wanderu + expedia
    print(combined)

    df = pd.DataFrame(combined, columns=['Mode', 'Dept', 'Arr', 'Duration', 'Price', 'Company'])

    # Convert arrival_time to datetime object
    arrival_time = pd.to_datetime(arrival_time)
    
    # Filter out rows with 'Arr' after arrival_time
    df['Arr'] = pd.to_datetime(df['Arr'])
    df['Dept'] = pd.to_datetime(df['Dept'])
    # Filter out rows where both Dept and Arr are before arrival_time
    df = df[(df['Dept'] <= arrival_time) & (df['Arr'] <= arrival_time)]

    df.to_csv('dataframe/transport.csv', index=False)
    print('csv saved')
    print('Dataframe: ')
    print(df)
    return df

def get_sortedData(sort_type):
    df = pd.read_csv('dataframe/transport.csv')
    if sort_type == '1':
        df = df.sort_values('Price', ascending=True)
        print('Ascending Price')
    elif sort_type == '2':
        df = df.sort_values('Duration', ascending=True)
        print('Ascending Duration')
        
    df.to_csv('dataframe/transport.csv', index=False)
    return df

# print(get_data('charles village').sort_values('price', ascending=False))

if __name__ == '__main__':
    get_data('9:00 PM', 'BWI', 'JFK', '05/14/2024')