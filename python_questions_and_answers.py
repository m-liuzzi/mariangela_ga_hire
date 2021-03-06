#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import io
import json
from pandas.io.json import json_normalize


def read_data(api):
    res = requests.get(api)
    json_data = json.loads(res.text)
    df = pd.DataFrame.from_dict(json_normalize(json_data), orient='columns')
    return df    
    
def transform_df(df):
    df = df.loc[:, df.columns.str.contains('close')] #look only at the "close" price
    s=df.columns.str.split('.') #split column headers in order to retrieve the dates
    dates = [sublist[1] for sublist in s] #get only the date from header name
    df.columns = dates #replace headers only with the date relevant to the price
    df = pd.melt(df, var_name='date')
    df["value"] = df.value.astype(float)
    return df

def calculate_weekly_price(df):
    print("Weekly close prices:")
    return df.groupby(df['date'].dt.week)["value"].mean()
    
def calculate_rolling_3(df):
    print("3-day rolling average:")
    fig, ax = plt.subplots()
    ax.plot(df.groupby(df.index // 3).agg("mean"), marker='o', linestyle='-')
    ax.set_ylabel('3-day rolling average')
    ax.set_title('3-day rolling average close price')
    return df.groupby(df.index // 3).agg("mean")
    
def calculate_rolling_7(df):
    print("7-day rolling average:")
    fig, ax = plt.subplots()
    ax.plot(df.groupby(df.index // 7).agg("mean"), marker='o', linestyle='-')
    ax.set_ylabel('7-day rolling average')
    ax.set_title('7-day rolling average close price')
    return df.groupby(df.index // 7).agg("mean")
    
if __name__ == __'main'__:
  my_api = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=NQW2B7EP84XGZ82L'
  data = read_data(my_api) 
  currency = transform_df(data)
  calculate_weekly_price(currency) #calculates weekly close price
  calculate_rolling_3(currency) #reports and displays 3-day rolling average close price
  calculate_rolling_7(currency) #reports and displays 7-day rolling average close price
  
