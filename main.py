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
from scripts.web_scraping.colsubsidio import colsubsidioScraper
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
    df.to_csv(f"data\colsubsidioData{dt.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)
    telapsed = dt.now() - start
    printLog("Finshed process of web crawling and scraping into https://www.drogueriascolsubsidio.com", log)
    printLog(f"Time Elapsed: {telapsed}", log)


# Test GetCredentials
user="fsalinas"
cr = GetCredentials(user)

# Test query
sql = "SELECT * FROM dw.dim_trabajadores;"
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
    Select=True
)
print(data)

# Run complete process on drogueriascolsubsidio.com
# processColsubsidio()

