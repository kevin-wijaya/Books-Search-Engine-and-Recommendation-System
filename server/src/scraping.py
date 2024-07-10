# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as bs
import os, random, time, requests
import pandas as pd

# initial UA and config
CURDIR = os.path.dirname(os.path.realpath(__file__))
ROOTDIR = os.path.dirname(CURDIR)
CONFIGDIR = os.path.join(CURDIR, 'config')
UA = [ua.replace('\n', '') for ua in open(os.path.join(CONFIGDIR, 'user-agents.txt')).readlines()]

# the url
amazon_url = 'https://www.amazon.com/dp/<ISBN>/'
isbn_search_url = 'https://isbnsearch.org/isbn/<ISBN>'

# abbriviate code
CLICK = ec.element_to_be_clickable
LOCATED = ec.presence_of_element_located
LOCATEDS = ec.presence_of_all_elements_located

# list DOM amazon
DOM_AMAZON = {
    'title':          (By.XPATH, '//*[@id="productTitle"]'),
    'description':    (By.XPATH, '//*[@id="bookDescription_feature_div"]/div/div[1]'),
    'button-captcha': (By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button')
}

# list DOM isbn search
DOM_ISBN_SEARCH = {
    'title':          ('h1', None),
    'author':         ('strong', lambda _: _ in ['Author:', 'Authors:']),
    'publisher':      ('strong', 'Publisher:'),
    'year' :          ('strong', 'Published:')
}

# class scraper
class Scraper:
    def __init__(self, debug) -> None:
        self.debug = debug
        self.driver = None
        self.headers = None
        self.data = []
    
    # function for start new session driver with user-agent
    def start(self, ua:list) -> None:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging']) 
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument("--disable-features=Permissions-Policy")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--log-level=1')
        options.add_argument(f'user-agent={ua}')
        if not self.debug: options.add_argument('--headless')
        self.headers = {'User-Agent': ua}
        self.driver = webdriver.Chrome(options=options)
        self.driver.delete_all_cookies()
        print(f'[INFO] start session -> UA : {ua}')
    
    # function for end current session driver
    def stop(self, ua:list) -> None:
        self.driver.delete_all_cookies()
        self.driver.close()
        self.driver.quit()
        print(f'[INFO] destroy session -> UA : {ua}')
    
    # shorthand for webdriverwait
    def wait(self, timeout:float=7.5) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout)
    
    # decoration for rotating user-agents
    def rotatingUserAgent(func:any) -> any:
        def _(self, *args, **kwargs):
            random.shuffle(UA)
            for ua in UA:
                try:
                    self.start(ua) 
                    result = func(self, *args, **kwargs)
                    self.stop(ua)
                    return result
                except Exception as e:
                    print('[ERRO] UA got blocked, change UA')
                    self.stop(ua)
            else:
                print('[FAIL] all UA got blocked')
        return _
    
    # get book by ISBN (dev only)
    @rotatingUserAgent
    def get_books(self, list_isbn:list) -> pd.DataFrame:
        # iterate the data
        status_ua = True
        for idx, isbn in enumerate(list_isbn):
            book = None
            try:
                # start scraping isbnsearch
                query_url_1 = isbn_search_url.replace('<ISBN>', isbn)
                result = requests.get(query_url_1, self.headers)

                # check the status_code, if it is not 200, proceed to the next data
                soup = None
                if result.status_code == 200:
                    soup = bs(result.content, 'html.parser')
                else: continue
                
                # Extract the book details
                try: 
                    title = soup.find(DOM_ISBN_SEARCH['title'][0]).text
                    author = soup.find(DOM_ISBN_SEARCH['author'][0], string=DOM_ISBN_SEARCH['author'][1])
                    publisher = soup.find(DOM_ISBN_SEARCH['publisher'][0], string=DOM_ISBN_SEARCH['publisher'][1])
                    year = soup.find(DOM_ISBN_SEARCH['year'][0], string=DOM_ISBN_SEARCH['year'][1])
                    description = '<UNDEFINED>'
                except Exception as e:
                    print(f'[ERRO] failed find soup, error msg: {str(e)}')
                    
                print(f'[INFO] {title=}')
                
                try:
                    # start scraping amazon
                    query_url_2 = amazon_url.replace('<ISBN>', isbn)
                    self.driver.get(query_url_2)
                    
                    try: 
                        # check if captcha appear
                        self.wait(0.5).until(LOCATED(DOM_AMAZON['button-captcha']))
                        print(f'[INFO] captcha detected')
                        self.driver.refresh()
                        self.wait(0.5).until(LOCATED(DOM_AMAZON['button-captcha']))
                        status_ua = False
                        raise
                    except: pass
                    
                    # check if the book is exists in amazon
                    title = self.wait().until(LOCATED(DOM_AMAZON['title'])).text
                    
                    # fill with new value
                    try: description = self.wait().until(LOCATED(DOM_AMAZON['description'])).text
                    
                    # fill with tag value
                    except: description = '<NO_DESCRIPTION>'

                except Exception as e:
                    # check status UA
                    if status_ua == False: raise
                
                # create a book detail
                book = {
                    'isbn': isbn,
                    'title': title,
                    'description': description,
                    'author': author.next_sibling.strip() if author else pd.NA,
                    'year_of_publication': year.next_sibling.strip()[:4] if year else pd.NA,
                    'publisher': publisher.next_sibling.strip() if publisher else pd.NA,
                }
                
            except Exception as e:
                # check status UA
                if status_ua == False: raise
                
                # basic failure logging with print
                print(f'[ERRO] item [{idx}]: failed to scrape the data for ISBN [{isbn}], the book doesn\'t exist or is undefined in the amazon store')
                time.sleep(0.9)
                
            finally:
                # append to data
                self.data.append(book)
                
        # return the data
        return pd.DataFrame(self.data)
    
    # get all description by ISBN (dev only)
    @rotatingUserAgent
    def add_descriptions(self) -> None:
        # read data from csv
        data = pd.read_csv(os.path.join(ROOTDIR, 'data', 'complete_books.csv'), low_memory=False)
        data_copy = data.copy(deep=True)
        
        # get indexes where link and description is null (cp: 3635, 6414, 8631, 9591, 14970, 24000)
        index = data_copy.index[
            ((data_copy['description'].isna() == True) | (data_copy['description'] == '<UNDEFINED>')) 
            & (data_copy.index > 24000)
            ]

        # iterate the data
        status_ua = True
        counter = 1
        for idx in index:
            try:
                # get isbn
                isbn = data['isbn'].iloc[idx]
                
                # start scraping
                query_url = amazon_url.replace('<ISBN>', isbn)
                self.driver.get(query_url)
                
                try: 
                    # check if captcha appear
                    self.wait(0.5).until(LOCATED(DOM_AMAZON['button-captcha']))
                    print(f'[INFO] captcha detected')
                    self.driver.refresh()
                    self.wait(0.5).until(LOCATED(DOM_AMAZON['button-captcha']))
                    status_ua = False
                    raise
                except: pass
                
                # check if the book is exists in amazon.com
                title = self.wait().until(LOCATED(DOM_AMAZON['title'])).text
                
                # fill with new value
                try: data.loc[idx, 'description'] = self.wait().until(LOCATED(DOM_AMAZON['description'])).text
                
                # fill with tag value
                except: data.loc[idx, 'description'] = '<NO_DESCRIPTION>'

                # basic success logging with print
                print(f'[INFO] item [{idx}]: Successfully scraped the data for ISBN [{isbn}], title [{title}]')
                
            except Exception as e:
                # check status UA
                if status_ua == False: raise
                
                # fill with tag value
                data.loc[idx, 'description'] = '<UNDEFINED>'
                
                # basic failure logging with print
                print(f'[ERRO] item [{idx}]: failed to scrape the data for ISBN [{isbn}], the book doesn\'t exist or is undefined in the amazon store')
                time.sleep(0.9)
                
            finally:             
                # overwrite to complete_books.csv
                if counter % 10 == 0:
                    print(f'[INFO] overwrite data ({counter}/{len(index)}) ({len(data)})')
                    data.to_csv(os.path.join(ROOTDIR, 'data', 'complete_books.csv'), index=False)
                    time.sleep(1.1)
                counter += 1