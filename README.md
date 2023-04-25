# Bookmaker-Scraper-and-Arbitrage-Finder

This repository contains Python scripts that scrape two bookmaker websites to obtain data on team names, odds, game ID, and match time and date on one sport, i.e., basketball. 
The scripts use the following libraries: Selenium, Beautiful Soup, Chromedriver, Fuzzywuzzy, Pandas, and Numpy.

The two main scripts, sp_bb_scraper.py and bw_bb_scraper.py, use Chromedriver to scrape data from the bookmaker websites. 
They then use Beautiful Soup to parse the HTML and extract the relevant data, such as team names and odds, game ID, and match time and date. 
The scraped data is written to CSV files for later comparative analysis.

The third script, bookmaker_arbitrage_finder.py, matches the team names of the different bookmakers using the Fuzzywuzzy library. 
Then calculates the arbitrage opportunities using Numpy and Pandas. The output is a list of matched matches from the two main scripts with an arbitrage opportunity.

## Dependencies:
> 1. Chromedriver (version should match the installed Chrome browser version)
> 2. Selenium
> 3. Beautiful Soup
> 4. Fuzzywuzzy[speedup]
> 5. Pandas
> 6. Numpy

To run the scripts, first, ensure that all the dependencies are installed. 
Then, edit the two main scripts to specify the bookmakers and sports to scrape. Run the scripts to scrape the data and save it to CSV files. 
Finally, run the bookmaker_arbitrage_finder.py script to find arbitrage opportunities in the scraped data.

Note that the chromedriver executable must be in the system PATH or located in the same directory as the script. 
Also, I ensured that the bookmakers being scraped allow web scraping and that scraping does not violate their terms of service.
