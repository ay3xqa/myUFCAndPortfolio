from scrapy.crawler import CrawlerProcess
from maincardspider import MaincardspiderSpider  

def run_spider():
    process = CrawlerProcess()
    process.crawl(MaincardspiderSpider)
    process.start()

if __name__ == "__main__":
    run_spider()