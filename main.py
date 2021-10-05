"""
Created on 28/09/2021
Author: Fabio Salinas (fabio.salinas1982@gmail.com)
Version: 1.0
"""

# External Packages
import pandas as pd
from datetime import datetime as dt
import time

# Internal packages
from scripts.web_scraping.colsubsidio import colsubsidioScraper, colsubsidioPostgres
from scripts.web_scraping.database.create_tables import colsubsidio
from scripts.web_scraping.packages.runSQL import runSQL
from scripts.web_scraping.packages.Load2PostgreSQL import sqlColsubsidio
from scripts.web_scraping.packages.CreateLog import printLog
from scripts.web_scraping.packages.GetCredentials import GetCredentials

log = "log\log.txt"

def processColsubsidio():
    """
    PENDING DOCUMENTATION...
    """
    start = dt.now()
    printLog("Starting web crawling and scraping process with https://www.drogueriascolsubsidio.com", log)
    clsSpider = colsubsidioScraper()
    df = clsSpider.productDataFromAllCategories()
    printLog("Saving the web scraping results from https://www.drogueriascolsubsidio.com into a csv file.", log)
    data_path = f"data\colsubsidioData{dt.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(data_path, index=False)
    telapsed = dt.now() - start
    printLog("Finshed process of web crawling and scraping into https://www.drogueriascolsubsidio.com", log)
    printLog(f"Time Elapsed: {telapsed}", log)
    
    start2 = dt.now()
    printLog("Starting process of loading data to PostgreSQL...", log)
    # Enable the next line for testing...
    # data_path = "data\colsubsidioData20211004_232433.csv"
    df = pd.read_csv(data_path, sep=",")
    df.info()
    
    user="fsalinas"
    cr = GetCredentials(user)
    interval = 500
    listOfTuples = [[x, x+interval] for x in range(0, df.values.shape[0], interval)]
    listOfTuples[-1][1] = df.values.shape[0]
    for intervals in listOfTuples:
        printLog(f"Working on interval {intervals} last Interval: {listOfTuples[-1]}", log)
        val = str(df.values[intervals[0]: intervals[1]].tolist()).replace("[","(").replace("]",")").replace("((","(").replace("))",")")
        clsInsert = colsubsidioPostgres(values = val)
        sql = clsInsert.setSQLInsert()
        data = runSQL(
            SQL=sql,
            user=user,
            password=cr[0],
            host=cr[1],
            port=cr[2],
            database=cr[3],
            sslcert="scripts/web_scraping/assets/private/gcp_boticarios/convertidos/ssl-cert.crt",
            sslkey="scripts/web_scraping/assets/private/gcp_boticarios/convertidos/ssl-key.key",
            sslrootcert="scripts/web_scraping/assets/private/gcp_boticarios/convertidos/ca-cert.crt",
            Select=False
        )
        printLog(f"Results of interval {intervals}: " + data["result"] + " - " + data["msg"] + " - " + str(data["telapsed"]), log)
    
    telapsed, totalTElapsed = dt.now() - start2, dt.now() - start
    printLog("Finshed process loading data to PostgreSQL", log)
    printLog(f"Time Elapsed: {telapsed}", log)
    printLog(f"Total Time Elapsed: {totalTElapsed}", log)

while True:
    t = int(dt.now().strftime("%H%M"))
    if t in (800, 1100, 1400, 1700, 2000, 2300):
        processColsubsidio()
    for s in range(0, 60, 1):
        msg = f"Waiting until the next review... ({60-s}) Seconds remaining..."
        print(msg, end="\r")
        time.sleep(1)