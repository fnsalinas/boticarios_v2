"""
Created on 28/09/2021
Author: Fabio Salinas (fabio.salinas1982@gmail.com)
Version: 1.0
"""

# External Packages
import pandas as pd
import time
from datetime import datetime as dt
from contextlib import closing
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

# Internal packages
from scripts.web_scraping.packages.CreateLog import printLog
from scripts.web_scraping.packages.GetScrapingConfig import GetScrapingConfig

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('prefs',{'profile.managed_default_content_setings.images':2})
scrapingConfigData = GetScrapingConfig("colsubsidio")

class colsubsidioScraper():

    log = "log\log_colsubsidio.txt"

    def __init__(
        self,
        url=scrapingConfigData[1],
        chromedriver=scrapingConfigData[0],
        dateScraping=dt.now().strftime("%Y-%m-%d"),
        timeScraping=dt.now().strftime("%H:%M:%S"),
        categoryURLs=[],
        productURLs=[],
        log = "log\log_cafam.txt"
        ):
        self.principal_url = url
        self.chromedriver = chromedriver
        self.dateScraping = dateScraping
        self.timeScraping = timeScraping
        self.categoryURLs = categoryURLs
        self.productURLs = productURLs
        self.log = log
    
    def getCategoriesList(self):
        """
        Navigate through the principal URL and extract the category URLs

        Arguments: None
        
        Returns:
            List with strings that contains all the Categories URLs.
        """
        try:
            with closing(Chrome(executable_path = self.chromedriver, options=options)) as browser:
                # Navigate to he principal URL and parse the html source
                browser.get(self.principal_url)
                soup = BeautifulSoup(browser.page_source, 'html.parser')

                # Create a dictionary with the Category URLs and <ul> elements
                categoriesList = soup.find_all('ul',{'class':'categoria-container'})
                dc_cat_url = {cat.find_all('a')[1].text.lower().replace('ver ', ''):cat for x, cat in enumerate(categoriesList)}

                # Extract the URL from the <ul> elements
                urls_list = []
                for cat in dc_cat_url.keys():
                    urls_list += [x.get_attribute_list('href')[0] for x in dc_cat_url[cat].find_all('a')]
                
                urls_list = [self.principal_url + x for x in list(dict.fromkeys(urls_list))]
            
            self.categoryURLs = urls_list
            return urls_list
        except:
            return self.getCategoriesList()

    def getOneProductData(self, productSoup, catURL):
        """
        Extract data from one product based on the soup of that product allocated in the category url.

        Arguments:
            productSoup (BeautifulSoup object): Contains the soup extracted from the caterories url.
        
        Returns (dict): Dictionady with the product data with the structure:
            {
                'product_url': productURL,
                'scraping_date': self.dateScraping,
                'scraping_time': self.timeScraping,
                'title': title,
                'presentation': presentation,
                'full_price': fullPrice,
                'final_price': finalPrice
            }
        """
        productURL = productSoup.find_all('a')[0].get_attribute_list('href')[0]
        title = productSoup.find('p', {'class': 'dataproducto-nameProduct'}).text
        
        try:
            presentation = productSoup.find('div', {'class': 'dataproducto-info dataproducto-Presentacion'}).text.strip()
        except:
            presentation = 'N/A'
        
        try:
            fullPrice = float(productSoup.find('div', {'class': 'precioTachadoVitrina'}).text.replace('Antes: $','').replace('.','').replace(',','.'))
        except:
            fullPrice = 0
        
        try:
            finalPrice = float(productSoup.find('p', {'class': 'dataproducto-bestPrice'}).text.replace('$','').replace('.','').replace(',','.'))
        except:
            finalPrice = 0
        
        return {
            'product_url': productURL.replace('"','').replace('\n','').replace(',',''),
            'category_url': catURL,
            'scraping_date': dt.now().strftime("%Y-%m-%d"),
            'scraping_time': dt.now().strftime("%H:%M:%S"),
            'title': title.replace('"','').replace("'","").replace('\n','').replace(',',''),
            'presentation': presentation.replace('"','').replace("'","").replace('\n','').replace(r'Presentaci??n', '').replace(',',''),
            'full_price': fullPrice,
            'final_price': finalPrice
        }
    
    def getAllProductData(self, browser, catURL):
        """
        Iterate through each product soup on the browser and apply the getOneProductData() method to concatenate all the results.

        Arguments:
            browser (selenium.webdriver.chrome.webdriver.WebDriver): Browser that have already loaded the categories URL.
        
        Returns (pandas.core.frame.DataFrame) with all the products of the category url.
        """
        productSoup = BeautifulSoup(browser.page_source, 'html.parser').find_all('div', {'class':'product-Vitrina-masVendidos js-productVitrineShowcase WishlistModule rendered'})
        productsDataList = []
        for prod in productSoup:
            dfOneProduct = pd.DataFrame.from_dict(self.getOneProductData(prod, catURL), orient='index').T
            if len(dfOneProduct)>0: productsDataList.append(dfOneProduct)
        
        try:
            concatenatedProductData = pd.concat(productsDataList, axis=0, ignore_index=True)
        except:
            concatenatedProductData = pd.DataFrame()
        return(concatenatedProductData)

    def productDataFromAllCategories(self, scrollWaitTime=2):
        """
        PENDING DOCUMENTATION...
        """
        printLog("Creating a list of Category URLs.", self.log)
        self.getCategoriesList()
        printLog("Starting process with each URL.", self.log)
        with closing(Chrome(executable_path = self.chromedriver, options=options)) as browser:
            productDataList = []
            for catURL in self.categoryURLs:
                printLog(f"Working on {catURL}", self.log)
                browser.get(catURL)

                lastHeight = browser.execute_script("return document.body.scrollHeight")
                scroll_number = 1
                while True:
                    printLog(f"{dt.now().strftime('%H:%M:%S')} Scroll nro: {scroll_number:,.0f}", self.log)
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scrollWaitTime)
                    newHeight = browser.execute_script("return document.body.scrollHeight")
                    if newHeight == lastHeight:
                        break
                    lastHeight = newHeight
                    scroll_number += 1

                productDataList.append(self.getAllProductData(browser, catURL))
        
        printLog(f"Lenght of productDataList: {len(productDataList)}", self.log)
        if len(productDataList)>0:
            allProductDataFrame = pd.concat(productDataList, axis=0, ignore_index=True)
            return (allProductDataFrame)

class colsubsidioPostgres():
    
    def __init__(self, values, sqlInsert = ""):
        with open("scripts/web_scraping/database/sql/insert_colsubsidio.sql", "r") as f:
            self.sqlInsert = f.read()
            self.values = values
    
    def setSQLInsert(self):
        self.sqlInsert = self.sqlInsert.replace("{values}", self.values)
        print(self.sqlInsert)
        return(self.sqlInsert)