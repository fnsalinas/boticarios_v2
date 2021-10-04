"""
Created on 28/09/2021
Author: Fabio Salinas (fabio.salinas1982@gmail.com)
Version: 1.0
"""

from scripts.web_scraping.packages.runSQL import runSQL

class sqlColsubsidio():

    def createColsubsidio():
        sql = """CREATE TABLE IF NOT EXISTS web_scraping.colsubsidio (
            id SERIAL PRIMARY KEY,
            product_url TEXT,
            scraping_date DATE,
            scraping_time TIME,
            title TEXT,
            presentation TEXT,
            full_price NUMBER,
            final_price NUMBER,
            datetime_created DEFAULT NOW());"""
        runSQL(sql, )
    
    def insertColsubsidio():
        print("Pendiente")
    
    def deleteColsubsidio():
        print("Pendiente")
    
    def dropColsubsidio():
        print("Pendiente")