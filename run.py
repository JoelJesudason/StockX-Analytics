from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv
import pandas as pd
import  numpy as np
from StockXAnalyzer import StockXShoeContent

def main():

    shoe_analyzer = StockXShoeContent()
    shoeurl = input("Shoe URL Ending: ")

    shoe_analyzer.acquire_shoe_data(shoeurl, inplace=True)    

    shoe_analyzer.plot_shoeplot()

if __name__ == '__main__':
    main()