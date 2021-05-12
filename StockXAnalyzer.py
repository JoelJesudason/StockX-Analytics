from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt

class StockXAnalyzer:

    def __init__(self):
        self.shoeplot = None

    def get_chart_data(self,shoeurl,inplace=False):

        url = f'http://webcache.googleusercontent.com/search?q=cache:https://stockx.com/{shoeurl}'
        print(url)

        html_content = requests.get(url).text

        # Parse the html content
        soup = BeautifulSoup(html_content, "lxml")

        # zone in on table
        chart_data = soup.find_all("path",attrs = {"class":"highcharts-graph"})

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