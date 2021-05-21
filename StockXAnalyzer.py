from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt

class StockXShoeContent:

    def __init__(self):
        self.shoeplot = None
        self.shoeurl = None
        self.soup = None

    def get_chart_data(self,shoeurl,inplace=False):

        self.shoeurl = f'http://webcache.googleusercontent.com/search?q=cache:https://stockx.com/{shoeurl}'
        print(self.shoeurl)

        html_content = requests.get(self.shoeurl).text

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

        self.shoeplot = xy_df['y'].plot()

        if inplace == False:
            return xy_df

    def plot_shoeplot(self):
        figure = self.shoeplot
        plt.show()

    def get_time_axis(self):

        # zone in x axis
        chart_data = self.soup.find_all("g",attrs = {"class":"highcharts-axis-labels highcharts-xaxis-labels"})

        return chart_data