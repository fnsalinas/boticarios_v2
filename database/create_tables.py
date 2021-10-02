class colsubsidio():

    def getSQLCreate():
        return """CREATE TABLE colsubsidio (
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
        return """INSERT INTO colsubsidio (
            product_url TEXT,
            scraping_date DATE,
            scraping_time TIME,
            title TEXT,
            presentation TEXT,
            full_price NUMBER,
            final_price NUMBER) VALUES {values};"""

    def getSQLDelete():
        return """DELETE FROM colsubsidio WHERE ({condition});"""

    def getSQLDrop():
        return """DROP TABLE colsubsidio;"""
