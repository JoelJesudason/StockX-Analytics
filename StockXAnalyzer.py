from bs4 import BeautifulSoup
from pathlib import Path
from time import strptime
import datetime
import requests
import csv
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt

class StockXShoeContent:

    def __init__(self):
        self.shoe_data = pd.DataFrame()
        self.shoe_url = ""
        self.soup = None
        self.num_shoes = 0

    def acquire_shoe_data(self,shoe_url,inplace=False):

        self.shoe_url = f'http://webcache.googleusercontent.com/search?q=cache:https://stockx.com/{shoe_url}'
        print(self.shoe_url)

        html_content = requests.get(self.shoe_url).text

        # Parse the html content
        self.soup = BeautifulSoup(html_content, "lxml")

        # zone in on table
        chart_data = self.soup.find_all("path",attrs = {"class":"highcharts-graph"})

        raw_xy_data = str(chart_data).split(' L ')[1:-1]
        xy_data = []
        for pair in raw_xy_data:
            xy_data.append( list(map(float,pair.split(' '))) )
        xy_df = pd.DataFrame(xy_data,index=range(len(xy_data)),columns=['x','y'])

        # the chart data comes flipped for some reason. This unflips
        xy_df['y'] = max(xy_df['y']) - xy_df['y'][:99]

        # self.shoe_data = pd.concat([ self.shoe_data , xy_df ])
        self.num_shoes += 1
        
        axis_data = self.soup.find_all("g",attrs = {"class":"highcharts-axis-labels highcharts-xaxis-labels"})
        axis_data = axis_data[0].find_all('text',attrs = {'transform':"translate(0,0)"})
        axis_data = [date.string.strip() for date in axis_data]
        
        formatted_time_axis = []
        for axis_date in axis_data:
            formatted_time_axis.append(datetime.datetime(2020,
                                                         # getting month
                                                         strptime(axis_date[axis_date.find('.')+2:],'%b').tm_mon,
                                                         # getting day
                                                         int( axis_date[:axis_date.find('.')] )))
            
        time_span = (formatted_time_axis[-1] - formatted_time_axis[0]).days
        increments = (formatted_time_axis[-1] - formatted_time_axis[0]).days / len(xy_df)
        
        xy_df['Day'] = np.arange(0.0, time_span, increments)

        # self.shoe_data['Day'] = np.arange(0.0, time_span, increments)
        self.shoe_data = pd.concat([ self.shoe_data , xy_df ])
        
        if inplace == False:
            return xy_df
        else:
            pass

    def get_time_axis(self):
    
        pass
    
    def get_data(self):
        return self.shoe_data
    
    def plot_shoeplot(self,plot_kind):
        figure = self.shoe_data.plot(x='Day',y='y',kind=plot_kind)
        plt.show()