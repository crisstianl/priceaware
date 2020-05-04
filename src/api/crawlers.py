from bs4 import BeautifulSoup
from urllib import request, parse
from ssl import SSLContext 
from sys import exc_info
from selenium import webdriver
from main.settings import WEB_DRIVER


def factory(store, query):
    if 'altex' == store.title.lower():
        return AltexCrawler(store, query)
    elif 'emag' == store.title.lower():
        return EmagCrawler(store, query)
    elif 'evomag' == store.title.lower():
        return EvomagCrawler(store, query)
    elif 'olx' == store.title.lower():
        return OlxCrawler(store, query)
    elif 'cel' == store.title.lower():
        return CelCrawler(store, query)
    else:
        return None

class AltexCrawler(object):
    def __init__(self, store, query):
        super().__init__()
        self.url = store.address + "cauta/?" +  parse.urlencode({'q': query})
        self.store = store

    def run(self, callback):
        print("Scrapping altex:", self.url)
        driver = None
        try:
            driver = webdriver.PhantomJS(executable_path=WEB_DRIVER)
            driver.get(self.url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')           
            # print(soup.prettify())

            container_ul = soup.find('ul', {'class': 'Products'})
            for div in container_ul.find_all('li', {'class': 'Products-item'}, limit=self.store.size):
                # find product name
                name_div = div.find('div', {'class': 'Product-list-center'})
                name_href = name_div.find('a', {'class': 'Product-name'})
                name = name_href.text

                # find product link
                link = name_href.get('href')

                # find product price
                price_div = div.find('div', {'class': 'Product-list-right'})
                price_div = price_div.find('div', {'class': 'Price-current'})
                p_childs = price_div.children
                price = "{0}{1} {2}".format(next(p_childs).string, next(p_childs).string, next(p_childs).string)
                
                # post result
                callback(name, link, price, self.store)
        except Exception as e:
            print("Scrapping error \"", exc_info()[0], "\" and message \"", e, "\"")
        finally:
            print("Scrapping altex completed")
            if driver: driver.quit()

        
class EmagCrawler(object):
    def __init__(self, store, query):
        super().__init__()
        self.url = store.address + "search/" +  parse.quote(query)
        self.store = store

    def run(self, callback):
        print("Scrapping emag:", self.url)
        httpPage = None
        try:
            httpPage = request.urlopen(self.url, context=SSLContext())
            soup = BeautifulSoup(httpPage.read(), 'html.parser') 
            # print(soup.prettify())

            container_div = soup.find('div', {'id': 'card_grid'})
            for div in container_div.find_all('div', {'class': 'card-item'}, limit=self.store.size):
                # find product name
                name_div = div.find('div', {'class': 'card-section-mid'})
                name_href = name_div.find('a', {'class': 'product-title'})
                name = name_href.text

                # find product link
                link = name_href.get('href')
                
                # find product price
                price_div = div.find('div', {'class': 'card-section-btm'})
                price_p = price_div.find('p', {'class': 'product-new-price'})             
                price = "{0},{1} {2}".format(price_p.contents[0].string, price_p.contents[1].string, price_p.contents[-1].string)

                # post result
                callback(name, link, price, self.store)
        except Exception as e:
            print("Scrapping error \"", exc_info()[0], "\" and message \"", e, "\"")
        finally:
            print("Scrapping emag completed")
            if httpPage: httpPage.close()


class EvomagCrawler(object):
    def __init__(self, store, query):
        super().__init__()
        self.url = store.address + "?" + parse.urlencode({'sn.q': query})
        self.store = store

    def run(self, callback):
        print("Scrapping evomag:", self.url)
        driver = None
        try:
            driver = webdriver.PhantomJS(executable_path=WEB_DRIVER)
            driver.get(self.url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')           
            # print(soup.prettify())

            container_div = soup.find('div', {'class': 'product_grid'})
            for div in container_div.find_all('div', {'class': 'nice_product_container'}, limit=self.store.size):
                # find product name
                name_div = div.find('div', {'class': 'npi_name'})
                name_href = name_div.findChild()
                name = name_href.text

                # find product link
                link = name_href.get('href')
                
                # find product price
                price_div = div.find('span', {'class': 'real_price'})
                price = price_div.text
                
                # post result
                callback(name, link, price, self.store)
        except Exception as e:
            print("Scrapping error \"", exc_info()[0], "\" and message \"", e, "\"")
        finally:
            print("Scrapping evomag completed")
            if driver: driver.quit()


class OlxCrawler(object):
    def __init__(self, store, query):
        super().__init__()
        self.url = store.address + "oferte/q-" +  parse.quote(query.replace(' ', '-'))
        self.store = store

    def run(self, callback):
        print("Scrapping olx:", self.url)
        driver = None
        try:        
            driver = webdriver.PhantomJS(executable_path=WEB_DRIVER)
            driver.get(self.url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')           
            #print(soup.prettify())

            container_table = soup.find('table', {'id': 'offers_table'})
            for row in container_table.find_all('tr', {'class': 'wrap'}, limit=self.store.size):
                inner_table = row.find('table')
                first_row = inner_table.findChild().findChild()
                cols = first_row.find_all('td')

                name_a = cols[1].find('a', {'class': ['detailsLink', 'detailsLinkPromoted']})
                name = name_a.text
                link = name_a.get('href')

                price_p = cols[2].find('p', {'class': 'price'})
                price = price_p.text

                # post result
                callback(name, link, price, self.store)
        except Exception as e:
            print("Scrapping error \"", exc_info()[0], "\" and message \"", e, "\"")
        finally:
            print("Scrapping olx completed")
            if driver: driver.quit()


class CelCrawler(object):
    def __init__(self, store, query):
        super().__init__()
        self.url = store.address + "cauta/" +  parse.quote(query)
        self.store = store

    def run(self, callback):
        print("Scrapping cel:", self.url)
        driver = None
        try: 
            driver = webdriver.PhantomJS(executable_path=WEB_DRIVER)
            driver.get(self.url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')           
            #print(soup.prettify())

            container_div = soup.find('div', {'id': 'listProducts'})
            for item_div in container_div.find_all('div', {'class': 'product_data'}, limit=self.store.size):
                # find product name
                info_div = item_div.find('div', {'class': 'productListing-nume'})
                name_div = info_div.find('h2', {'class': 'productTitle'})
                name_href = name_div.findChild()
                name = name_href.findChild().text

                # find product link
                link = name_href.get('href')
                
                # find product price
                price_div = info_div.find('div', {'class': 'pretWrapper'})
                price_childs = price_div.findChild().findChildren()
                price = price_childs[0].text + " " + price_childs[1].text
                
                # post result
                callback(name, link, price, self.store)
        except Exception as e:
            print("Scrapping error \"", exc_info()[0], "\" and message \"", e, "\"")
        finally:
            print("Scrapping cel completed")
            if driver: driver.quit()
