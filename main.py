# External Packages
import pandas as pd
from datetime import datetime as dt
import time

# Internal packages
from scripts.web_scraping.colsubsidio import colsubsidioScraper
from scripts.web_scraping.database.create_tables import colsubsidio
# from scripts.web_scraping.packages import Load2PostgreSQL
# from scripts.web_scraping.packages.runSQL import _runTest, runSQL
from scripts.web_scraping.packages import *
from scripts.web_scraping.packages.Load2PostgreSQL import sqlColsubsidio
from scripts.web_scraping.packages.CreateLog import printLog

log = "log\log.txt"

def processColsubsidio():
    """
    PENDING DOCUMENTATION...
    """
    printLog("Starting web crawling and scraping process with https://www.drogueriascolsubsidio.com", log)
    clsSpider = colsubsidioScraper()
    df = clsSpider.productDataFromAllCategories()
    printLog("Saving the web scraping results from https://www.drogueriascolsubsidio.com into a csv file.", log)
    df.to_csv(f"data\colsubsidioData{dt.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)
    printLog("Finshed process of web crawling and scraping into https://www.drogueriascolsubsidio.com", log)

# Run complete process on drogueriascolsubsidio.com
processColsubsidio()



# sqlcls = sqlColsubsidio()
# sqlcls.createColsubsidio()


# print(_runTest())



# runSQL(
#     SQL,
#     user="postgres",
#     password="A123",
#     host="localhost",
#     port="5432",
#     database="postgres",
#     sslcert=None,
#     sslkey=None,
#     sslrootcert=None,
#     Select=True
#     )

# print("\n\nBuilding the object...")
# cs = colsubsidioScraper()
# print("-*-"*50)
# print("\n\nGetting products list...")
# cs.productDataFromAllCategories().to_csv(f"./data/colsubsidio_{dt.now().strftime('%Y%m%d_%H%M%S')}.csv")
# with open("data/data.txt", "+w") as file:
#     file.writelines(str(dataList))
# print("-*-"*50)
# # print(categoriesList(cd=chromedriver, url=principal_url))
# # print(productDataFromCategory(r"https://www.drogueriascolsubsidio.com/higiene-y-cuidado-personal/aseo-personal/jabones-y-gel-antibacterial", 2))