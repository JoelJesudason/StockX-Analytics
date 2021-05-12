from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv
import pandas as pd
import  numpy as np
from StockXAnalyzer import StockXAnalyzer

def main():

    shoe_analyzer = StockXAnalyzer()
    shoeurl = input("Shoe URL: ")

    shoe_analyzer.get_chart_data(shoeurl, inplace=True)    

    shoe_analyzer.plot_shoeplot()

if __name__ == '__main__':
    main()