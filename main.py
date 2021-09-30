import pandas as pd
import time
from web_scraping.colsubsidio import colsubsidioScraper
from packages.runSQL import _runTest, runSQL

print(_runTest())

print("\n\nBuilding the object...")
cs = colsubsidioScraper()
print("-*-"*50)
print("\n\nGetting products list...")
dataList = cs.getAllProductData()
print("\n\nPrinting to txt file...")
with open("data/data.txt", "+a") as file:
    file.writelines(str(dataList))
print("-*-"*50)
# print(categoriesList(cd=chromedriver, url=principal_url))
# print(productDataFromCategory(r"https://www.drogueriascolsubsidio.com/higiene-y-cuidado-personal/aseo-personal/jabones-y-gel-antibacterial", 2))