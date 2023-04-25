from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import timedelta

start_time = time.time()

def main():
    content = parse_html(URL= "https://www.betway.co.ke/sport/basketball", opt= intialize_hl_browser())
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
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup

def get_data(soup_object) -> list:
    """ Using css selectors from the soup object the function targets specified data from the webpage
        then stores them in a list
        
        Args:
            soup_object -> webpage content
        
    """

    date = [element.get_text().replace("\n", "").replace(" ", "").strip() for element in soup_object.select('a > label.ellips.PaddingScreen.theOtherFont.label__league_title')]
    home_team = [element.get_text().strip() for element in soup_object.select('div.col-xs-12.col-md-12.col-lg-7.outcomes.betbooster-outcomeRow > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)')]
    away_team = [element.get_text().strip() for element in soup_object.select('div.col-xs-12.col-md-12.col-lg-7.outcomes.betbooster-outcomeRow > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)')]
    ht_1 = [element.get_text().strip() for element in soup_object.select('div.col-xs-12.col-md-12.col-lg-7.outcomes.betbooster-outcomeRow > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')]
    at_2 = [element.get_text().strip() for element in soup_object.select('div.col-xs-12.col-md-12.col-lg-7.outcomes.betbooster-outcomeRow > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)')]
    match_info = [date, home_team, away_team, ht_1, at_2]
    return match_info

def save_data(match_data) -> None:
    """ Write the data to a csv file in preparation for comparative analysis

        Args:
            match_data -> a list of lists of scraped data
    """
    
    gt, ht, at, h1, a2 = match_data
    df = pd.DataFrame({
        "date": gt, "home_team": ht, "away_team": at, 
        "ht_1": h1, "at_2": a2
    })
    df.drop_duplicates(keep= False, inplace= False)
    df.to_csv("bw_basketball.csv", mode= "a",index= False, header= True)
    print(".csv file successfully created")

if __name__ == "__main__":
    main()


elapsed_time_secs = time.time() - start_time
print("Execution time: %s secs (Wall clock time)" % timedelta(seconds= round(elapsed_time_secs)))