"""
Created on 28/09/2021
Author: Fabio Salinas (fabio.salinas1982@gmail.com)
Version: 1.0
"""

# External Packages
import pandas as pd
from datetime import datetime as dt
import time
from multiprocessing import Process

# Internal packages
from scripts.web_scraping.colsubsidio import colsubsidioScraper, colsubsidioPostgres
from scripts.web_scraping.cafam import cafamScraper, cafamPostgres
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

def processCafam():
    """
    PENDING DOCUMENTATION...
    """
    log = "log\log_cafam.txt"
    start = dt.now()
    printLog("Starting web crawling and scraping process with https://www.drogueriascafam.com.co", log)
    clsSpider = cafamScraper()
    df = clsSpider.productDataFromAllCategories()
    printLog("Saving the web scraping results from https://www.drogueriascafam.com.co into a csv file.", log)
    data_path = f"data\cafamData{dt.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(data_path, index=False)
    telapsed = dt.now() - start
    printLog("Finshed process of web crawling and scraping into https://www.drogueriascafam.com.co", log)
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
        clsInsert = cafamPostgres(values = val)
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

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    
    for p in proc:
        p.join()

def processWS():
    process = input("Procesar ahora? (Si/No): ").lower()=="si"
    while True:
        t = int(dt.now().strftime("%H%M"))
        if t in (700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300) or process:
            runInParallel(processColsubsidio, processCafam)
            process=False
            # try:
            #     # processColsubsidio()
            #     webScrapingFunc()
            #     process=False
            # except:
            #     print("Error al procesar...")
        for s in range(0, 60, 1):
            msg = f"Waiting  until the next review... ({60-s}) Seconds remaining..."
            print(msg, end="\r")
            time.sleep(1)

if __name__ == "__main__":
    processWS()
