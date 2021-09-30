import pandas as pd
import time
from datetime import datetime as dt
from contextlib import closing
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('prefs',{'profile.managed_default_content_setings.images':2})

class colsubsidioScraper():

    def __init__(
        self,
        url=r"https://www.drogueriascolsubsidio.com",
        chromedriver=r"assets\chromedriver.exe",
        dateScraping=dt.now().strftime("%Y-%m-%d"),
        timeScraping=dt.now().strftime("%H:%M:%S"),
        categoryURLs=[],
        productURLs=[]
        ):
        self.principal_url = url
        self.chromedriver = chromedriver
        self.dateScraping = dateScraping
        self.timeScraping = timeScraping
        self.categoryURLs = categoryURLs
        self.productURLs = productURLs
    
    def getCategoriesList(self):
        """
        Navigate through the principal URL and extract the product categories URLs

        Arguments:
            cd      (String): Path to the chromedriver that match with the chrome browser version installed.
            url     (String): Path to the Principal URL that contains all the catergorie URLs.
        
        Returns:
            List with strings that contains all the Categories URLs.
        """

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

    def productDataFromCategory(self, catURL, scrollWaitTime=2):
        """
        PENDING DOCUMENTATION...
        """
        def getAllProductData(browser):
            productSoup = BeautifulSoup(browser.page_source, 'html.parser').find_all('div', {'class':'product-Vitrina-masVendidos js-productVitrineShowcase WishlistModule rendered'})
            productsDataList = []
            for prod in productSoup:
                productURL = prod.find_all('a')[0].get_attribute_list('href')[0]
                title = prod.find('p', {'class': 'dataproducto-nameProduct'}).text
                
                try:
                    presentation = prod.find('div', {'class': 'dataproducto-info dataproducto-Presentacion'}).text.strip()
                except:
                    presentation = 'N/A'
                
                try:
                    fullPrice = float(prod.find('div', {'class': 'precioTachadoVitrina'}).text.replace('Antes: $','').replace('.','').replace(',','.'))
                except:
                    fullPrice = 0
                
                try:
                    finalPrice = float(prod.find('p', {'class': 'dataproducto-bestPrice'}).text.replace('$','').replace('.','').replace(',','.'))
                except:
                    finalPrice = 0
                
                productsDataList.append({
                    'product_url': productURL,
                    'scraping_date': self.dateScraping,
                    'scraping_time': self.timeScraping,
                    'title': title,
                    'presentation': presentation,
                    'full_price': fullPrice,
                    'final_price': finalPrice
                })
            
            return pd.concat([pd.DataFrame.from_dict(x, orient='index').T for x in productsDataList], axis=0, ignore_index=True)
        
        def getProductURLs(browser):
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            prodUrls = [x.get_attribute_list('href')[0] for x in soup.find_all('a') if x.get_attribute_list('href')[0]!=None and x.get_attribute_list('href')[0][-2:].lower()=='/p']
            return list(dict.fromkeys(prodUrls))

        with closing(Chrome(executable_path = self.chromedriver, options=options)) as browser:
            # Navigate to the category URL and parse the html source
            browser.get(catURL)

            lastHeight = browser.execute_script("return document.body.scrollHeight")
            productDataList, scroll_number = [], 1
            while True:
                print(f'{dt.now().strftime("%H:%M:%S")} Scroll nro: {scroll_number:,.0f}', end = '\r')
                # Scroll hasta el final de la pagina
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # captura las urls de la pagina hasta donde está cargada
                productDataList.append(getAllProductData(browser))

                # esperar a que la pagina cargue
                time.sleep(scrollWaitTime)

                # Calcula la nueva altura de la pagina despues de hacer scroll y lo compara con la latura anterior
                newHeight = browser.execute_script("return document.body.scrollHeight")
                if newHeight == lastHeight:
                    break
                lastHeight = newHeight
                scroll_number += 1

            productDataList.append(getProductURLs(browser))
            
            return (productDataList)
    
    def getAllProductData(self):
        """
        PENDING DOCUMENTATION...
        """

        productDataList = []
        for catURL in self.getCategoriesList():
            try:
                productDataList.append(self.productDataFromCategory(catURL=catURL, scrollWaitTime=2))
            except:
                continue
        
        return(productDataList)