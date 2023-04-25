from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import time
from datetime import timedelta
 
start_time = time.time()

def main():
    content = parse_html(URL= "https://www.ke.sportpesa.com/sports/basketball?sportId=2&section=upcoming&filterDay=-1&paginationOffset=90", opt= intialize_hl_browser())
    save_data(match_data= get_data(content)) 

def intialize_hl_browser():
    """Access chrome on headless mode. """

    options = Options() # headless browser
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors=yes")
    return options

def parse_html(URL, opt):
    """ Load the html and css contents of the speciied page, and its source into beautiful soup

        Args:
            URL -> webpage to crawl
            opt -> specify browser to crawl in headless mode
    """

    driver = webdriver.Chrome(r"C:\Users\ABC\Documents\python\Web scraper\chromedriver.exe", chrome_options= opt)
    driver.get(URL)
    # Load the contents of the page, its source into beautiful soup
    # It also allows one to select elements by using css selectors
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup

def get_data(soup_object) -> list:
    """ Using css selectors from the soup object the function targets specified data from the webpage
        then stores them in a list
        
        Args:
            soup_object -> webpage content
        
    """

    game_time = [element.get_text().strip() for element in soup_object.select('div.event-info.event-column > div:nth-child(1) > time-component > span')]
    date = [element.get_text().strip() for element in soup_object.select('div.event-info.event-column > div:nth-child(2) > time-component > span')]
    game_id = [element.get_text().strip() for element in soup_object.select('.event-info.event-column > div.event-text.ng-binding')]
    home_team = [element.get_text().strip() for element in soup_object.select('div.event-names.event-column > div:nth-child(1)[title]')]
    away_team = [element.get_text().strip() for element in soup_object.select('.event-names.event-column > div:nth-child(2)[title]')]
    ht_1 = [element.get_text().strip() for element in soup_object.select('.event-selections > div:nth-child(1) > div.ng-binding')]
    at_2 = [element.get_text().strip() for element in soup_object.select('.event-selections > div:nth-child(2) > div.ng-binding')]
    match_info = [game_time, date, game_id, home_team, away_team, ht_1, at_2]
    return match_info

def save_data(match_data) -> None:
    """ Write the data to a csv file in preparation for comparative analysis

        Args:
            match_data -> a list of lists of scraped data
    """

    gt, dt, gi, ht, at, h1, a2 = match_data
    df = pd.DataFrame.from_dict({
    "time": gt, "date": dt, "game_id": gi, 
    "home_team": ht, "away_team": at, 
    "ht_1": h1, "at_2": a2
    }, orient= "index")
    df = df.transpose()

    df.to_csv("sp_basketball.csv", mode= "a",index= False, header= True)
    print(".csv file successfully created")

if __name__ == "__main__":
    main()


elapsed_time_secs = time.time() - start_time
print("Execution time: %s secs (Wall clock time)" % timedelta(seconds= round(elapsed_time_secs)))