import pandas as pd
import time
from web_scraping.colsubsidio import colsubsidioScraper
from database.create_tables import colsubsidio
from packages.runSQL import _runTest, runSQL

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
# cs.productDataFromAllCategories().to_csv("./data/data.csv")
# with open("data/data.txt", "+w") as file:
#     file.writelines(str(dataList))
# print("-*-"*50)
# # print(categoriesList(cd=chromedriver, url=principal_url))
# # print(productDataFromCategory(r"https://www.drogueriascolsubsidio.com/higiene-y-cuidado-personal/aseo-personal/jabones-y-gel-antibacterial", 2))