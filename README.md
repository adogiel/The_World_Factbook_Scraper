# The_World_Factbook_Scraper
The project was designed to conduct web scraping from the CIA World Factbook website, specifically targeting countries in Africa and Europe with Beautiful Soup, Scrapy and Selenium scrapers. The purpose was to extract relevant information, store it in a structured format, namely a CSV file, and compare the scrapers performance.

Instruction for Scrapy

1. Download the Scrapy folder
2. In Visual Studio Code open the folder with spider factbook_scraper
3. In terminal write:
   cd spiders + enter
4. To run the code write command in the terminal:
   scrapy runspider factbook_spider.py -o countries.csv + enter
   To save it in file with other name than countries we can simply replace it with desired name
5. To limit the number of countries scraped you can change limit = False to limit = True
6. CSV is saved in the spider folder but you can also download it with clicking on csv and then File -> Save As
