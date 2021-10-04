"""
Created on 28/09/2021
Author: Fabio Salinas (fabio.salinas1982@gmail.com)
Version: 1.0
"""

class colsubsidio():

    def getSQLCreate():
        return """CREATE TABLE IF NOT EXISTS web_scraping.colsubsidio (
            id SERIAL PRIMARY KEY,
            product_url TEXT,
            scraping_date DATE,
            scraping_time TIME,
            title TEXT,
            presentation TEXT,
            full_price NUMBER,
            final_price NUMBER,
            datetime_created DEFAULT NOW());"""

    def getSQLInsert():
        return """INSERT INTO web_scraping.colsubsidio (
            product_url TEXT,
            scraping_date DATE,
            scraping_time TIME,
            title TEXT,
            presentation TEXT,
            full_price NUMBER,
            final_price NUMBER) VALUES {values};"""

    def getSQLDelete():
        return """DELETE FROM web_scraping.colsubsidio WHERE ({condition});"""

    def getSQLDrop():
        return """DROP TABLE IF EXISTS web_scraping.colsubsidio;"""
