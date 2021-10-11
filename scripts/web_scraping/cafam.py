"""
Created on 06/10/2021
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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('prefs',{'profile.managed_default_content_setings.images':2})
scrapingConfigData = GetScrapingConfig("cafam")

class cafamScraper():

    def __init__(
        self,
        url=scrapingConfigData[1],
        chromedriver=scrapingConfigData[0],
        dateScraping=dt.now().strftime("%Y-%m-%d"),
        timeScraping=dt.now().strftime("%H:%M:%S"),
        categoryURLs=[],
        productURLs=[],
        log = "log\log_cafam.txt"):
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
                
                categoriesList = soup.find_all('div', {'class': 'iqitmegamenu-wrapper col-xs-12 cbp-hor-width-1 clearfix'})[0]
                categoriesList = categoriesList.find_all('li', {'class': 'cbp-hrmenu-tab'})
                
                urls_list = [x.get_attribute_list('href')[0] for x in categoriesList[0].find_all('a') if len(x.get_attribute_list('href')[0].split('/'))==4]
            
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

        try:
            productURL = productSoup.find('a').get_attribute_list('href')[0]
        except:
            productURL = 'No conseguida'

        try:
            title = productSoup.find('span',{'class':'grid-name'}).text.strip()
        except:
            title = 'No conseguida'
        
        try:
            productBrand = productSoup.find('span',{'class':'desc-grid'}).text.strip()
        except:
            productBrand = 'No conseguida'
        
        try:
            fullPrice = int(productSoup.find('span',{'class':'old-price product-price'}).text.strip().replace('$ ','').replace(',',''))
        except:
            fullPrice = 0
        
        try:
            finalPrice = int(productSoup.find('span',{'class':'price product-price'}).text.strip().replace('$ ','').replace(',',''))
        except:
            finalPrice = 0
        
        return {
            'product_url': productURL.replace('"','').replace('\n','').replace(',',''),
            'category_url': catURL,
            'scraping_date': dt.now().strftime("%Y-%m-%d"),
            'scraping_time': dt.now().strftime("%H:%M:%S"),
            'title': title.replace('"','').replace("'","").replace('\n','').replace(',',''),
            'productBrand': productBrand.replace('"','').replace("'","").replace('\n','').replace(r'Presentación', '').replace(',',''),
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
        productSoup = BeautifulSoup(browser.page_source, 'html.parser').find('div',{'class':'list-wrapper'}).find_all('li')
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

        def nextPage(browser):
            time.sleep(scrollWaitTime)
            try:
                pagination = browser.find_elements_by_id('pagination')[0]
                print("\n\nPagination: " + str(pagination.find_element_by_class_name('pagination_next')))
                pagination.find_element_by_class_name('pagination_next').click()
                wait.until(EC.presence_of_element_located((By.ID, "center_column")))
                browser.execute_script("window.stop();")
                print("BROWSER: " + str(browser.current_url))
                return True
            except:
                return False
            
        printLog("Creating a list of Category URLs.", self.log)
        self.getCategoriesList()
        printLog("Starting process with each URL.", self.log)
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        with closing(Chrome(executable_path = self.chromedriver, options=options)) as browser:
            wait = WebDriverWait(browser, 20)
            productDataList = []
            for catURL in self.categoryURLs:
                printLog(f"Working on {catURL}", self.log)
                browser.get(catURL)

                # NUEVAS LINEAS DE CODIGO REVISAR!!!!
                try:
                    pagination = browser.find_elements_by_id('pagination')[0]
                    listPagCatURLs = [f"{browser.current_url}?p={y}" for y in range(int([x.text for x in browser.find_elements_by_tag_name("li") if x.text.isdigit()][-1]))]
                except:
                    listPagCatURLs = [catURL]
                    
                for pagCatURL in listPagCatURLs:
                    printLog(f"Working on {pagCatURL}", self.log)
                    try:
                        browser.get(pagCatURL)
                        productDataList.append(self.getAllProductData(browser, pagCatURL))
                    except:
                        print("-*"*20 + " Error al procesar browser..." + "-*"*20)
                        browser = Chrome(executable_path = self.chromedriver, options=options)
        
        printLog(f"Lenght of productDataList: {len(productDataList)}", self.log)
        if len(productDataList)>0:
            allProductDataFrame = pd.concat(productDataList, axis=0, ignore_index=True)
            return (allProductDataFrame)

class cafamPostgres():
    
    def __init__(self, values, sqlInsert = ""):
        with open("scripts/web_scraping/database/sql/insert_cafam.sql", "r") as f:
            self.sqlInsert = f.read()
            self.values = values
    
    def setSQLInsert(self):
        self.sqlInsert = self.sqlInsert.replace("{values}", self.values)
        print(self.sqlInsert)
        return(self.sqlInsert)