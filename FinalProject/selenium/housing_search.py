from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

from CLSearch import CLSearch
from aptsSearch import aptsSearch

def get_data(text):
    craigslist = CLSearch(text)
    apts = aptsSearch(text)
    combined = craigslist + apts

    df = pd.DataFrame(combined, columns=['name', 'link', 'price', 'beds', 'bath'])
    duplicateRows = df[df.duplicated(['name', 'price'])]
    df.drop(duplicateRows.index, inplace=True)
    df.to_csv('dataframe/apartments.csv', index=False)
    print('csv saved')
    print('Dataframe: ')
    print(df)
    return df

def get_sortedData(sort_type):
    df = pd.read_csv('dataframe/apartments.csv')
    if sort_type == '1':
        df = df.sort_values('price', ascending=True)
        print('Ascending Price')
    elif sort_type == '2':
        df = df.sort_values('price', ascending=False)
        print('Descending Price')
    elif sort_type == '3':
        df = df.sort_values('beds', ascending=True)
        print('Ascending Beds')
    elif sort_type == '4':
        df = df.sort_values('beds', ascending=False)
        print('Descending Beds')
    elif sort_type == '5':
        df = df.sort_values('bath', ascending=True)
        print('Ascending Baths')
    else:
        df = df.sort_values('bath', ascending=False)
        print('Descending Baths')
        
    df.to_csv('dataframe/apartments.csv', index=False)
    return df

# print(get_data('charles village').sort_values('price', ascending=False))